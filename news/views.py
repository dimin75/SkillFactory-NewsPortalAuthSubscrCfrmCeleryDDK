from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import CreatePostForm, BasePostForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
# from .signals import send_post_notification
from .signals import notify_news_creator

# Create your views here.
class PostView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'postView'

class PostList(ListView):
    # Model to output
    model = Post
    # template for output
    template_name = 'news_list.html'
    # list name
    context_object_name = 'postList'
    queryset = Post.objects.order_by('-created_at')
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class SearchList(PostList):
    template_name = 'search.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',
                           'news.change_post')
    template_name = 'add_post.html'
    form_class = CreatePostForm
    success_url = '/news/'

    def post(self, request, *args, **kwargs):
        form = CreatePostForm(request.POST)

        if form.is_valid():
            # post = Post(
            #     author=Author.objects.get(user=request.user),
            #     title=request.POST['title'],
            #     text=request.POST['text']
            # )
            post = form.save(commit=False)
            post.author = Author.objects.get(user=request.user)
            post.title = request.POST['title']
            post.text = request.POST['text']
            # post.save()
            try:
                post.save()
                # код обработки после успешного сохранения
                return redirect('/news/')  # или куда вам нужно перенаправить после успешного сохранения
            # except ValidationError as e:
            #     # Обработка ошибки валидации
            #     print(f'Validation Error: {e}')
            #     return render(request, self.template_name, {'form': form, 'error': 'Validation error'})
            except Exception as e:
                # Обработка других исключений
                print(f'Error: {e}')
                print('Все равно возвращаемся на страницу новостей в исходную точку...')
                return redirect('/news/')
                # return render(request, self.template_name, {'form': form, 'error': 'An error occurred'})
        else:
            # Форма не прошла валидацию, обработка ошибок или отображение формы с ошибками
            return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #     post = Post(
    #         author=Author.objects.get(user=request.user),
    #         title=request.POST['title'],
    #         text=request.POST['text']
    #     )
    #
    #     post.save()

        # for id in request.POST.getlist('categories'):
        #     postCategory = PostCategory(post=post, category=Category.objects.get(pk=id))
        #     postCategory.save()
        #
        # subject = f'{post.created_at.strftime("%Y-%M-%d")} вами создана новая новость!'
        # content = render_to_string('post_created.html', {'post': post, })
        # email = request.user.email

        # Отправка уведомлений о новой статье через send_mail()
        # send_post_notification(subject, email, content)

        # Отправка уведомлений о новой статье через mail_managers()
        # print('передача из views.py:')
        # print(subject)
        # print(content)
        # print(email)
        # notify_news_creator(subject=subject, content=content, email=email)
        # notify_news_creator()



        # return redirect('/news/')

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'post_edit.html'
    form_class = BasePostForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

class SubscriptionView(ListView):
    model = Category
    template_name = 'subscriptions.html'
    context_object_name = 'subscriptionView'
    queryset = Category.objects.order_by('name')
    paginate_by = 2

@login_required
def add_subscribe(request):
    user = request.user
    category = Category.objects.get(pk=request.POST['cat_id'])
    subscribe = CategorySubscribers(user=user, category=category)
    subscribe.save()

    return redirect('/subscriptions')