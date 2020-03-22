from datetime import date

from django.core.cache import cache
from django.shortcuts import render, get_object_or_404

from comment.forms import CommentForm
from comment.models import Comment
from config.models import SideBar, VisitStatistic, DailyVisitStatistic, IPStatistic
from .models import Post, Tag, Category
from django.views.generic import DetailView, ListView
from django.db.models import Q, F

# Create your views here.

"""
ListView流程：
  1. 在Get请求中，首先会调用get_queryset方法拿到数据源
  2. 接着调用get_context_data方法拿到需要渲染到模板中的数
        a. 在get_context_data中首先调用get_paginate_by拿到每页数据
        b. 接着调用get_context_object_name拿到要渲染到模板中的这个queryset名称
        c. 然后调用paginate_queryset进行分页处理
        d. 最后拿到数据转为dict并返回
  3. 调用render_to_response渲染数据到每一页中
        a. 在render_to_response中调用get_template_name拿到模板名
        b. 然后把request, context, template_name等传递到模板中   
"""


class CommonViewMixin:
    # get_context_data是MultipleObjectMixin类中的方法，这里重写方法，在下面IndexView中直接引用
    # 因list.html需要渲染sidebars和navs，categories，这部分就独立抽取出来实现
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VisitStatistic.objects.filter(id=1).update(visit_number=F('visit_number') + 1)
        DailyVisitStatistic.statistic()
        IPStatistic.AddIPAddr(self.request)

        # 用于渲染base.html中的分类和侧边栏
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    # 控制分页数量
    paginate_by = 3
    # 与list.html中的post_list关联
    context_object_name = 'post_list'
    # 关联模板
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        # 在list.html也中关联category
        context.update({
            'category': category,
        })
        return context

    # 重写get_querset
    def get_queryset(self):
        queryset = super().get_queryset()
        # url路由中关联category_id
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Category, pk=tag_id)
        # 在list.html中关联tag
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # url路由中关联tag_id
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        # print(keyword)
        if not keyword:
            return queryset
        # print(queryset.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)))
        return queryset.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))


class PostDetailView(CommonViewMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1, uv=F('uv')+1)
        self.handle_visited()
        return response

    """
    文章访问统计，使用系统生成的用户id，并将器放置在用户的cookie中来标记用户。
    """
    def handle_visited(self):
        increase_pv = False
        increase_uv = False

        uid = self.request.uid

        pv_key = 'pv:%s:%s' % (uid, self.request.uid)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        print(f'pv_key:{pv_key}, uv_key:{uv_key}')

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60) # 1 分钟有效

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60) # 1 天有效

        if increase_uv and increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'comment_form': CommentForm,
                'comment_list': Comment.get_by_target(self.request.path),
            }
        )
        return context


