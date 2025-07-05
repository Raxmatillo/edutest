from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
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

    @action(detail=True, methods=['post'])
    def invite_student(self, request, pk=None):
        group = self.get_object()
        username = request.data.get('username')

        if not username:
            return Response({"detail": "Username required."}, status=400)

        try:
            student = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=404)

        join_request, created = GroupJoinRequest.objects.get_or_create(
            group=group, student=student
        )

        if not created:
            return Response({"detail": "So‘rov allaqachon mavjud."}, status=400)

        # TODO: Botga yuborish yoki notifikatsiya
        return Response(GroupJoinRequestSerializer(join_request).data)
