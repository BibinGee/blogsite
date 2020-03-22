from django.contrib import admin
from .models import Link, SideBar, VisitStatistic, DailyVisitStatistic, IPStatistic
from blogsite.custom_site import custom_site
# Register your models here.


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar)
class SidebBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SidebBarAdmin, self).save_model(request, obj, form, change)


@admin.register(VisitStatistic)
class VisitStatisticAdmin(admin.ModelAdmin):
    list_display = ('visit_number', )
    fields = ('visit_number',)


@admin.register(DailyVisitStatistic)
class DailyVisitStatisticAdmin(admin.ModelAdmin):
    list_display = ('daily_visit_number', 'date')
    fields = ('daily_visit_number', 'date')


@admin.register(IPStatistic)
class IPStatisticAdmin(admin.ModelAdmin):
    list_display = ('ip', 'ip_domain', 'created_time')
    fields = ('ip', )
