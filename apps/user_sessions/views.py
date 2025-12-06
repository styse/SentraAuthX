from rest_framework import generics, permissions
from .serializers import SessionSerializer
from .models import Session


class UserSessionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SessionSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        active_only = self.request.query_params.get['active_only']
        qs = Session.objects.filter(user=user)
        
        if active_only == 'true':
            qs = qs.filter(is_active=True)
            
        return qs.order_by("-last_active_at")
