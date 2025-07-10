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
    stock_linea = 0

    if request.method == 'POST':
        codigo = request.POST.get('codigo')

        # Buscar en base de datos
        try:
            material = Material.objects.get(codigo=codigo)
            print("Material encontrado en base de datos")
        except Material.DoesNotExist:
            material = None

        # Leer MASTER
        try:
            master_path = os.path.join(settings.BASE_DIR, 'Master de materiales.xlsx')
            df_master = pd.read_excel(master_path, sheet_name='Master')
            df_master.columns = df_master.columns.str.strip()
            print("Columnas Master:", df_master.columns.tolist())

            fila = df_master[df_master['Número de material'].astype(str) == str(codigo)]
            if not fila.empty:
                linea = fila.iloc[0]['Línea']
                descripcion = fila.iloc[0]['Texto breve de material']
        except Exception as e:
            print(f"Error al leer Master: {e}")

        # Leer STOCK_SAP (sin encabezado y asignar manualmente)
        try:
            stock_path = os.path.join(settings.BASE_DIR, 'stock_sap.xlsx')
            df_stock_raw = pd.read_excel(stock_path, header=None)

            # Asignar nombres de columnas desde la fila 2
            df_stock_raw.columns = df_stock_raw.iloc[1]
            df_stock = df_stock_raw[2:].copy()
            df_stock.columns = df_stock.columns.str.strip()

            df_stock['Número de material'] = df_stock['Número de material'].astype(str)

            filtro = df_stock[
                (df_stock['Número de material'] == str(codigo)) &
                (df_stock['Alm.'] == 'W199')
            ]

            print("Filas encontradas:", filtro)

            if not filtro.empty:
                stock_linea = filtro['Libre utilización'].sum()
        except Exception as e:
            print(f"Error al leer stock_sap.xlsx: {e}")

    return render(request, 'buscar_material.html', {
        'material': material,
        'codigo': codigo,
        'linea': linea,
        'descripcion': descripcion,
        'stock_linea': stock_linea
    })

