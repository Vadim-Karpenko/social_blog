from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='article_created')
    title = models.CharField(max_length=240)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True, blank=True)
    users_view = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_viewed',
                                        blank=True)

    def get_absolute_url(self):
        return reverse('detail', args=[self.pk])

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments_created')
    article= models.ForeignKey(Article, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user.get_full_name, self.image)
