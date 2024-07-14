from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Multimedia(models.Model):
    Nombre = models.CharField(max_length=200)
    Descripcion = models.CharField(max_length=1000)
    Imagen = models.ImageField(upload_to='static/img/videos/', null=True, blank=True)
    categoria = models.BooleanField(default=True)
    Link = models.URLField(default='https://www.youtube.com/')

    def __str__(self) -> str:
        return self.Nombre
    
class UserList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    multimedia = models.ForeignKey(Multimedia, on_delete=models.CASCADE)

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    multimedia = models.ForeignKey(Multimedia, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario por {self.usuario.username} en {self.multimedia.Nombre}'    

from django.db import models

class Respuesta(models.Model):
    comentario = models.ForeignKey(Comentario, related_name='respuestas', on_delete=models.CASCADE, null=True)
    contenido = models.TextField()
    multimedia = models.ForeignKey(Multimedia, related_name='respuestas', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.contenido