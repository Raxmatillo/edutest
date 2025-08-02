from django.urls import path
from .views import RegisterView, MeView, LogoutView, TeacherListView, StudentListView, UserSearchAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('teachers/', TeacherListView.as_view(), name='teacher-list'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('users/search/', UserSearchAPIView.as_view(), name='user-search'),

]