from django.conf import settings
from django.contrib.sessions.middleware import (
    SessionMiddleware as DjangoSessionMiddleware,
)


class SessionMiddleware(DjangoSessionMiddleware):
    """
    Middleware that provides ip and user_agent to the session store.
    """
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        
        request.session = self.SessionStore(
            ip=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            session_key=session_key
        )
