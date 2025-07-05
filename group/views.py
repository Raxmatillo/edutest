from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Group, GroupJoinRequest
from .serializers import GroupSerializer, GroupJoinRequestSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(teacher=user)

    @action(detail=True, methods=['post'], url_path='invite-students')
    def invite_students(self, request, pk=None):
        group = self.get_object()
        serializer = InviteStudentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usernames = serializer.validated_data['usernames']

        invited = []
        errors = []

        for username in usernames:
            try:
                student = User.objects.get(username=username, role='student')
                join_request, created = GroupJoinRequest.objects.get_or_create(
                    group=group, student=student
                )
                if created:
                    invited.append(student.username)
                else:
                    errors.append(f"{username} already invited.")
            except User.DoesNotExist:
                errors.append(f"{username} not found.")

        return Response({
            "invited": invited,
            "errors": errors
        }, status=status.HTTP_201_CREATED)

class GroupJoinRequestViewSet(viewsets.ModelViewSet):
    queryset = GroupJoinRequest.objects.all()
    serializer_class = GroupJoinRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroupJoinRequest.objects.filter(student=self.request.user, status='pending')

    @action(detail=True, methods=['post'], url_path='accept')
    def accept(self, request, pk=None):
        join_request = self.get_object()
        if join_request.student != request.user:
            return Response({"detail": "Ruxsat yo'q."}, status=403)

        join_request.status = 'accepted'
        join_request.save()
        join_request.group.students.add(request.user)

        return Response({"detail": "Guruhga muvaffaqiyatli qo‘shildingiz."})
