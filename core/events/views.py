from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DomainEvent


class DomainEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainEvent
        fields = ["id", "event_type", "aggregate_type", "aggregate_id", "payload", "created_at", "processed", "error"]
        read_only_fields = ["id", "created_at"]


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DomainEventSerializer

    def get_queryset(self):
        qs = DomainEvent.objects.filter(organization_id=self.request.user.organization_id)
        event_type = self.request.query_params.get("event_type")
        if event_type:
            qs = qs.filter(event_type=event_type)
        return qs.order_by("-created_at")[:200]

    @action(detail=False, methods=["get"])
    def types(self, request):
        from .models import EVENT_TYPES
        return Response(EVENT_TYPES)
