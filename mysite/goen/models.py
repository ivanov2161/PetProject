from django.db import models


class Story(models.Model):
    """Uploaded story"""
    objects = models.Manager()
    name = models.CharField(max_length=128)
    whole_text = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='cover/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stories'


class Word(models.Model):
    """Words from story"""
    objects = models.Manager()
    word_original = models.CharField(max_length=128)
    word_translate = models.CharField(max_length=128)
    word_description = models.TextField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def __str__(self):
        return self.word_original

    class Meta:
        db_table = 'words'


class WordLearned(models.Model):
    """Model to link a specific user and learned words"""
    objects = models.Manager()
    progress = models.IntegerField(default=0)
    next_day_learn = models.DateField(auto_now_add=True)
    is_learned = models.BooleanField(default=False)
    learn_person = models.CharField(max_length=128)
    learn_word = models.ForeignKey(Word, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wordLearned'
