from .models import Session
from django.utils import timezone

def create_user_session(user, token_key, request):
    """
    Creates a session record after user login (password or OTP).
    """
    
    ip = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT","")
    
    return Session.object.create(
        user = user,
        token_key = token_key,
        ip_address = ip,
        user_agent = user_agent
    )


def get_client_ip(request):
    """
    Extract client IP address from request.
    """
    
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    
    # Behind a reverse proxy
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    
    # normal
    return request.META.get("REMOTE_ADDR")


def deactivate_session_by_token_key(token_key):
    try:
        session = Session.objects.get(token_key=token_key, is_active=True)
        session.is_active = False
        session.last_active_at = timezone.now()
        session.save()
        
    except Session.DoesNotExist():
        pass
    
    
def deactivate_all_sessions_for_user(user):
    Session.objects.filter(user=user, is_active=True).update(
        is_active=False,
        last_active_at=timezone.now()
    )
    