from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import JefeTokenSerializer

class JefeTokenObtainView(TokenObtainPairView):
    serializer_class = JefeTokenSerializer