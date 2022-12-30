from datetime import datetime, timedelta
from django.db.models import QuerySet
from googletrans import Translator
from goen.models import Word, WordLearned, Story
from random import choice
import re


def get_ranking_list(users):
    """Render ranking list for Home table """
    ranking_list = {}
    for user in users:
        count = 0
        words = WordLearned.objects.filter(learn_person=user.pk)
        amount_learning_words = WordLearned.objects.filter(learn_person=user.pk).filter(is_learned=False).count()
        amount_learned_words = WordLearned.objects.filter(learn_person=user.pk).filter(is_learned=True).count()

        for word in words:
            count += word.progress
            count += word.is_learned * 100

        ranking_list[user.username + '_points'] = count
        ranking_list[user.username + '_amount_learning_words'] = amount_learning_words
        ranking_list[user.username + '_amount_learned_words'] = amount_learned_words

    return ranking_list


def add_word_to_learn(word: str, story: Story, user_pk: int) -> None:
    """Adds word from story to learn """

    word = _delete_symbols(word)

    if not WordLearned.objects.filter(learn_person=user_pk,
                                      learn_word__word_original=word).exists():
        translator = Translator()
        word = Word.objects.get_or_create(word_original=word,
                                          word_translate=translator.translate(word, dest='ru').text.lower(),
                                          word_description=_get_sentence_by_word(story.whole_text, word), story=story)
        WordLearned.objects.create(learn_person=user_pk, learn_word=word[0])


def get_words_to_learn(user_pk: int) -> QuerySet:
    """Get words for study by date and repeat count"""
    return WordLearned.objects.filter(learn_person=user_pk, next_day_learn__lte=datetime.now().date()).exclude(
        is_learned=True)


def check_exist_words_to_learn(user_pk: int) -> bool:
    """Get words for study by date and repeat count"""
    return WordLearned.objects.filter(learn_person=user_pk, next_day_learn__lte=datetime.now().date()).exclude(
        is_learned=True).exists()


def see_translate(dict_vars, words_list, word, user_pk):
    _decrease_word_count(words_list.first())
    dict_vars['answer'] = word.word_original
    dict_vars['progress'] = WordLearned.objects.get(learn_word=word, learn_person=user_pk).progress


def right_answer(dict_vars, words_list, word, user_pk):
    _increase_word_count(words_list.first())
    dict_vars['out'] = _out_compliment()
    dict_vars['out_color'] = '#7bad45'
    dict_vars['answer'] = word.word_original
    dict_vars['display_btn_next'] = ''
    dict_vars['progress'] = WordLearned.objects.get(learn_word=word, learn_person=user_pk).progress


def wrong_answer(dict_vars):
    dict_vars['out'] = _out_disappointment()
    dict_vars['out_color'] = '#d6a445'


def _decrease_word_count(word_learned: WordLearned) -> None:
    """Decrease word counter after right answer"""

    if word_learned.progress == 0:
        WordLearned.objects.filter(pk=word_learned.pk).update(next_day_learn=_date_update(0))
    else:
        WordLearned.objects.filter(pk=word_learned.pk).update(progress=word_learned.progress - 1,
                                                              next_day_learn=_date_update(0))


def _increase_word_count(word_learned: WordLearned) -> None:
    """Increase word counter after right answer"""

    if word_learned.progress == 0:
        WordLearned.objects.filter(pk=word_learned.pk).update(progress=word_learned.progress + 1,
                                                              next_day_learn=_date_update(
                                                                  word_learned.progress + 1))
    else:
        WordLearned.objects.filter(pk=word_learned.pk).update(progress=word_learned.progress + 1,
                                                              next_day_learn=_date_update(
                                                                  word_learned.progress))
    if word_learned.progress >= 7:
        WordLearned.objects.filter(pk=word_learned.pk).update(is_learned=True)


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
    sentence = 'No sentence'
    try:
        pattern = re.compile(r"([A-Z][^.!?]*({})[^.!?]*[.!?])".format(word))
        sentence = pattern.findall(story)[0][0].replace(word, '*' * len(word))
        return sentence
    except IndexError:
        try:
            pattern = re.compile(r"(({})[^.!?]*[^.!?])".format(word), re.IGNORECASE)
            sentence = pattern.findall(story)[0][0].replace(word.capitalize(), '*' * len(word))
            return sentence
        except IndexError:
            return sentence
