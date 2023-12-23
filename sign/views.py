from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .forms import BaseRegisterForm #, UserLoginForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps

# class BaseLoginView(CreateView):
#     model = User
#     form_class = UserLoginForm
#     success_url = '/news/'
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)

       # Кроме добавления автора в группу, добавляем запись о нем в таблицу БД
        author = apps.get_model('news', 'Author')()
        author.user = user
        author.save()

    return redirect('/')
# Create your views here.
