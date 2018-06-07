from django import template
from django.db.models import Count
from ..models import Article, Comment

register = template.Library()


@register.simple_tag
def total_posts():
    return Article.objects.count()

@register.simple_tag
def total_comments():
    return Comment.objects.count()

@register.simple_tag
def get_most_commented_posts(count=2):
    return Article.objects.annotate(total_comments=Count('comment')).order_by('-total_comments')[:count]

@register.simple_tag
def get_most_viewed_posts():
    return Article.objects.all().order_by('-counter')[:3]