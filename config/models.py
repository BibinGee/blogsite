import json

import requests
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import F
from django.template.loader import render_to_string
from django.utils import timezone


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1,6), range(1,6)), verbose_name="权重", help_text="权重高展示靠前")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "友链"

    def __str__(self):
        return self.title


class SideBar(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '展示'),
        (STATUS_DELETE, '隐藏'),
    )

    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMENT, '最近评论'),
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name="展示类型")
    content = models.TextField(max_length=500, blank=True, verbose_name="内容", help_text="如果设置的不是HTML，可为空")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    @property
    def content_html(self):
        from blog.models import Post
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            # print(Post.latest_posts())
            context = {
                'posts': Post.latest_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': Post.hot_post()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_COMMENT:
            # 按时间排列评论
            context = {
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL).order_by('-created_time')[:3]
            }
            result = render_to_string('config/blocks/sidebar_comments.html', context)

        return result


class VisitStatistic(models.Model):
    visit_number = models.PositiveIntegerField(verbose_name='访问总数', default=0)

    def __str__(self):
        return '访问总数'

    class Meta:
        verbose_name = '访问总数'


class IPStatistic(models.Model):
    ip = models.CharField(max_length=30, verbose_name='用户访问IP')
    ip_domain = models.CharField(max_length=200, verbose_name='IP归属地')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="访问时间")

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = '用户访问IP'

    @classmethod
    def AddIPAddr(cls, request):
        # 记录访问ip和每个ip的次数
        if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
            client_ip = request.META['HTTP_X_FORWARDED_FOR']
            client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
        else:
            client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip
        # print(client_ip)
        ip_domain = cls.get_ip_domain(client_ip)
        cls.objects.create(ip=client_ip, ip_domain=ip_domain)

    @classmethod
    def get_ip_domain(cls, user_ip):
        url = f'http://freeapi.ipip.net/{user_ip}'
        try:
            respone = requests.get(url)
            ip_location = respone.text
            ip_domain = json.loads(ip_location)
        except Exception as e:
            print(e)
            return "unknown domain"
            # ip_domain = None
        else:
            if type(ip_domain) is list:
                print(ip_domain)
                return ip_domain
            else:
                return "unknown domain"


class DailyVisitStatistic(models.Model):
    daily_visit_number = models.PositiveIntegerField(verbose_name='每天访问量', default=0)
    date = models.DateField(verbose_name='日期', default=timezone.now)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = '每天访问量'

    @classmethod
    def statistic(cls):
        date = timezone.now().date()
        obj = cls.objects.filter(date=date)
        if obj:
            obj.update(daily_visit_number=F('daily_visit_number') + 1)
        else:
            cls.objects.create(date=date, daily_visit_number=1)
