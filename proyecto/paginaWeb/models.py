from django.db import models
from django.contrib.auth.models import User 
from geopy.distance import geodesic

# Create your models here.


#Modelo de mascotas  
class Mascota(models.Model):
    id = models.AutoField(primary_key=True)
    raza = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    tamaño = models.CharField(max_length=100)
    descripcion = models.TextField(default='Sin descripcion')
    estado = models.CharField(max_length=10, default='Perdido')
    fotografia = models.ImageField(upload_to='mascotas/', blank=True, null=True)
    latitud = models.FloatField(default=0,blank=True, null=True)
    longitud = models.FloatField(default=0,blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateField()
    genero=models.CharField(max_length=10,default='Desconocido')
    contacto=models.CharField(max_length=100,default='Desconocido')
    
    def __str__(self):
        return self.especie

    
    def registrarMascota(self):
        self.save()
        return f"Mascota {self.especie}-{self.raza} registrada con exito."
    
    def eliminarMascota(self):
        self.delete()
        return f"Mascota {self.especie}-{self.raza} eleiminada con exito."
    
    def actualizarMascota(self,**kwargs):
        for key, value in kwargs.items():
            if hasattr(self,key):
                setattr(self,key,value)
        self.save()
        return f"Mascota {self.especie}-{self.raza if self.raza else 'Sin raza'} actualizada correctamente"
    
    def obtenerDetalles(self):
        return{
            "ID": self.id,
            "Especie": self.especie,
            "Raza":self.raza if self.raza else "Sin raza",
            "Color":self.color,
            "Tamaño":self.tamaño,
            "Descripcion":self.descripcion,
            "Estado":self.estado,
            "Fotografia": getattr(self.fotografia,'url',"No disponible"),
            "Direccion": self.direccion if self.direccion else "No especificada"
        }
    
    def obtenerUbicacion(self):
        return self.direccion if self.direccion else "Ubicacion no disponible"

    def actualizarUbicacion(self,nueva_direccion):
        self.direccion=nueva_direccion
        self.save()
        return f"Ubicacion actualizada a: {self.direccion}"
    
    def dentroDeRango(self,latitud,longitud):
        #calcula la distancia entre la ubicacion de la mascota y las cordenadas dadas, saviendo que son coordenadas geograficas y devuelve  true su estan dentro de un rango definido por la variable rango
        rango=1
        cordenada1=(self.latitud,self.longitud)
        cordenada2=(latitud,longitud)
        distancia=geodesic(cordenada1,cordenada2).kilometers    
        return distancia<=rango
    
   
    
    



#Modelo de Publicacion
class Publicacion(models.Model):
    id=models.AutoField(primary_key=True)
    usuario=models.ForeignKey('Usuario',on_delete=models.CASCADE)
    mascota=models.ForeignKey('Mascota',on_delete=models.CASCADE)
    fecha_publicacion=models.DateTimeField(auto_now_add=True)
    comentarios=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Publicacion de {self.usuario.username} sobre {self.mascota.especie}"
    
    def crearPublicacion(self,usuario,mascota,comentarios=""):
        self.usuario=usuario
        self.mascota=mascota
        self.comentarios=comentarios
        self.save()
        return f"Publicacion creada por {self.usuario.username} sobre {self.mascota.especie}"
    
    def editarPublicacion(self,nuevo_comentario):
        self.comentarios=nuevo_comentario
        self.save()
        return f"Publicacion editada correctamente"
    
    def eliminarPublicacion(self):
        self.delete()
        return f"Publicacion eliminada con exito"
    
    def agregarComentarios(self,nuevo_comentario):
        self.comentarios+=f"\n{nuevo_comentario}"
        self.save()
        return "Comentario agregado correctamente"
    
# Clase Usuario
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    # Nombre del usuario (máximo 50 caracteres)
    nombre = models.CharField(max_length=50)    
    email = models.EmailField(unique=True)
    # Contraseña del usuario (en una aplicación real debería encriptarse)
    contraseña = models.CharField(max_length=128)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        # Devuelve el nombre del usuario como objeto
        return self.nombre

    # Guarda el usuario en     
    def registrar(self):
        self.save()
        return f"Usuario {self.nombre} registrado con éxito."
    
    def iniciarSesion(self, email, password):
        # Verifica el email y la contraseña para iniciar sesión
        if self.email == email and self.contraseña == password:
            return f"Sesión iniciada para {self.nombre}."
        return "Credenciales inválidas."
    
    def cerrarSesion(self):
        # Simula el cierre de sesión del usuario
        return f"Sesión cerrada para {self.nombre}."
    
    def actualizarPerfil(self, **kwargs):
        # Actualiza los datos del usuario con los valores proporcionados
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        return f"Perfil de {self.nombre} actualizado con éxito."
    
    def autenticacion(self, email, password):
        # Verifica si el email y la contraseña coinciden con los del usuario
        return self.email == email and self.contraseña == password