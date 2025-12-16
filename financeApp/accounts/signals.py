"""Signal handlers for the accounts app."""

from __future__ import annotations

from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from .cache_utils import clear_user_runtime_state


@receiver(user_logged_out)
def clear_cache_on_logout(sender, request, user, **kwargs):
    """Clear cached data and session values whenever a user logs out."""

    session = getattr(request, "session", None)
    clear_user_runtime_state(user, session=session)
