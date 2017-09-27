from django.shortcuts import get_object_or_404
from .models import Article, Comment
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import ArticleCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from itertools import chain
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.core.mail import send_mail



class Article_create(LoginRequiredMixin, FormView):
    template_name = 'blog/article/create.html'
    form_class = ArticleCreateForm
    # if article successfully created, redirect ot main page
    success_url = '/'
    login_url = '/login/'

    def form_valid(self, form):
        # get cleaned data from form
        cd = form.cleaned_data
        # create object, but don't save to database yet
        new_item = form.save(commit=False)
        # author equal you
        new_item.user = self.request.user
        # save to database
        new_item.save()
        # empty list
        emails = []
        # get your followers ids
        your_follower_ids =  self.request.user.following.values_list('id', flat=True)
        # get Users by your followers ids
        your_followers = User.objects.filter(id__in=your_follower_ids)
        # if you have followers
        if your_followers:
            # typical for
            for user in your_followers:
                # if user have an email
                if user.email:
                    # push to list
                    emails.append(user.email)
        # send an emails
        send_mail('New article was recently published!', ('User ' + str(self.request.user) + ' published new article! Check this in your news page!'), 'rellay2.worker@gmail.com',     emails, fail_silently=False)
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

# Sorry for not class-based view :)
@ajax_required
@require_POST
@login_required
def user_watch(request):
    # Get data from ajax
    article = request.POST.get('id')
    action = request.POST.get('action')
    # If data from ajax is not Null
    if article and action:
        # get object
        article = get_object_or_404(Article, id=article)
        # if action from ajax equal "saw"
        if action == 'saw':
            # add to this article your view
            article.users_view.add(request.user)
        else:
            # remove your view from article
            article.users_view.remove(request.user)
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'ko'})
