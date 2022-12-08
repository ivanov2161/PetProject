from datetime import datetime, timedelta
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.shortcuts import render
from googletrans import Translator
from goen.forms import Answer
from goen.models import Word, WordLearned
from random import choice
import re


def add_word_to_learn(word: str, story, user_pk) -> None:  # Recode this function
    """Adds word from story to learn """

    word = _delete_symbols(word)
    if WordLearned.objects.filter(learnPerson=user_pk,
                                  learnWord__wordOriginal=word).count() == 0:
        translator = Translator()
        if Word.objects.filter(wordOriginal=word).count() == 0:

            word = Word.objects.create(wordOriginal=word,
                                       wordTranslate=translator.translate(word, dest='ru').text.lower(),
                                       wordDescription=_get_sentence_by_word(story.wholeText, word), story=story)

        else:
            word = Word.objects.get(wordOriginal=word)

        word_learned = WordLearned(learnPerson=user_pk, learnWord=word)
        word_learned.save()


def get_words_to_learn(user_pk: int) -> QuerySet:
    """Get words for study by date and repeat count"""
    return WordLearned.objects.filter(learnPerson=user_pk, nextDayLearn__lte=datetime.now().date()).exclude(
        is_learned=True)


def exam_or_see_words(request: WSGIRequest) -> tuple:
    """Function for testing learning words"""

    try:
        words_list = get_words_to_learn(request.user.pk)
        out = '...'
        out_color = 'white'
        answer = {'answer': '...'}
        word = words_list.first().learnWord
        progress = WordLearned.objects.filter(learnWord=word, learnPerson=request.user.pk)
        display_btn_next = 'none'

        if request.method == 'POST':
            if request.POST.get('seeTranslate') == 'seeTranslate':
                _decrease_word_count(words_list)
                answer['answer'] = word.wordOriginal

            elif word.wordOriginal == request.POST['answer'].lower():
                _increase_word_count(words_list)
                out = _out_compliment()
                out_color = '#7bad45'
                answer['answer'] = word.wordOriginal
                display_btn_next = ''

            else:
                out = _out_disappointment()
                out_color = '#d6a445'

        return render(request, 'learningWords.html', {'inputAnswer': Answer(), 'word': word,
                                                      'answer': answer['answer'], 'out': out, 'color': out_color,
                                                      'progress': progress[0].count, 'amount': words_list.count(),
                                                      'display_btn_next': display_btn_next})

    except AttributeError:
        return render(request, 'learningWords.html', {'inputAnswer': Answer(), 'word': 'The words are over',
                                                      'answer': 'We are waiting for you tomorrow!',
                                                      'out': '...', 'color': 'white', 'progress': '0',
                                                      'display_btn_next': 'none'})


def _decrease_word_count(words_list: QuerySet) -> None:
    """Decrease word counter after right answer"""

    if words_list[0].count == 0:
        WordLearned.objects.filter(pk=words_list[0].pk).update(nextDayLearn=_date_update(0))
    else:
        WordLearned.objects.filter(pk=words_list[0].pk).update(count=words_list[0].count - 1,
                                                               nextDayLearn=_date_update(0))


def _increase_word_count(words_list: QuerySet) -> None:
    """Increase word counter after right answer"""

    if words_list[0].count == 0:
        WordLearned.objects.filter(pk=words_list[0].pk).update(count=words_list[0].count + 1,
                                                               nextDayLearn=_date_update(
                                                                   words_list[0].count + 1))
    elif words_list[0].count >= 7:
        WordLearned.objects.filter(pk=words_list[0].pk).update(is_learned=True)

    else:
        WordLearned.objects.filter(pk=words_list[0].pk).update(count=words_list[0].count + 1,
                                                               nextDayLearn=_date_update(
                                                                   words_list[0].count))


def _out_compliment() -> str:
    """Generate compliment for right answer"""

    compliment = ['RIGHT!', 'OUTSTANDING!', 'SPECTACULAR!', 'EXCELLENT!', 'MAGNIFICENT!']
    return choice(compliment)


def _out_disappointment() -> str:
    """Generate disappointment for wrong answer"""

    disappointment = ['WRONG', 'INCORRECT', 'MISTAKE', 'FALSE']
    return choice(disappointment)


def _delete_symbols(text: str) -> str:
    """Delete symbols from adding word"""

    chars = ('!@#$%^&*()1234567890":;,./?\|~`\'')
    return text.strip(chars)


def _date_update(count: int) -> datetime.date:
    """Update next day learn for word"""

    return datetime.now().date() + timedelta(days=count)


def _get_sentence_by_word(story, word):
    story += '.'
    try:
        pattern = re.compile(r"([A-Z][^.!?]*({})[^.!?]*[.!?])".format(word))

        return pattern.findall(story)[0][0].replace(word, '*' * len(word))
    except IndexError:
        pattern = re.compile(r"(({})[^.!?]*[.!?])\s".format(word.capitalize()))

        return pattern.findall(story)[0][0].replace(word.capitalize(), '*' * len(word))


def _temp_func():
    words = Word.objects.all()

    for word in words:
        Word.objects.filter(pk=word.pk).update(
            wordDescription=_get_sentence_by_word(word.story.wholeText, word.wordOriginal))
