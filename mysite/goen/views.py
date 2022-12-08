from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterUserForm, LoginUserForm, UploadStory
from .models import Story, WordLearned
from .utils import DataMixin
from .services import get_words_to_learn, exam_or_see_words, add_word_to_learn, _temp_func


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sign Up")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Authentication')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def home(request):
    amount = get_words_to_learn(request.user.pk).count()
    users = User.objects.all()
    ranking_list = {}

    for i in users:
        count = 0
        person = WordLearned.objects.filter(learnPerson=i.pk)
        for j in person:
            count += j.count
            count += j.is_learned * 100
        ranking_list[i.username] = count

    ranking_list = dict(reversed(sorted(ranking_list.items(), key=lambda item: item[1])))

    return render(request, 'home.html', {'amount': amount, 'ranking_list': ranking_list})


def about(request):
    # _temp_func()
    return render(request, 'about.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def learning_words(request):
    return exam_or_see_words(request)


def list_of_stories(request):
    stories = Story.objects.all()
    return render(request, 'listOfStories.html', {'stories': stories})


def show_story_and_words(request, story):
    user_pk = request.user.pk
    story = Story.objects.get(pk=story)
    words = WordLearned.objects.filter(learnPerson=user_pk).filter(learnWord__story=story).order_by('pk')
    status = ''

    if request.method == 'POST':
        if request.POST.get('add'):
            add_word_to_learn(request.POST.get('add').lower(), story, user_pk)
        elif request.POST.get('delete'):
            WordLearned.objects.filter(pk=request.POST.get('delete')).delete()

    return render(request, 'showStory.html', {'words': words, 'name_story': story.name,
                                             'story': story.wholeText.split('\n'), 'status': status})


def show_my_words(request):
    words = WordLearned.objects.filter(learnPerson=request.user.pk)
    return render(request, 'showMyWords.html', {'words': words})


def upload_story(request):
    if request.user.username == 'admin':
        print(request.FILES)
        form = UploadStory(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = UploadStory()
        return render(request, 'uploadStory.html', {'form': form})
    else:
        return render(request, 'home.html')
