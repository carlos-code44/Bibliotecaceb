from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'App1'

urlpatterns = [
    path('libros/', views.lista_libros, name='libros'),
    path('inicio/', views.index, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('agregar-libro/', views.agregar_libro, name='agregar_libro'),
    path('eliminar-libro/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('obtener_libro/<int:libro_id>/', views.obtener_libro, name='obtener_libro'),
    path('editar_libro/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('logout/', views.logout_view, name='logout'),
    path('horarios/', views.horarios, name='horarios'),
    path('normas/', views.normas, name='normas'),
    path('mas_info/', views.mas_info, name='mas_info'),
    path('prestamos/', views.prestamos, name='prestamos'),
    path('lista_prestamos/', views.lista_prestamos, name='lista_prestamos'),
    path('administradores/', views.administradores, name='administradores'),
    path('cambiar_usuario/', views.cambiar_usuario, name='cambiar_usuario'),
    path('cambiar_correo/', views.cambiar_correo, name='cambiar_correo'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('realizar-prestamo/', views.realizar_prestamo, name='realizar_prestamo'),
    path('marcar-devuelto/<int:prestamo_id>/', views.marcar_devuelto, name='marcar_devuelto'),
    path('libros-usuarios/', views.libros_usuarios_view, name='libros_usuarios'),
    path('toggle-admin/<int:user_id>/', views.toggle_admin, name='toggle_admin'),
    path('make-admin/<int:user_id>/', views.make_admin, name='make_admin'),
    path('remove-admin/<int:user_id>/', views.remove_admin, name='remove_admin'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

