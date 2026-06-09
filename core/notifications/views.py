from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "channel", "recipient", "subject", "message", "status", "created_at", "sent_at"]
        read_only_fields = ["id", "created_at", "sent_at"]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ["id", "event_type", "channels", "is_enabled"]


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(
            organization_id=self.request.user.organization_id
        ).order_by("-created_at")[:100]


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationPreferenceSerializer

    def get_queryset(self):
        return NotificationPreference.objects.filter(user_id=self.request.user.id)
