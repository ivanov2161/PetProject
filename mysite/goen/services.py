from datetime import datetime, timedelta
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from googletrans import Translator
from goen.models import Word, WordLearned, Story
from random import choice
import re


def add_word_to_learn(word: str, story: Story, user_pk: int) -> None:
    """Adds word from story to learn """

    word = _delete_symbols(word)
    if WordLearned.objects.filter(learn_person=user_pk,
                                  learn_word__word_original=word).count() == 0:
        translator = Translator()
        if Word.objects.filter(word_original=word).count() == 0:

            word = Word.objects.create(word_original=word,
                                       word_translate=translator.translate(word, dest='ru').text.lower(),
                                       word_description=_get_sentence_by_word(story.whole_text, word), story=story)

        else:
            word = Word.objects.get(word_original=word)

        word_learned = WordLearned(learn_person=user_pk, learn_word=word)
        word_learned.save()


def get_words_to_learn(user_pk: int) -> QuerySet:
    """Get words for study by date and repeat count"""
    return WordLearned.objects.filter(learn_person=user_pk, next_day_learn__lte=datetime.now().date()).exclude(
        is_learned=True)


def check_words(request: WSGIRequest, answer: dict, words_list: QuerySet, word: Word) -> tuple:
    """Function for testing learning words"""

    out = '...'
    out_color = 'white'
    display_btn_next = 'none'

    if request.POST.get('seeTranslate') == 'seeTranslate':
        _decrease_word_count(words_list)
        answer['answer'] = word.word_original
        return out, out_color, display_btn_next

    elif word.word_original == request.POST['answer'].lower():
        _increase_word_count(words_list)
        out = _out_compliment()
        out_color = '#7bad45'
        answer['answer'] = word.word_original
        display_btn_next = ''
        return out, out_color, display_btn_next

    else:
        out = _out_disappointment()
        out_color = '#d6a445'
        return out, out_color, display_btn_next


def _decrease_word_count(words_list: QuerySet) -> None:
    """Decrease word counter after right answer"""

    if words_list[0].count == 0:
        WordLearned.objects.filter(pk=words_list[0].pk).update(next_day_learn=_date_update(0))
    else:
        WordLearned.objects.filter(pk=words_list[0].pk).update(count=words_list[0].count - 1,
                                                               next_day_learn=_date_update(0))


def _increase_word_count(words_list: QuerySet) -> None:
    """Increase word counter after right answer"""

    if words_list[0].count == 0:
        WordLearned.objects.filter(pk=words_list[0].pk).update(count=words_list[0].count + 1,
                                                               next_day_learn=_date_update(
                                                                   words_list[0].count + 1))
    elif words_list[0].count >= 7:
        WordLearned.objects.filter(pk=words_list[0].pk).update(is_learned=True)

    else:
        WordLearned.objects.filter(pk=words_list[0].pk).update(count=words_list[0].count + 1,
                                                               next_day_learn=_date_update(
                                                                   words_list[0].count))


def _out_compliment() -> str:
    """Generate compliment for right answer"""

    compliment = ['RIGHT!', 'OUTSTANDING!', 'SPECTACULAR!', 'EXCELLENT!', 'MAGNIFICENT!']
    return choice(compliment)


def _out_disappointment() -> str:
    """Generate disappointment for wrong answer"""

    disappointment = ['WRONG', 'INCORRECT', 'MISTAKE', 'FALSE', '=(']
    return choice(disappointment)


def _delete_symbols(text: str) -> str:
    """Delete symbols from adding word"""

    chars = ('!@#$%^&*()1234567890":;,./?\|~`\'')
    return text.strip(chars)


def _date_update(count: int) -> datetime.date:
    """Update next day learn for word"""

    return datetime.now().date() + timedelta(days=count)


def _get_sentence_by_word(story: str, word: str) -> str:
    story += '.'
    try:
        pattern = re.compile(r"([A-Z][^.!?]*({})[^.!?]*[.!?])".format(word))

        return pattern.findall(story)[0][0].replace(word, '*' * len(word))
    except IndexError:
        pattern = re.compile(r"(({})[^.!?]*[.!?])\s".format(word.capitalize()))

        return pattern.findall(story)[0][0].replace(word.capitalize(), '*' * len(word))
