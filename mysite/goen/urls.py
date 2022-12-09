from django.conf.urls.static import static
from django.urls import path

from goen.views import *
from mysite import settings

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('about/', about),
    path('learningWords/', learning_words, name='learningWords'),
    path('uploadStory/', upload_story),
    path('listOfStories/', list_of_stories),
    path('showStory/<int:story>', show_story_and_words, name='add_word'),
    path('showMyWords/', show_my_words),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
