import uuid
from django.db import models


class FeatureFlag(models.Model):
    organization_id = models.UUIDField(db_index=True)
    key = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    rollout_percentage = models.IntegerField(default=100)
    metadata = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feature_flags"
        unique_together = ("organization_id", "key")

    @classmethod
    def is_enabled(cls, organization_id, key: str) -> bool:
        try:
            flag = cls.objects.get(organization_id=organization_id, key=key)
            return flag.enabled
        except cls.DoesNotExist:
            return False
