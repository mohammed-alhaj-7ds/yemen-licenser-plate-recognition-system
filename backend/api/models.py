from __future__ import annotations

import uuid

from django.db import models


class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, help_text="Name for identifying the API key")
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} - {str(self.key)[:8]}..."

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

