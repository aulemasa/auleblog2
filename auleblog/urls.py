#coding: utf-8

from django.urls import path, re_path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogSitemap
import auleblog.views

sitemaps = {'posts':BlogSitemap}

urlpatterns = [
    path('', auleblog.views.articlesViews, name='articles_list'),
    re_path(r'^article/(?P<url_title>[-\w\d]+),(?P<article_id>\d+)/$', auleblog.views.articleViews, name='article'),
    re_path(r'^category/(?P<category_id>\d+)', auleblog.views.categoryViews),
    re_path(r'^find-article/$', auleblog.views.find_by_title),
    re_path(r'^news/(?P<article_id>\d+)/pdf/$', auleblog.views.articleToPdf, name='pdf'),
    re_path(r'^articles/rss/', auleblog.views.NewEntries(), name='new_entry'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^article_details/(?P<slug>[-\w\d]+),(?P<pk>\d+)/$', auleblog.views.ArticleDetailView.as_view(), name='article-details'),
    re_path('^my_form/$', auleblog.views.CommentFormView.as_view(), name='my_form_view_url'),
]