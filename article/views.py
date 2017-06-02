from collections import defaultdict
from math import ceil
from os.path import join
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Article,Cyuuni,Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, TemplateView

class BaseMixIn(object):
    def get_context_data(self,**kwargs):
        context = super(BaseMixIn,self).get_context_data(**kwargs)
        context['cyuuni_byou'] = Cyuuni.objects.filter(status=0).order_by('?').first()
        return context

class IndexView(BaseMixIn,ListView):
    model = Article
    template_name = 'article/index_base.html'
    context_object_name = 'article_list'
    paginate_by = 5

    def get_queryset(self):
        article_list = Article.objects.filter(article_status=0).order_by("-pub_date")
        return article_list

class ArticleView(BaseMixIn,DetailView):
    template_name = 'article/article.html'
    model = Article
    context_object_name = 'article'
    slug_field = 'slug'
    pk_url_kwarg = 'article_id'

class TimeLine(BaseMixIn,TemplateView):
    template_name = 'article/timeline.html'
    def get_context_data(self,**kwargs):
        model = Article
        article_list = Article.objects.filter(article_status=0).order_by("-pub_date")
        year_all = defaultdict(list)
        for article in article_list:
            year = article.pub_date.year
            year_all[year].append(article)
        year_all=sorted(year_all.items(),reverse=True)
        context = super(TimeLine,self).get_context_data(**kwargs)
        context['year_all'] = year_all
        context['article_list'] = article_list
        return context

class CategoryView(BaseMixIn,DetailView):
    model = Category    
    template_name = 'article/category.html'
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'

    def get_object(self, queryset=None):
        obj = super(CategoryView, self).get_object()
        obj.article = obj.article_set.all()
        return obj 

class AboutView(BaseMixIn,TemplateView):
    template_name = 'article/about.html'

def cyuuni_detail(request, cyuuni_id):
    if cyuuni_id == 'rand':
        cyuuni_byou = Cyuuni.objects.filter(status=0).order_by('?').first()
    else:
        cyuuni_byou = Cyuuni.objects.filter(status=0).get(id=cyuuni_id)
    args = {'cyuuni_byou':cyuuni_byou}
    return render(request, 'article/cyuuni.html', args)    