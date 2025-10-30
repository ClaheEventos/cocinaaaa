from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import VentasTokenSerializer

class VentasLoginView(TokenObtainPairView):
    serializer_class = VentasTokenSerializer
