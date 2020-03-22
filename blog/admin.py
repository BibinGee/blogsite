from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from blogsite.custom_site import custom_site
from blogsite.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry
# Register your models here.


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']


class PostInline(admin.TabularInline):
    fields = ('title', 'content')
    extra = 1
    model = Post


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    inlines = [PostInline]  # 与文章类进行内联

    def post_count(self, obj):      # 自定义函数，用于显示文章数量
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    "自定义过滤器，只展示当前用户"

    title = "分类过滤器"
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm  # 引入自定义表格，与字段desc关联, 使用多行显示
    list_display = ['title', 'category', 'status', 'created_time', 'owner', 'operator', 'pv', 'uv']
    list_display_links = []

    list_filter = [CategoryOwnerFilter]      # 过滤字段
    search_fields = ['title', 'category__name']     # 配置搜索字段

    # actions_on_top = True
    actions_on_bottom = True

    # save_on_top = True

    exclude = ['owner']

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    # fieldsets 用户控制布局，格式是两个元素的tuple的list，如：
    # fieldsets = (
    #     (名称， {内容}),
    #     (名称， {内容}),
    #   )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'title_image'),
                'desc',
            ),
        }),
        ('内容', {
            'fields': (
                'content',
            ),
        }),
        ('额外信息', {
            # 'classes': ('wide', ),
            'fields': ('status', 'category', 'tag',),

        })
    )

    # filter_horizontal = ('tag', )   # 设置字段横向显示

    # filter_vertical = ('tag', )     # 设置字段垂直显示

    def operator(self, obj):    # 自定义函数， 用于显示用户编辑状态
        return format_html(
            '<a href="{}">编辑</a>', reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

"""    class Media:
        css = {
            'all': ('https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',),
        }

        js = ('https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js', )"""