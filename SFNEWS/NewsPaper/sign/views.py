from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from news.models import Author, Post
import datetime


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['subscriptions'] = self.request.user.category_set.all()

        # check if this author has created more than 3 posts this day
        if self.request.user.groups.filter(name='authors').exists():
            user = self.request.user
            author = Author.objects.get(user=user)
            posts = Post.objects.filter(author=author).order_by('-date').values('date')
            length = len(posts)
            post_count = 0
            for i in range(length):
                condition = posts[i]['date'].date() == datetime.date.today()
                if condition:
                    post_count += 1
                else:
                    break

            context['posted_today'] = post_count
            context['can_create'] = post_count < 3

        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)

    return redirect('my_account')

