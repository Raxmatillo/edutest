from rest_framework import serializers
from .models import Question, Test

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

class BulkQuestionCreateSerializer(serializers.Serializer):
    questions = QuestionSerializer(many=True)

    def create(self, validated_data):
        questions_data = validated_data['questions']
        return Question.objects.bulk_create([
            Question(**item) for item in questions_data
        ])
