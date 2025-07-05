from django.urls import path
from .views import TestCreateView, TestListView, TestDetailView, QuestionCreateView, BulkQuestionCreateAPIView

urlpatterns = [
    path('tests/create/', TestCreateView.as_view(), name='test-create'),
    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/<int:pk>/', TestDetailView.as_view(), name='test-detail'),
    path('questions/create/', QuestionCreateView.as_view(), name='question-create'),
    path('questions/bulk-create/', BulkQuestionCreateAPIView.as_view(), name='bulk-question-create'),
]
