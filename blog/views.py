from django.shortcuts import render
from .models import Article, Comment
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import ArticleCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse


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
