from mysite.wsgi import *
from django.contrib.auth.models import User
from goen.models import Story, WordLearned, Word
from django.test import TestCase
from goen.services import _delete_symbols, add_word_to_learn, get_words_to_learn, check_exist_words_to_learn, \
    see_translate


class AddWordToLearnTestCase(TestCase):
    def test_add_word_to_learn(self):
        test_story = Story.objects.create(name='test_book', whole_text='test_text, test_text1', cover='test_cover')
        add_word_to_learn('test_text1', test_story, 1)
        word = Word.objects.get(word_original='test_text', story=test_story)
        result_word_learned = WordLearned.objects.get(learn_word=word, learn_person=1)
        self.assertEqual('test_text', result_word_learned.learn_word.word_original)


class GetWordsToLearnTestCase(TestCase):
    def test_get_words_to_learn(self):
        test_user = User.objects.create_user(username='TestUser')
        test_story = Story.objects.create(name='test_book', whole_text='test_first, test_second', cover='test_cover')
        add_word_to_learn('test_first', test_story, test_user)
        add_word_to_learn('test_second', test_story, test_user)
        result = get_words_to_learn(test_user)
        self.assertEqual(2, len(result))


class CheckExistWordsToLearn(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='TestUser')
        self.test_story = Story.objects.create(name='test_book', whole_text='test_first, test_second',
                                               cover='test_cover')

    def test_get_words_to_learn_true(self):
        add_word_to_learn('test_first', self.test_story, self.test_user)
        add_word_to_learn('test_second', self.test_story, self.test_user)
        result = check_exist_words_to_learn(self.test_user)
        self.assertTrue(result)

    def test_get_words_to_learn_false(self):
        result = check_exist_words_to_learn(self.test_user)
        self.assertFalse(result)


class SeeTranslateTestCase(TestCase):
    def setUp(self):
        self.dict_vars = {'answer': '', 'progress': 0}
        self.right_result = {'answer': 'test_first', 'progress': 4}
        self.test_user = User.objects.create_user(username='TestUser')
        self.test_story = Story.objects.create(name='test_book', whole_text='test_first, test_second',
                                               cover='test_cover')
        add_word_to_learn('test_first', self.test_story, self.test_user)
        add_word_to_learn('test_second', self.test_story, self.test_user)
        self.word = Word.objects.get(word_original='test_first')
        self.word_learned = WordLearned.objects.get(learn_word=self.word, learn_person=self.test_user)
        WordLearned.objects.filter(pk=self.word_learned.pk).update(progress=5)
        self.words_list = get_words_to_learn(self.test_user)

    def test_see_translate(self):
        see_translate(self.dict_vars, self.words_list, self.word, self.test_user)
        self.word_learned.refresh_from_db()
        self.assertEqual(4, self.word_learned.progress)
        self.assertEqual(self.right_result, self.dict_vars)


class DeleteSymbolsTestCases(TestCase):
    def test_delete_numbers(self):
        result = _delete_symbols('test1')
        self.assertEqual('test', result)

    def test_delete_symbols(self):
        result = _delete_symbols('test%#$')
        self.assertEqual('test', result)
