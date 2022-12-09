from django.contrib import admin

from .models import Story, Word, WordLearned

admin.site.register(Story)
admin.site.register(Word)
admin.site.register(WordLearned)
