from django.contrib import admin
from .models import Group, GroupJoinRequest


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'teacher', 'created_at', 'updated_at')
    list_filter = ('name', 'teacher', 'created_at', 'updated_at')
    search_fields = ('name', 'teacher__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(GroupJoinRequest)
class GroupJoinRequestAdmin(admin.ModelAdmin):
    list_display = ('group', 'student', 'status', 'created_at')
    list_filter = ('group', 'status', 'created_at')
    search_fields = ('group__name', 'student__username')
    readonly_fields = ('created_at', )