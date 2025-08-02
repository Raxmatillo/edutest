import random

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Test, Question, TestResult
from rest_framework.views import APIView, Response, status
from .serializers import (
    TestSerializer, 
    QuestionSerializer, 
    BulkQuestionCreateSerializer, 
    ShuffledQuestionSerializer,
    SubmitAnswerSerializer,
    TestResultSerializer,
)

from django.shortcuts import get_object_or_404

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
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        test = serializer.validated_data.get('test')

        # Foydalanuvchi o‘zining testiga savol qo‘shmoqda — tekshiramiz:
        if test.created_by != self.request.user:
            raise PermissionDenied("Siz ushbu testga savol qo‘sha olmaysiz.")

        serializer.save()



class TeacherQuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise PermissionDenied('Test topilmadi.')

        if test.created_by != self.request.user:
            raise PermissionDenied('Sizga bu testga ruxsat yo‘q.')

        return Question.objects.filter(test=test)

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


class TestQuestionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id, is_active=True)
        except Test.DoesNotExist:
            return Response({"detail": "Bunday test mavjud emas yoki faol emas."}, status=404)

        questions = test.questions.all()

        if test.shuffle_questions:
            questions = list(questions)
            random.shuffle(questions)

        serializer = ShuffledQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=200)


class SubmitTestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'answers': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    additional_properties=openapi.Schema(type=openapi.TYPE_STRING),
                    example={
                        "12": "a",
                        "13": "b",
                        "14": "c"
                    }
                )
            },
            required=['answers']
        )
    )
    def post(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id, is_active=True)
        except Test.DoesNotExist:
            return Response({"detail": "Bunday test mavjud emas yoki faol emas."}, status=404)

        user = request.user

        # Allaqachon bajarganmi
        if TestResult.objects.filter(test=test, student=user).exists():
            return Response({"detail": "Siz bu testni allaqachon ishlagansiz."}, status=400)

        serializer = SubmitAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answers = serializer.validated_data['answers']

        questions = test.questions.all()
        total = questions.count()
        correct = 0

        for question in questions:
            qid = str(question.id)
            if qid in answers and answers[qid] == question.correct:
                correct += 1

        score = round((correct / total) * 100, 2)

        result = TestResult.objects.create(
            test=test,
            student=user,
            score=score,
            total_questions=total,
            correct_answers=correct
        )

        return Response({
            "score": score,
            "correct_answers": correct,
            "total_questions": total,
            "submitted_at": result.submitted_at
        }, status=201)

class TestResultsView(generics.ListAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        test = get_object_or_404(Test, id=test_id, created_by=self.request.user)
        return test.results.all().select_related('student')


class MyResultsView(generics.ListAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestResult.objects.filter(student=self.request.user).order_by('-submitted_at')
