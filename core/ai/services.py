"""
AI Provider abstraction layer.
Swap implementations without touching business logic.
"""
import time
import hashlib
import json
from abc import ABC, abstractmethod
from typing import Optional


class BaseAIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system: str = "", max_tokens: int = 2000, temperature: float = 0.3) -> str:
        pass


class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, system: str = "", max_tokens: int = 2000, temperature: float = 0.3) -> str:
        import openai
        client = openai.OpenAI(api_key=self.api_key)
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content


class AnthropicProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, system: str = "", max_tokens: int = 2000, temperature: float = 0.3) -> str:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        kwargs = {"model": self.model, "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]}
        if system:
            kwargs["system"] = system
        resp = client.messages.create(**kwargs)
        return resp.content[0].text


class AIRouter:
    """
    Routes task types to the appropriate provider.
    Configure via DB or env vars.
    """
    TASK_ROUTING = {
        "rfp_response": "openai",
        "compliance_check": "anthropic",
        "drawing_analysis": "openai",
        "demand_forecast": "openai",
        "guest_message": "openai",
        "trade_impact": "openai",
        "permit_extract": "openai",
        "maintenance_predict": "openai",
        "route_optimize": "openai",
        "general": "openai",
    }

    @classmethod
    def get_provider(cls, task_type: str) -> BaseAIProvider:
        import os
        provider_name = cls.TASK_ROUTING.get(task_type, "openai")
        if provider_name == "anthropic":
            return AnthropicProvider(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        return OpenAIProvider(api_key=os.environ.get("OPENAI_API_KEY", ""))

    @classmethod
    def generate(
        cls,
        task_type: str,
        prompt: str,
        system: str = "",
        organization_id=None,
        max_tokens: int = 2000,
    ) -> str:
        from core.ai.models import AIRequest
        provider = cls.get_provider(task_type)
        start = time.time()
        try:
            response = provider.generate(prompt=prompt, system=system, max_tokens=max_tokens)
            latency = int((time.time() - start) * 1000)
            AIRequest.objects.create(
                organization_id=organization_id or "00000000-0000-0000-0000-000000000000",
                provider=provider.__class__.__name__,
                prompt=prompt[:2000],
                response=response[:4000],
                latency_ms=latency,
            )
            return response
        except Exception as exc:
            AIRequest.objects.create(
                organization_id=organization_id or "00000000-0000-0000-0000-000000000000",
                provider=provider.__class__.__name__,
                prompt=prompt[:2000],
                error=str(exc),
            )
            raise


class CachedAIRouter(AIRouter):
    """AIRouter with response caching by prompt hash."""

    @classmethod
    def generate(cls, task_type: str, prompt: str, system: str = "", organization_id=None, max_tokens: int = 2000) -> str:
        from django.utils import timezone
        from core.ai.models import ResponseCache
        import datetime

        cache_key = hashlib.sha256(f"{task_type}:{system}:{prompt}".encode()).hexdigest()
        try:
            cached = ResponseCache.objects.get(prompt_hash=cache_key, expires_at__gt=timezone.now())
            return cached.response
        except ResponseCache.DoesNotExist:
            pass

        response = super().generate(task_type, prompt, system, organization_id, max_tokens)
        ResponseCache.objects.update_or_create(
            prompt_hash=cache_key,
            defaults={
                "response": response,
                "expires_at": timezone.now() + datetime.timedelta(hours=24),
            },
        )
        return response
