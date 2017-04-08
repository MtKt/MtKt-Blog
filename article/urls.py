from django.conf.urls import url
from . import views

app_name = 'article'
urlpatterns = [
                url(r'^$', views.IndexView.as_view(), name = 'index'),
                url(r'^(?P<slug>[-\w\d]+),(?P<article_id>\d+)/$', views.ArticleView.as_view(), name='article'),
                url(r'^about/$', views.AboutView.as_view(), name = 'about' ),
                url(r'^timeline/$', views.TimeLine.as_view(), name = 'timeline'),
                url(r'^category/$', views.CategoryView.as_view(),name = 'category'),
                url(r'^cyuuni/$', views.cyuuni_detail, name = 'cyuuni'),
                #url(r'^cyuuni/(?P<cyuuni_id>\d+)/$', views.CyuuniDetail.as_view(), name = 'cyuuni_s'),
              ]