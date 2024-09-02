import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca.settings")
import django
django.setup()

from App1.models import Libro
from django.db import connections

def importar_datos():
    with connections['default'].cursor() as cursor:
        # Ejecuta una consulta SQL para obtener los datos
        cursor.execute("SELECT id, isbn, titulo, autor, editorial, fecha, numero_pags, numero_topografia, numero_ejemplar, descripcion FROM libros")
        datos = cursor.fetchall()

        # Crea instancias de Libro a partir de los datos
        for dato in datos:
            libro = Libro(
                id=dato[0],
                isbn=dato[1],
                titulo=dato[2],
                autor=dato[3],
                editorial=dato[4],
                fecha=dato[5],
                numero_pags=dato[6],
                numero_topografia=dato[7],
                numero_ejemplar=dato[8],
                descripcion=dato[9]
            )
            libro.save()

if __name__ == "__main__":
    importar_datos()