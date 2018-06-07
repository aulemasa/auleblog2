#coding: utf-8

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=256)

    def __str__(self):
        return str("%s" % (self.category_name))


class Article(models.Model):
    title = models.CharField(max_length=256)
    meta_description = models.CharField(max_length=155, blank=True)
    meta_keywords = models.CharField(max_length=256, blank=True)
    url_title = models.SlugField(max_length=50)
    content = models.TextField()
    date_pub = models.DateField()
    active = models.BooleanField(verbose_name="Aktywne")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.IntegerField(default=0)
    category_article_id = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "{title}".format(title=self.title)

    def get_absolute_url(self):
        return "/article/%s%s%s/" % (self.url_title, ',', self.id)

    def absolute_title(self):
        return "%s" % self.title

    class Meta:
        ordering = ['date_pub']


class Comment(models.Model):
    add_date = models.DateTimeField(auto_now_add=True)
    comment_author = models.CharField(max_length=256)
    comment_content = models.TextField()
    post = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return str("%s: %s" % (self.comment_author, self.comment_content[:60]))
