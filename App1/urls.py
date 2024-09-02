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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
