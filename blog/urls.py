from django.conf.urls import url

from . import views
from .views import RSSFeed

app_name = 'blog'

urlpatterns = [
    url(r'^home/$',views.home,name='home'),
    url(r'^time/$',views.current_datetime,name='current_datetime'),
    url(r'^test_time/$',views.test_time,name='test_time'),
    url(r'^detail/(?P<id>\d+)/$',views.detail,name='detail'),
    url(r'^archives/$',views.archives,name='archives'),
    url(r'^about_me/$',views.about_me,name='about_me'),
    url(r'^search_tag/(?P<tag>\w+)/$',views.search_tag,name='search_tag'),
    url(r'^search/$',views.blog_search,name='search'),
    url(r'^feed/',RSSFeed(),name="RSS"),
]
