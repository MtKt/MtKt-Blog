from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
                url(r'^$', views.IndexView.as_view(), name = 'index'),
                url(r'^(?P<slug>[-\w\d]+),(?P<article_id>\d+)/$', views.ArticleView, name='article'),
                url(r'^about/$', views.AboutView.as_view(), name = 'about' ),
                url(r'^timeline/$', views.TimeLine.as_view(), name = 'timeline'),
                url(r'^category/(?P<category>\w+)/$', views.CategoryView.as_view(), name = 'category')
                ]
