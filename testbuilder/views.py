from rest_framework import generics, permissions
from .models import Test, Question
from rest_framework.views import APIView, Response, status
from .serializers import TestSerializer, QuestionSerializer, BulkQuestionCreateSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create a test detail view
class TestCreateView(generics.CreateAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Create a test list view (only see tests created by the user)
class TestListView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Test.objects.filter(created_by=self.request.user).order_by('-created_at')    

# See only one test by its ID
class TestDetailView(generics.RetrieveAPIView):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Test.objects.filter(created_by=self.request.user)

# add question to a test
class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     test_id = self.kwargs.get('test_id')
    #     test = Test.objects.get(id=test_id, created_by=self.request.user)
    #     serializer.save(test=test)


class BulkQuestionCreateAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=BulkQuestionCreateSerializer,
        operation_description="Bulk question create",
        responses={201: openapi.Response('Successfully created')}
    )
    def post(self, request):
        serializer = BulkQuestionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Savollar muvaffaqiyatli qo‘shildi."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
