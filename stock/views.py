from django.shortcuts import render
from .models import Material
import pandas as pd
import os

def buscar_material(request):
    material = None
    codigo = ""
    linea = None

    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        try:
            material = Material.objects.get(codigo=codigo)
        except Material.DoesNotExist:
            material = None

        try:
            excel_path = os.path.join(os.path.dirname(__file__), '..', 'Master de materiales.xlsx')
            df = pd.read_excel(excel_path, sheet_name="Master")

            print("📥 Código ingresado:", codigo)
            print("🧾 Columnas del Excel:", df.columns.tolist())
            print("🔍 Primeras filas del Excel:\n", df.head())

            # Forzar tipo string en columna y buscar coincidencia exacta
            df['Número de material'] = df['Número de material'].astype(str)
            fila = df[df['Número de material'] == codigo]

            print("✅ Coincidencia encontrada:\n", fila)

            if not fila.empty:
                linea = fila.iloc[0]['Línea']  # O el nombre exacto de la columna
                print("🧵 Línea encontrada:", linea)
            else:
                print("⚠️ Código no encontrado en el Excel.")

        except Exception as e:
            print("❌ Error leyendo el Excel:", e)

    return render(request, 'buscar_material.html', {
        'material': material,
        'codigo': codigo,
        'linea': linea
    })
