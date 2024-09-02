from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Libro
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def lista_libros(request):
    print(f"Usuario autenticado: {request.user.is_authenticated}")
    print(f"Usuario: {request.user.username}")  
    buscar = request.GET.get('txtbuscar', '')
    if buscar:
        libros = Libro.objects.filter(
            Q(titulo__icontains=buscar) |
            Q(autor__icontains=buscar) |
            Q(isbn__icontains=buscar) |
            Q(descripcion__icontains=buscar)
        )
    else:
        libros = Libro.objects.all()

    paginator = Paginator(libros, 6)
    pagina = request.GET.get('pagina', 1)
    libros_paginados = paginator.get_page(pagina)

    return render(request, 'App1/libros.html', {'libros': libros_paginados, 'buscar': buscar})

def index(request):
    return render(request, 'App1/index.html',)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST['correo']
        password = request.POST['contraseña']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('App1:libros')  # Redirigir a la página de inicio o dashboard
        else:
            messages.error(request, 'Correo o contraseña incorrectos')
    return render(request, 'App1/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        email = request.POST['correo']
        password = request.POST['contraseña']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect('login')
    
    return render(request, 'App1/login.html')


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

def agregar_libro(request):
    if request.method == 'POST':
        nuevo_libro = Libro(
            titulo=request.POST['titulo'],
            autor=request.POST['autor'],
            editorial=request.POST['editorial'],
            fecha=request.POST['fecha'],
            isbn=request.POST['isbn'],
            numero_pags=request.POST['numero_pags'],
            numero_topografia=request.POST['numero_topografia'],
            numero_ejemplar=request.POST['numero_ejemplar'],
            descripcion=request.POST['descripcion'],
        )
        if 'portada' in request.FILES:
            portada = request.FILES['portada']
            # Genera un nombre de archivo único
            filename = f"portada_{nuevo_libro.titulo}_{portada.name}"
            # Guarda el archivo
            path = default_storage.save(f'portadas/{filename}', ContentFile(portada.read()))
            # Guarda la ruta relativa en el modelo
            nuevo_libro.portada = path
        
        return redirect('App1:libros')
    
    return render(request, 'App1:libros')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Libro

def eliminar_libro(request, libro_id):
    if request.method == 'POST':
        libro = get_object_or_404(Libro, id=libro_id)
        titulo = libro.titulo
        libro.delete()
        messages.success(request, f'El libro "{titulo}" ha sido eliminado correctamente.')
    return redirect('App1:libros')  # Asume que tienes una vista llamada 'libros'


from django.http import JsonResponse
from .models import Libro

def obtener_libro(request, libro_id):
    try:
        libro = Libro.objects.get(id=libro_id)
        data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'autor': libro.autor,
        'editorial': libro.editorial,
        'fecha': libro.fecha,
        'isbn': libro.isbn,
        'numero_pags': libro.numero_pags,
        'numero_topografia': libro.numero_topografia,
        'numero_ejemplar': libro.numero_ejemplar,
        'descripcion': libro.descripcion,
        'portada': libro.portada.url if libro.portada else None,
    }
        return JsonResponse(data)
    except Libro.DoesNotExist:
        return JsonResponse({'error': 'Libro no encontrado'}, status=404)
    

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        # Update the libro object with the new data
        libro.titulo = request.POST.get('titulo')
        libro.autor = request.POST.get('autor')
        libro.editorial = request.POST.get('editorial')
        libro.fecha = request.POST.get('fecha')
        libro.isbn = request.POST.get('isbn')
        libro.numero_pags = request.POST.get('numero_pags')
        libro.numero_topografia = request.POST.get('numero_topografia')
        libro.numero_ejemplar = request.POST.get('numero_ejemplar')
        libro.descripcion = request.POST.get('descripcion')
        
        if 'portada' in request.FILES:
            portada = request.FILES['portada']
            # Si ya existe una portada, elimínala
            if libro.portada:
                if os.path.isfile(libro.portada.path):
                    os.remove(libro.portada.path)
            
            # Genera un nombre de archivo único
            filename = f"portada_{libro.titulo}"
            # Guarda el nuevo archivo
            path = default_storage.save(f'portadas/{filename}', ContentFile(portada.read()))
            # Actualiza la ruta en el modelo
            libro.portada = path
        
        libro.save()
        messages.success(request, 'Libro actualizado correctamente.')
        return redirect('App1:libros')  # Redirect to the book list page
    
    # If it's a GET request, you might want to render the edit form
    # But in this case, we're using a modal, so we don't need to do anything here
    return redirect('App1:libros')


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('App1:login')


# subpaginas de inicio (horario, normas y quienes somos)

def horarios(request):
    return render(request, 'App1/horarios.html',)

def normas(request):
    return render(request, 'App1/normas.html',)

def mas_info(request):
    return render(request, 'App1/mas_info.html',)