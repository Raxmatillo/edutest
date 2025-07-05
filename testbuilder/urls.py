from django.urls import path
from .views import (
    TestCreateView, 
    TestListView, 
    TestDetailView, 
    QuestionCreateView, 
    BulkQuestionCreateAPIView,
    TestQuestionListView,
    SubmitTestView,
    MyResultsView,
    TestResultsView
)

urlpatterns = [
    path('tests/create/', TestCreateView.as_view(), name='test-create'),
    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/<int:pk>/', TestDetailView.as_view(), name='test-detail'),
    path('questions/create/', QuestionCreateView.as_view(), name='question-create'),
    path('questions/bulk-create/', BulkQuestionCreateAPIView.as_view(), name='bulk-question-create'),
    path('tests/<int:test_id>/questions/', TestQuestionListView.as_view(), name='test-questions'),
    path('tests/<int:test_id>/submit/', SubmitTestView.as_view(), name='submit-test'),
    path('tests/<int:test_id>/results/', TestResultsView.as_view(), name='test-results'),
    path('my-results/', MyResultsView.as_view(), name='my-results'),

]
