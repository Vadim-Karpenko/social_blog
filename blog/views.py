from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Article, Comment
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from .forms import ArticleCreateForm


class Article_create(FormView):
    template_name = 'blog/article/create.html'
    form_class = ArticleCreateForm
    success_url = '/'

    def form_valid(self, form):
        cd = form.cleaned_data
        new_item = form.save(commit=False)
        new_item.user = self.request.user
        new_item.save()
        return super(Article_create, self).form_valid(form)

class Detail(DetailView):
    model = Article
