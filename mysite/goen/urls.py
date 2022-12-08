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
    path('learningWords/', exam_or_see_words, name='learningWords'),
    path('uploadBook/', upload_story),
    path('listOfBooks/', list_of_books),
    path('showBook/<int:book>', show_book_and_words, name='add_word'),
    path('showMyWords/', show_my_words),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
