from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Libro
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .decorators import admin_required

@admin_required
def lista_libros(request): 
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



# --------------------------------vistas de login-register-roles------------------------------------------------

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

def login_view(request):
    if request.method == 'POST':
        email = request.POST['correo']
        password = request.POST['contraseña']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            # Verifica si existe un perfil de usuario, si no, créalo
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if user.userprofile.is_admin:
                return redirect('App1:libros')
            else:
                return redirect('App1:libros_usuarios')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'App1/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        email = request.POST['correo']
        password = request.POST['contraseña']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado')
            return redirect('App1:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este usuario ya está registrado')
            return redirect('App1:register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect('App1:login')
    
    return render(request, 'App1/login.html')


# asignar roles de administrador


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User

@user_passes_test(lambda u: u.userprofile.is_admin)
def toggle_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.userprofile.is_admin = not user.userprofile.is_admin
    user.userprofile.save()
    return redirect('App1:administradores')

@admin_required
def administradores(request):
    users = User.objects.all()
    return render(request, 'App1/administradores.html', {'users': users})



#---------------------------------vistas crud---------------------------------------------------------------------

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

from django.shortcuts import redirect, render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from .models import Libro

def agregar_libro(request):
    if request.method == 'POST':
        try:
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
                filename = f"portada_{nuevo_libro.titulo}_{portada.name}"
                path = default_storage.save(f'portadas/{filename}', ContentFile(portada.read()))
                nuevo_libro.portada = path
            
            nuevo_libro.save()  # Save the new book to the database
            messages.success(request, 'Libro agregado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al agregar el libro: {str(e)}')
        
        return redirect('App1:libros')
    
    return render(request, 'App1/libros.html')


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


# ---------------------------subpaginas de inicio (horario, normas y quienes somos)-----------------------

def horarios(request):
    return render(request, 'App1/horarios.html',)

def normas(request):
    return render(request, 'App1/normas.html',)

def mas_info(request):
    return render(request, 'App1/mas_info.html',)



# ----------------------------------vistas encargadas del formulario de prestamos--------------------------

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Libro, Prestamo
from django.contrib import messages


from django.shortcuts import redirect
from django.contrib import messages

@require_POST
def realizar_prestamo(request):
    libro_id = request.POST.get('libro_id')
    try:
        libro = Libro.objects.get(id=libro_id)
        
        if not libro.disponible:
            messages.error(request, 'Este libro ya no está disponible.')
            return redirect('App1:prestamos')
        
        prestamo = Prestamo(
            libro=libro,
            estudiante_nombre=request.POST.get('student_name'),
            curso=request.POST.get('grade'),
            telefono=request.POST.get('contact_phone'),
            email=request.POST.get('contact_email'),
            fecha_prestamo=request.POST.get('loan_date'),
            fecha_devolucion=request.POST.get('return_date'),
            comentarios=request.POST.get('comments')
        )
        prestamo.save()
        
        libro.disponible = False
        libro.save()
        
        messages.success(request, 'Préstamo realizado con éxito.')
    except Libro.DoesNotExist:
        messages.error(request, 'El libro seleccionado no existe.')
    except Exception as e:
        messages.error(request, f'Error al realizar el préstamo: {str(e)}')
    
    return redirect('App1:prestamos')


from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Libro

@admin_required
def prestamos(request):
    buscar = request.GET.get('txtbuscar2', '')
    
    if buscar:
        libros = Libro.objects.filter(
            Q(titulo__icontains=buscar) |
            Q(autor__icontains=buscar) |
            Q(isbn__icontains=buscar) |
            Q(descripcion__icontains=buscar)
        )
    else:
        libros = Libro.objects.all()

    # Paginación
    paginator = Paginator(libros, 3)  # 3 libros por página
    pagina = request.GET.get('pagina', 1)
    libros_paginados = paginator.get_page(pagina)

    context = {
        'libros': libros_paginados,
        'buscar': buscar,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('App1/_libros_list.html', context)
        return JsonResponse({
            'html': html,
            'has_previous': libros_paginados.has_previous(),
            'has_next': libros_paginados.has_next(),
            'previous_page_number': libros_paginados.previous_page_number() if libros_paginados.has_previous() else None,
            'next_page_number': libros_paginados.next_page_number() if libros_paginados.has_next() else None,
        })
    
    return render(request, 'App1/prestamos.html', context)


#-------------------------------vistas de historial de prestamos---------------------------------------------

    
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Prestamo, Libro

@admin_required
def lista_prestamos(request):
    prestamos = Prestamo.objects.all().order_by('-fecha_prestamo')
    return render(request, 'App1/lista_prestamos.html', {'prestamos': prestamos})

def marcar_devuelto(request, prestamo_id):
    if request.method == 'POST':
        prestamo = Prestamo.objects.get(id=prestamo_id)
        libro = prestamo.libro
        libro.disponible = True
        libro.save()
        prestamo.delete()
        return JsonResponse({'success': True, 'message': 'Préstamo marcado como devuelto y eliminado.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})



#----------------------------------vistas de admisntradores--------------------------------------------------


from django.contrib.auth.models import User
from django.shortcuts import render

@admin_required
def administradores_view(request):
    users = User.objects.all().select_related('userprofile')
    print(f"Número de usuarios: {users.count()}")  # Agrega esta línea para depuración
    return render(request, 'App1/administradores.html', {'users': users})




from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile

def make_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.is_admin = True
    profile.save()
    return redirect('App1:administradores')

def remove_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = UserProfile.objects.get(user=user)
    profile.is_admin = False
    profile.save()
    return redirect('App1:administradores')

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('App1:administradores')



#------------------------------- vistas editar perfil-----------------------------------------------------

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect

def cambiar_usuario(request):
    if request.method == 'POST':
        nuevo_usuario = request.POST.get('nuevo_usuario')
        password = request.POST.get('password')
        
        # Verificamos si la contraseña es correcta
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            # Actualizamos el nombre de usuario
            user.username = nuevo_usuario
            user.save()
            messages.success(request, 'Usuario actualizado correctamente')
            return redirect('App1:libros')
        else:
            messages.error(request, 'Contraseña incorrecta')
            return redirect('App1:cambiar_usuario')

    return redirect('App1:libros')


def cambiar_correo(request):
    if request.method == 'POST':
        nuevo_correo = request.POST.get('nuevo_correo')
        password = request.POST.get('password')
        
        # Verificamos si la contraseña es correcta
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            # Actualizamos el correo del usuario
            user.email = nuevo_correo
            user.save()
            messages.success(request, 'Correo actualizado correctamente')
            return redirect('App1:libros')
        else:
            messages.error(request, 'Contraseña incorrecta')
            return redirect('App1:cambiar_correo')

    return redirect('App1:libros')



def cambiar_contrasena(request):
    if request.method == 'POST':
        nueva_contrasena = request.POST.get('nueva_contrasena')
        contrasena_actual = request.POST.get('contrasena_actual')
        
        # Verificamos si la contraseña actual es correcta
        user = authenticate(username=request.user.username, password=contrasena_actual)
        if user is not None:
            # Actualizamos la contraseña del usuario
            user.set_password(nueva_contrasena)
            user.save()
            
            # Actualizamos la sesión para que el usuario no se desconecte
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('App1:libros')
        else:
            messages.error(request, 'Contraseña actual incorrecta')
            return redirect('App1:cambiar_contrasena')

    return redirect('App1:libros')


#----------------------------------------vista para paginas de usuario------------------------------------------------

def libros_usuarios_view(request):

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

    return render(request, 'App1/libros_usuarios.html', {'libros': libros_paginados, 'buscar': buscar})