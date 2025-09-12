from django.db import models

class Cliente(models.Model):
    dni = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    fecha_evento = models.DateField()
    salon = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre} - {self.dni}"
    
class Telefono(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='telefonos')
    numero1 = models.CharField(max_length=20)
    numero2 = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.numero1} / {self.numero2} ({self.cliente.nombre})"

class Isla(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='islas')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"
    
class IslaPremium(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='islas_premium')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"
    

class PlatoPrincipal(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class PlatoInfantil(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class EleccionPlatos(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='eleccion_platos')
    plato_principal = models.ForeignKey(PlatoPrincipal, on_delete=models.SET_NULL, null=True)
    plato_infantil = models.ForeignKey(PlatoInfantil, on_delete=models.SET_NULL, null=True, blank=True)
    aclaraciones_alimentarias = models.TextField(blank=True)

    def __str__(self):
        return f"Elección de platos de {self.cliente.nombre}"
class Eleccion_Platos(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='elecciones')
    plato_principal = models.TextField(null=True, blank=True)
    plato_infantil = models.TextField(null=True, blank=True)
    aclaraciones_alimentarias = models.TextField(null=True, blank=True)
    
    # Cantidades de personas
    num_adultos = models.PositiveIntegerField(null=True, blank=True)
    num_ninos = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.plato_principal}"    
class Postre(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='postres')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"

class MesaDulcePremium(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mesa_dulce_premium')
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"
    
class Extra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='extras')
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"
    
class Show(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='shows')
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"
    
class EleccionFinDeFiesta(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='fin_de_fiesta')
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"
   
class Cantidades(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cantidades')
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.cantidad} personas"


class BarraTragos(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE, related_name="barra_tragos")
    duracion = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.duracion} - {self.cliente.nombre}"

class EleccionRecepcion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='recepcion')
    item = models.CharField(max_length=200)  # nombre del ítem
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.item} - {self.cantidad} personas ({self.cliente.nombre})"
    
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    USUARIO_TIPOS = (
        ('intermedio', 'Usuario Intermedio'),
        ('limitado', 'Usuario Limitado'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=USUARIO_TIPOS, default='limitado')

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfilusuario.save()