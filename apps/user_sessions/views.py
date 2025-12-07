from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import SessionSerializer
from .models import Session
from knox.models import AuthToken

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


class UserSessionDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SessionSerializer
    lookup_url_kwarg = "session_id"
    
    def get_queryset(self):
        return Session.objects.filter(user = self.request.user)
    
    def delete(self, request, *args, **kwargs):

        session_id = kwargs.get("session_id")
        session = Session.objects.filter(id = session_id, user = request.user).first()
        
        if not session:
            return Response({"detail" : "Session not found."}, status= status.HTTP_404_NOT_FOUND)
        
        try:
            AuthToken.objects.get(token_key=session.token_key[:8]).delete()
        except AuthToken.DoesNotExist:
            pass

        session.is_active = False
        session.save()
        
        return Response({"detail": "Session revoked successfully."}, status= status.HTTP_200_OK)