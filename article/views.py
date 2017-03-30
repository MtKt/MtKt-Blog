from collections import defaultdict
from math import ceil
from os.path import join
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q


class IndexView(ListView):
    model = Article
    template_name = 'article/index_base.html'
    context_object_name = 'article_list'
    paginate_by = 5
    def get_queryset(self):
        article_list = Article.objects.filter(article_status=0).order_by("-pub_date")
        return article_list

def ArticleView(request, slug, article_id):
    args = {'article': get_object_or_404(Article, pk=article_id)}
    return render(request, 'article/article.html', args)

class TimeLine(ListView):
    model = Article
    template_name = "article/time.html"
    context_object_name = "article_list"
    paginate_by = 25

    def get_queryset(self):
        article_list = Article.objects.set_all()
        return article_list

class CategoryView(ListView):
    template_name = 'article/category.html'
    context_object_name = 'article_list'
    paginate_by = 25
    def get_queryset(self):
        category = self.kwargs.get('category', '')
        try:
            article_list = Category.objects.get(name=category).article_set.all()
        except Category.DoesNotExist:
            logger.error(u'[CategoryView]此分类不存在:[%s]' % category)
            raise Http404
        return article_list

class AboutView(TemplateView):
    template_name = 'article/about.html'