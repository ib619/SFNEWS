from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category

from django.views import View
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 4


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_categories'] = self.object.category.all()
        return context


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = (
        'news.add_post',
    )
    template_name = 'post_create.html'
    form_class = PostForm

    def post(self, request):
        super(PostCreateView, self).post(request)
        post = self.object
        cats = post.category.all()
        for cat in cats:
            subs = cat.subscribers.all()
            for sub in subs:
                html_content = render_to_string(
                    'post_create_mail.html',
                    {
                        'post': post,
                        'sub_name': sub.username,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'{post.name}',
                    body=f'Hello, {sub.username}. New post in your favourite category!',
                    from_email='igorbodnarprog@yandex.ru',
                    to=[sub.email],
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()

        return redirect('posts')


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = (
        'news.change_post',
    )
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = (
        'news.delete_post',
    )
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostSearch(ListView):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'posts_search'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class Posts(View):
    def get(self, request):
        posts = Post.obejcts.order_by('-id')
        p = Paginator(posts, 1)
        posts = p.get_page(request.GET.get('page', 1))

        data = {
            'posts': posts,
        }

        return render(request, 'posts.html', data)


class CategoryView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category_subscribe.html'
    context_object_name = 'category'

    def post(self, request, *args, **kwargs):
        user = request.user
        id = self.kwargs.get('pk')
        category = Category.objects.get(pk=id)
        category.subscribers.add(user)
        category.save()

        return redirect('my_account')


class CategoryUnsubView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category_unsubscribe.html'
    context_object_name = 'category'

    def post(self, request, *args, **kwargs):
        user = request.user
        id = self.kwargs.get('pk')
        category = Category.objects.get(pk=id)
        category.subscribers.remove(user)
        category.save()

        return redirect('my_account')



