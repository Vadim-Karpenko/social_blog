from django.contrib import admin
from .models import Article, Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    list_filter = ['created']

admin.site.register(Article, ArticleAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'active')
    list_filter = ('created', 'active')
    search_fields = ('user', 'body')

admin.site.register(Comment, CommentAdmin)
