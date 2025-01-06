from rest_framework.throttling import UserRateThrottle
from datetime import datetime, timedelta


class CustomRateThrottle(UserRateThrottle):
    cache = {}

    def allow_request(self, request, view):
        user_ip = self.get_ident(request)
        now = datetime.now()

        if user_ip not in self.cache:
            self.cache[user_ip] = [now]
            return True

        # Clean up old requests
        self.cache[user_ip] = [
            timestamp
            for timestamp in self.cache[user_ip]
            if timestamp > now - timedelta(seconds=60)
        ]

        # Allow up to 5 requests per minute
        if len(self.cache[user_ip]) < 50:
            self.cache[user_ip].append(now)
            return True
        return False

    def wait(self):
        return 60  # Wait for 60 sec before allowing new requests
