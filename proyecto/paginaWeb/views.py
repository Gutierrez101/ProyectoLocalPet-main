from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Mascota, Usuario

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['contraseña']
        usuario = Usuario.objects.filter(nombre=username, contraseña=password).first()
        if usuario:
            return listar_mascota(request)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'Login.html')

def new_user_view(request):
    if request.method == 'POST':
        username = request.POST['nombre']
        password = request.POST['contrasena']
        confirm_password = request.POST['contrasena']
        email = request.POST['correo']

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'newUser.html')
        
        if Usuario.objects.filter(nombre=username).exists():
            messages.error(request, 'El usuario ya existe')
        elif Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado')
        else:
            user = Usuario(nombre=username, contraseña=password, email=email)
            user.save()
            messages.success(request, 'Usuario registrado correctamente')
            return redirect('login')
    return render(request, 'newUser.html')

def registro_mascota(request):
    if request.method == 'POST':
        raza = request.POST.get('raza')
        color = request.POST.get('color')
        tamaño = request.POST.get('tamano')
        latitud = request.POST.get('latitud') or 0
        longitud = request.POST.get('longitud') or 0
        fotografia = request.FILES.get('media')
        descripcion = request.POST.get('descripcion')
        genero = request.POST.get('genero')
        contacto = request.POST.get('contacto')
        fecha = request.POST.get('fecha-inicio')
        
        mascota = Mascota(
            genero=genero,
            raza=raza,
            color=color,
            tamaño=tamaño,
            latitud=latitud,
            longitud=longitud,
            fotografia=fotografia,
            descripcion=descripcion,
            contacto=contacto,
            fecha=fecha
        )
        mascota.save()
        return listar_mascota(request)
    return render(request, 'registro-mascota-perdida.html')

def buscar_mascota(request):
    if request.method == 'POST':
        mascotasFiltradas = Mascota.objects.all()

        if request.POST.get('raza') and request.POST.get('raza') != '':
            mascotasFiltradas = mascotasFiltradas.filter(raza=request.POST.get('raza'))
        if request.POST.get('color') and request.POST.get('color') != '':
            mascotasFiltradas = mascotasFiltradas.filter(color=request.POST.get('color'))
        if request.POST.get('genero') and request.POST.get('genero') != '':
            mascotasFiltradas = mascotasFiltradas.filter(genero=request.POST.get('genero'))
        if request.POST.get('tamano'):
            mascotasFiltradas = mascotasFiltradas.filter(tamaño=request.POST.get('tamano'))
        
            
        
        
        
        if request.POST.get('fecha-inicio') and request.POST.get('fecha-inicio') != '' :
            mascotasFiltradas = mascotasFiltradas.filter(fecha__gte=request.POST.get('fecha-inicio'))
            
        if request.POST.get('latitud') and request.POST.get('longitud') and request.POST.get('latitud') != '' and request.POST.get('longitud') != '':
            mascotasFiltradas = [mascota for mascota in mascotasFiltradas if mascota.dentroDeRango(float(request.POST.get('latitud')), float(request.POST.get('longitud')))]
        
        
        
        if not mascotasFiltradas:
            error_message='No se encontraron mascotas con los filtros seleccionados'
            messages.error(request,error_message)
            return render(request, 'buscar-mascota-perdida.html', {'error_message': error_message})
        
        return render(request, 'listado-mascota.html', {'Mascotas': mascotasFiltradas,'error_message': None})
              
    return render(request, 'buscar-mascota-perdida.html')

def listar_mascota(request):
    mascotas = Mascota.objects.all()
    return render(request, 'listado-mascota.html', {'Mascotas': mascotas})

def cambiar_estado_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    if mascota.estado == "Perdido":
        mascota.estado = "Encontrado"
        messages.success(request, f"La mascota mascota ahora está marcada como ENCONTRADA.")
    else:
        messages.warning(request, "La mascota ya había sido encontrada.")
    
    mascota.save()
    return redirect('listar_mascotas_perdidas')

