from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import CreatePostForm, BasePostForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
        post = Post(
            author=Author.objects.get(user=request.user),
            title=request.POST['title'],
            text=request.POST['text']
        )

        # post = Post(
        #     title=request.POST['title'],
        #     text=request.POST['text']
        # )
        # поскольку в задании не было указано ничего про авторизацию,
        # то используем одного уникального пользователя user1,
        # под которого в консоли закачана основная часть новостей.
        # user_loc = User.objects.get(username='user1')
        # author_user = Author.objects.get(user=user_loc)
        # post.author = author_user
        post.save()

        for id in request.POST.getlist('categories'):
            postCategory = PostCategory(post=post, category=Category.objects.get(pk=id))
            postCategory.save()

        return redirect('/news/')

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