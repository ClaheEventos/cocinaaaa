from django.db import models
from django.contrib.auth.models import User

class PerfilVentas(models.Model):  # Perfil de usuarios de ventas
    USUARIO_TIPOS = (
        ('ventas', 'Usuario de Ventas'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfilventas')
    tipo = models.CharField(max_length=20, choices=USUARIO_TIPOS, default='ventas')

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"

    def es_ventas_o_superusuario(self):
        """
        Retorna True si el usuario es tipo 'ventas' o es superusuario
        """
        return self.tipo == 'ventas' or self.user.is_superuser