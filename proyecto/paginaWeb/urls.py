from django.urls import path
from .views import index, login_view, new_user_view, registro_mascota, buscar_mascota, listar_mascota, cambiar_estado_mascota

urlpatterns = [
    path("", index, name="index"),
    path('login/', login_view, name='login'),
    path('new_user/', new_user_view, name='new_user'),
    path('registro_mascota_perdida/', registro_mascota, name='registro_mascota_perdida'),
    path('buscar_mascota_perdida/', buscar_mascota, name='buscar_mascota_perdida'),
    path('listado_mascota/', listar_mascota, name='listar_mascotas_perdidas'),
    path('cambiar_estado_mascota/<int:mascota_id>/', cambiar_estado_mascota, name='cambiar_estado_mascota'),
]