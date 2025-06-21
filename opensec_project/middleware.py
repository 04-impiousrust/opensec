import time
from django.conf import settings
from django.http import HttpResponse


class RateLimitMiddleware:
    """Simple in-memory IP-based rate limiting middleware."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.history = {}
        self.limit = getattr(settings, "RATE_LIMIT_REQUESTS", 60)
        self.window = getattr(settings, "RATE_LIMIT_WINDOW", 60)

        try:
            self.limit = int(self.limit)
            self.window = int(self.window)
        except (TypeError, ValueError) as exc:
            raise ValueError("RATE_LIMIT_REQUESTS and RATE_LIMIT_WINDOW must be integers") from exc

        if self.limit <= 0 or self.window <= 0:
            raise ValueError("RATE_LIMIT_REQUESTS and RATE_LIMIT_WINDOW must be positive")

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "")
        now = time.time()
        timestamps = self.history.get(ip, [])
        # remove expired timestamps
        timestamps = [t for t in timestamps if now - t < self.window]
        if len(timestamps) >= self.limit:
            return HttpResponse("Too Many Requests", status=429)
        timestamps.append(now)
        self.history[ip] = timestamps
        return self.get_response(request)
