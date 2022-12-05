from django.db import models


class Book(models.Model):
    """Uploaded book"""
    objects = models.Manager()
    name = models.CharField(max_length=128)
    wholeText = models.TextField()
    uploadDate = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='cover/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'books'


class Word(models.Model):
    """Words from book"""
    objects = models.Manager()
    wordOriginal = models.CharField(max_length=128)
    wordTranslate = models.CharField(max_length=128)
    wordDescription = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.wordOriginal

    class Meta:
        db_table = 'words'


class WordLearned(models.Model):
    """Model to link a specific user and learned words"""
    objects = models.Manager()
    count = models.IntegerField(default=0)
    nextDayLearn = models.DateField(auto_now_add=True)
    is_learned = models.BooleanField(default=False)
    learnPerson = models.CharField(max_length=128)
    learnWord = models.ForeignKey(Word, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wordLearned'
