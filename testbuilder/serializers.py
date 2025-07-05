import random

from rest_framework import serializers
from .models import Question, Test, TestResult

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = [
            'id',
            'title',
            'subject',
            'description',
            'test_type',
            'test_limit',
            'shuffle_questions',
            'is_active',
            'expire_at',
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)



class QuestionSerializer(serializers.ModelSerializer):
    correct = serializers.ChoiceField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])

    class Meta:
        model = Question
        fields = [
            'id',
            'test',
            'question_title',
            'image',
            'answer_a',
            'answer_b',
            'answer_c',
            'answer_d',
            'correct',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']




class ShuffledQuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id',
            'question_title',
            'image',
            'answers',
        ]

    def get_answers(self, obj):
        # Original variants
        options = [
            {'label': 'A', 'value': obj.answer_a, 'key': 'a'},
            {'label': 'B', 'value': obj.answer_b, 'key': 'b'},
            {'label': 'C', 'value': obj.answer_c, 'key': 'c'},
            {'label': 'D', 'value': obj.answer_d, 'key': 'd'},
        ]

        # Faqat mavjud variantlar bo‘yicha filter (ixtiyoriy)
        options = [opt for opt in options if opt['value']]

        random.shuffle(options)
        return options

class TestResultSerializer(serializers.ModelSerializer):
    test_title = serializers.CharField(source='test.title', read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'test', 'test_title', 'score', 'correct_answers', 'total_questions', 'submitted_at']


class BulkQuestionCreateSerializer(serializers.Serializer):
    questions = QuestionSerializer(many=True)

    def create(self, validated_data):
        questions_data = validated_data['questions']
        return Question.objects.bulk_create([
            Question(**item) for item in questions_data
        ])


class SubmitAnswerSerializer(serializers.Serializer):
    answers = serializers.DictField(
        child=serializers.ChoiceField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])
    )
