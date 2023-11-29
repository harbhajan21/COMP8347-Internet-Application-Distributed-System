from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

class AutoLogoutMiddleware(SessionMiddleware):
    def process_request(self, request):
        # Call parent's process_request method
        super().process_request(request)

        # Reset the session timeout if the user is authenticated
        if request.user.is_authenticated:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)