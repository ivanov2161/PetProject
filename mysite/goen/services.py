from datetime import datetime, timedelta
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from googletrans import Translator
from goen.forms import UploadBook, Answer
from goen.models import Word, WordLearned
from random import choice


def add_book(request: WSGIRequest) -> HttpResponse:
    if request.user.username == 'admin':
        form = UploadBook(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'home.html')
        else:
            form = UploadBook()
        return render(request, 'uploadBook.html', {'form': form})
    else:
        return render(request, 'home.html')


def add_word_to_learn(word: str, book, user_pk) -> None:  # Recode this function
    word = _delete_symbols(word)
    if len(WordLearned.objects.filter(learnPerson=user_pk).filter(
            learnWord__wordOriginal=word)) == 0:  # To ask Vadim
        translator = Translator()
        if len(Word.objects.filter(wordOriginal=word)) == 0:

            word = Word(wordOriginal=word, wordTranslate=translator.translate(word, dest='ru').text.lower(),
                        wordDescription='nope', book=book)
            word.save()
        else:
            word = Word.objects.get(wordOriginal=word)

        word_learned = WordLearned(learnPerson=user_pk, learnWord=word)
        word_learned.save()


def get_words_to_learn(user_pk: int) -> QuerySet:
    return WordLearned.objects.filter(learnPerson=user_pk).filter(
        nextDayLearn__lte=datetime.now().date()).exclude(is_learned=True)


def exam_or_see_words(request: WSGIRequest) -> tuple:
    try:
        words_list = get_words_to_learn(request.user.pk)
        out = '...'
        out_color = 'white'
        answer = {'answer': '...'}
        word = words_list[0].learnWord
        progress = WordLearned.objects.filter(learnWord=word).filter(learnPerson=request.user.pk)
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

        return render(request, 'learningWords.html', {'inputAnswer': Answer(), 'word': word.wordTranslate,
                                                      'answer': answer['answer'], 'out': out, 'color': out_color,
                                                      'progress': progress[0].count, 'amount': len(words_list),
                                                      'display_btn_next': display_btn_next})

    except IndexError:
        return render(request, 'learningWords.html', {'inputAnswer': Answer(), 'word': 'The words are over',
                                                      'answer': 'We are waiting for you tomorrow!',
                                                      'out': '...', 'color': 'white', 'progress': '0',
                                                      'display_btn_next': 'none'})


def _decrease_word_count(words_list: QuerySet) -> None:
    if words_list[0].count == 0:
        WordLearned.objects.filter(pk=words_list[0].pk).update(nextDayLearn=_date_update(0))
    else:
        WordLearned.objects.filter(pk=words_list[0].pk).update(count=words_list[0].count - 1,
                                                               nextDayLearn=_date_update(0))


def _increase_word_count(words_list: QuerySet) -> None:
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


def _out_compliment():
    compliment = ['RIGHT!', 'OUTSTANDING!', 'SPECTACULAR!', 'EXCELLENT!', 'MAGNIFICENT!']
    return choice(compliment)


def _out_disappointment():
    disappointment = ['WRONG', 'INCORRECT', 'MISTAKE', 'FALSE']
    return choice(disappointment)


def _delete_symbols(text: str) -> str:
    chars = ('’s', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ' - ', '_', '+', '=', ':',
             ';', ' \'', '\' ', '\"', '\"', '«', '»', '{', '}', '[', ']', '.', ',', '?', '/', '|,', '~',
             '`', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' I ', ' i ', ' he ', ' we ',
             ' our ', ' be ', ' in ', ' a ', ' the ', ' an ', ' is ', ' q ', ' w ', ' e ', ' r ', ' t ',
             ' y ', ' u ', ' i ', ' o ', ' p ', ' a ', ' s ', ' d ', ' f ', ' g ', ' h ', ' j ', ' k ', ' l ',
             ' z ', ' x ', ' c ', ' v ', ' b ', ' n ', ' m ', ' ')
    cyrillic = 'йцукенгшщзхъфывапролджэячсмитьбюё'
    text = ' ' + text + ' '
    for i in chars:
        text = text.replace(i, '')
    for i in cyrillic:
        text = text.replace(i, '')
    return text


def _date_update(count: int) -> datetime.date:
    return datetime.now().date() + timedelta(days=count)
