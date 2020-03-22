"""blogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf.urls import url
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings

from comment.views import CommentView
from .custom_site import custom_site

from blog.views import IndexView, CategoryView, TagView, PostDetailView, SearchView
from config.views import LinkView
from blog.sitemap import PostSitemap
from django.contrib.sitemaps import views as sitemap_views


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url(r'^links/$', LinkView.as_view(), name='links'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', admin.site.urls, name='super-admin'),
    # url(r'^admin/', custom_site.urls, name='admin'),
    url(r'^sitemap.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}})
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^silk/', include('silk.urls', namespace='silk'))
#     ] + urlpatterns
