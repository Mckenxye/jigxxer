from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
# Create your models here.


#clase para los datos de los negocios

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Administrador', 'Administrador'),
        ('Cliente', 'Cliente'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='Cliente')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Cambiar related_name para evitar conflicto
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Cambiar related_name para evitar conflicto
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


User = get_user_model()

class Negocio(models.Model):
    id_negocio = models.AutoField(primary_key=True)
    nombre_negocio = models.CharField(max_length=50, verbose_name='Nombre del Negocio')
    telefono = models.CharField(max_length=50, verbose_name='Teléfono')
    numero_de_local = models.CharField(max_length=50, verbose_name='Número de Local')
    usuario_administrador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='negocios', verbose_name='Usuario Administrador')
    
    def __str__(self):#funcion para mostrar mas informacion en la pagina de administracion
        descripcion =  (f"Negocio: {self.nombre_negocio}--Telfono: {self.telefono}--Local: {self.numero_de_local} " )
        return descripcion
    
# clase para la tabla de venta y recoleccion de informacion de producto 
class Venta(models.Model):
    Id_venta = models.AutoField(primary_key=True)#autoincreentable key 
    imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen')#imagen
    producto = models.CharField(max_length=50, verbose_name='Producto')#varchar
    precio = models.IntegerField(verbose_name="Precio")#int
    cantidad = models.IntegerField(verbose_name="Cantidad")#int
    Id_negocio = models.ForeignKey('Negocio', on_delete=models.CASCADE, verbose_name="Id_negocio")#foranea key
    descripcion = models.CharField(max_length=1000, verbose_name='descripcion')#varchar
    categoria = models.CharField(max_length=1000, verbose_name='categoria')#varchar
    
    def __str__(self):#funcion para mostrar mas informacion en la pagina de administracion
        descripcion =  (f"Producto: {self.producto}--Precio: {self.precio}--Cantidad: {self.cantidad}" )
        return descripcion
    def eliminar(self, using = None, keep_parents=False):
        self.imagen.storage.delete(self.imagen)
        super().delete()
    
