from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class VentasTokenSerializer(TokenObtainPairSerializer):
    """
    Serializer que valida el login solo para usuarios con perfil de 'ventas'
    o superusuarios.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar datos personalizados al token
        token['username'] = user.username
        token['tipo'] = getattr(user, 'perfilventas', None).tipo if hasattr(user, 'perfilventas') else 'superusuario'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        perfil = getattr(user, 'perfilventas', None)

        # Verificamos permisos
        if not perfil and not user.is_superuser:
            raise serializers.ValidationError("No tienes permisos para acceder (solo usuarios de ventas)")

        if perfil and not perfil.es_ventas_o_superusuario():
            raise serializers.ValidationError("No tienes permisos para acceder (solo usuarios de ventas)")

        # Retornar token y usuario
        data['username'] = user.username
        data['tipo'] = 'superusuario' if user.is_superuser else perfil.tipo
        return data
