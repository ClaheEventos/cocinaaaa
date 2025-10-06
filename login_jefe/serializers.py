from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

class JefeTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar datos adicionales al token si querés
        token['username'] = user.username
        token['tipo'] = getattr(user, 'perfiljefe', None).tipo if hasattr(user, 'perfiljefe') else 'superusuario'
        return token

    def validate(self, attrs):
        # Validar usuario y password
        data = super().validate(attrs)

        user = self.user
        perfil = getattr(user, 'perfiljefe', None)

        if not perfil and not user.is_superuser:
            raise serializers.ValidationError("No tienes permisos para acceder")

        if perfil and not perfil.es_jefe_o_superusuario():
            raise serializers.ValidationError("No tienes permisos para acceder")

        return data