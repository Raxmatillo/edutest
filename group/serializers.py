from rest_framework import serializers
from .models import Group, GroupJoinRequest
from core.models import User  # user modelini import qilish

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'teacher', 'students', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'teacher']


class GroupJoinRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = GroupJoinRequest
        fields = ['id', 'group', 'student', 'status', 'created_at', 'student_name']
        read_only_fields = ['id', 'created_at', 'status', 'student_name']

    def get_student_name(self, obj):
        return obj.student.full_name


class InviteStudentsSerializer(serializers.Serializer):
    usernames = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
