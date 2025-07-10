from django.shortcuts import render
from .models import Material
import pandas as pd
import os
from django.conf import settings

def buscar_material(request):
    material = None
    codigo = None
    linea = None
    descripcion = None

    if request.method == 'POST':
        codigo = request.POST.get('codigo')

        # Buscar en base de datos
        try:
            material = Material.objects.get(codigo=codigo)
        except Material.DoesNotExist:
            material = None

        # Ruta al archivo Excel en la raíz del proyecto
        excel_path = os.path.join(settings.BASE_DIR, 'Master de materiales.xlsx')

        try:
            df = pd.read_excel(excel_path, sheet_name='Master')

            # Eliminar espacios en nombres de columnas (por si acaso)
            df.columns = df.columns.str.strip()

            # Buscar fila que coincida con el código
            fila = df[df['Número de material'].astype(str) == str(codigo)]

            if not fila.empty:
                linea = fila.iloc[0]['Línea']
                descripcion = fila.iloc[0]['Texto breve de material']
        except Exception as e:
            print(f"Error al leer el archivo Excel: {e}")

    return render(request, 'buscar_material.html', {
        'material': material,
        'codigo': codigo,
        'linea': linea,
        'descripcion': descripcion
    })
