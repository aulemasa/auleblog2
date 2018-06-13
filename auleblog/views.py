#coding: utf-8

from django.shortcuts import render
from .models import Category, Article, Comment
from .calendar import WorkoutCalendar
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import date
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.utils.safestring import mark_safe
from django.conf import settings
from weasyprint import HTML, CSS
from django.template import Context
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.syndication.views import Feed
# Create your views here.
@csrf_protect
def articlesViews(request):
    article_all = Article.objects.all().order_by('-id')
    category_all_in_view = Category.objects.all()

    paginator = Paginator(article_all, 10)
    page = request.GET.get('page')
    article_all_pagination = paginator.get_page(page)

    arg = {}

    year = date.today().year
    month = date.today().month
    start_value = 0
    previous_month = request.GET.get('pm')

    try:
        previous_month = previous_month
    except ValueError:
        previous_month = None
    current_month = request.GET.get('am')
    try:
        current_month = current_month
    except ValueError:
        current_month = None

    if previous_month != None:
        ny = month - int(previous_month)
        if ny <= 12 and ny >= 1:
            start_value = start_value + int(previous_month)
            my_workouts = Article.objects.order_by('date_pub').filter(date_pub__year=year, date_pub__month=ny)
            view_calendar = WorkoutCalendar(my_workouts).formatmonth(year, ny)
            return render(request, 'blog/articles.html', {'article_all_pagination': article_all_pagination, 'arg': arg, 'view_calendar': mark_safe(view_calendar),
                                                          'previous_month': previous_month,
                                                          'start_value': start_value,
                                                          'category_all_in_view': category_all_in_view})
        elif current_month != None:
            return render(request, 'blog/articles.html', {'article_all_pagination': article_all_pagination, 'arg': arg, 'view_calendar': mark_safe(view_calendar),
                                                          'category_all_in_view': category_all_in_view})
        else:
            my_workouts = Article.objects.order_by('date_pub').filter(date_pub__year=year, date_pub__month=month)
            view_calendar = WorkoutCalendar(my_workouts).formatmonth(year, month)
    else:
        my_workouts = Article.objects.order_by('date_pub').filter(date_pub__year=year, date_pub__month=month)
        view_calendar = WorkoutCalendar(my_workouts).formatmonth(year, month)

    return render(request, 'blog/articles.html', {'article_all_pagination': article_all_pagination, 'arg': arg, 'view_calendar': mark_safe(view_calendar),
                                                  'category_all_in_view': category_all_in_view})


def categoryViews(request, category_id):
    choose_category = Article.objects.filter(category_article_id=category_id).order_by('-date_pub')
    all_categories = Category.objects.get(id=category_id)
    return render(request, 'blog/categoryviewhtml.html', {'choose_category': choose_category,
                                                   'all_categories': all_categories})


def articleViews(request, url_title, article_id):
    single_article = Article.objects.get(id=article_id)
    try:
        next = single_article.get_next_by_date_pub()
    except Article.DoesNotExist:
        next = None
    try:
        prev = single_article.get_previous_by_date_pub()
    except Article.DoesNotExist:
        prev = None

    art2 = Article.objects.filter(id=article_id)
    counter_adder = single_article.counter + 1
    art2.update(counter=counter_adder)

    comment = Comment.objects.filter(post=article_id)

    data = {'post': single_article.id}
    form = CommentForm(initial=data)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('article', kwargs={'url_title': url_title,
                                                                   'article_id': single_article.id}))

    return render(request, 'blog/article.html', {'art': single_article, 'next': next, 'prev': prev,
                                                 'comment': comment, 'form': form})


def find_by_title(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    searching_title = Article.objects.filter(title__contains=search_text)

    return render(request, 'ajax_search.html', {'searching_title': searching_title})


def articleToPdf(request, article_id):
    single_article = Article.objects.get(id=article_id)
    html_template = get_template('pdf.html')

    context = {'single_article': single_article}

    rendered_html = html_template.render(context)

    pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(settings.PDF_ROOT + '/css/pdf.css')])

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="report.pdf"'

    return http_response


class NewEntries(Feed):
    title = "Message from  Aule Blog"
    link = "/"

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:150]


def custom_404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def custom_500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
