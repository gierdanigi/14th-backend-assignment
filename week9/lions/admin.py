from django.contrib import admin
from .models import Lion, Task, LionProfile, Tag


@admin.register(Lion)
class LionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'track', 'created_at']
    list_filter = ['track']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'lion', 'title', 'completed', 'created_at']
    list_filter = ['completed', 'lion']
    search_fields = ['title', 'lion__name']


@admin.register(LionProfile)
class LionProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'lion', 'github_url', 'created_at']
    search_fields = ['lion__name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
