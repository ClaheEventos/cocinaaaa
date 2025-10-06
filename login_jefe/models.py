from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):  # Perfil de jefes
    USUARIO_TIPOS = (
        ('jefe', 'Usuario Jefe'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfiljefe')
    tipo = models.CharField(max_length=20, choices=USUARIO_TIPOS, default='jefe')

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"

    def es_jefe_o_superusuario(self):
        """
        Retorna True si el usuario es tipo 'jefe' o es superusuario
        """
        return self.tipo == 'jefe' or self.user.is_superuser