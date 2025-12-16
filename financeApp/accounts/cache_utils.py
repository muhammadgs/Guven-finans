"""Utility helpers for clearing user-specific cache and session data."""

from __future__ import annotations

from typing import Iterable, Optional

from django.contrib.auth import get_user_model
from django.core.cache import cache

UserModel = get_user_model()

# Cache and session keys that should be cleared when the user signs out or the tab closes.
DEFAULT_CACHE_KEY_TEMPLATES: tuple[str, ...] = (
    "user:{user_id}:profile",
    "user:{user_id}:permissions",
    "user:{user_id}:dashboard",
)

SESSION_KEYS_TO_CLEAR: tuple[str, ...] = (
    "dashboard_data",
    "recent_activity",
    "permissions_cache",
)


def _build_user_cache_keys(user: UserModel, templates: Iterable[str]) -> list[str]:
    user_identifier = getattr(user, "pk", None) or getattr(user, "id", None) or user.get_username()
    return [template.format(user_id=user_identifier) for template in templates]


def clear_user_runtime_state(
    user: Optional[UserModel],
    session=None,
    cache_key_templates: Iterable[str] = DEFAULT_CACHE_KEY_TEMPLATES,
    session_keys: Iterable[str] = SESSION_KEYS_TO_CLEAR,
) -> None:
    """Remove cached and session data for a user.

    Args:
        user: The authenticated user whose data should be cleared.
        session: Optional session object to clear.
        cache_key_templates: Cache key templates containing ``{user_id}`` placeholder.
        session_keys: Session keys that should be removed when a session is supplied.
    """

    if not user:
        return

    cache_keys = _build_user_cache_keys(user, cache_key_templates)
    cache.delete_many(cache_keys)

    if session is not None:
        for key in session_keys:
            session.pop(key, None)
        session.modified = True
