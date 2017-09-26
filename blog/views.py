from .models import Article, Comment
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import ArticleCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from itertools import chain


class Article_create(FormView):
    template_name = 'blog/article/create.html'
    form_class = ArticleCreateForm
    success_url = '/'
    login_required = True

    def form_valid(self, form):
        cd = form.cleaned_data
        new_item = form.save(commit=False)
        new_item.user = self.request.user
        new_item.save()
        return super(Article_create, self).form_valid(form)

class DetailView(DetailView):
    model = Article

class ListView(LoginRequiredMixin, ListView):
    model = Article
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        def get_followers_news():
            following_ids = self.request.user.following.values_list('id', flat=True)
            # Filter only actions you was subscribe
            # Отфильтровать только действия на которые ты подписан
            articles = Article.objects.filter(user_id__in=following_ids)
            # Filter only your actions
            # Отфильтровать только твои действия
            your_articles = Article.objects.filter(user=self.request.user)
            # combine two different lists of QuerySet
            # Соеденить два разных списка QuerySet
            articles = list(chain(articles, your_articles))
            # make list back to QuerySet, and order by created date
            # Вернуть список обратно в QuerySet, и отсортировать по дате создания
            articles = Article.objects.filter(pk__in=[x.pk for x in articles]).order_by('-created')
            return articles

        context['followers_articles'] = get_followers_news()
        return context
