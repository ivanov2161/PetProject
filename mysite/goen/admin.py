from django.contrib import admin

from .models import Story, Word, WordLearned


class StoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'upload_date']


class WordAdmin(admin.ModelAdmin):
    list_display = ['word_original', 'word_translate', 'word_description', 'story']
    search_fields = ['word_original']


class WordLearnedAdmin(admin.ModelAdmin):
    list_display = ['learn_word', 'learn_person', 'progress', 'is_learned', 'next_day_learn']
    search_fields = ['learn_word__word_original', 'learn_person', 'progress', 'is_learned']


admin.site.register(Story, StoryAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(WordLearned, WordLearnedAdmin)
