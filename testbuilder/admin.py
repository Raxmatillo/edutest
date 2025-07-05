from django.contrib import admin
from .models import Test, Question, TestResult


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subject', 'test_type', 'created_by', 'is_active', 'expire_at', 'created_at')
    list_filter = ('test_type', 'is_active', 'created_at')
    search_fields = ('title', 'subject', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'question_title', 'correct', 'created_at')
    list_filter = ('test',)
    search_fields = ('question_title',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'student', 'score', 'correct_answers', 'total_questions', 'submitted_at')
    list_filter = ('test', 'submitted_at')
    search_fields = ('student__username', 'test__title')
    readonly_fields = ('submitted_at',)
