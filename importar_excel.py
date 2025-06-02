import os
import django
import openpyxl

# Configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_stock.settings")
django.setup()

from stock.models import Material

archivo_excel = 'stock_sap.xlsx'
wb = openpyxl.load_workbook(archivo_excel)
hoja = wb.active

# Buscar fila de cabeceras real (la que contiene "Número de material")
for i, fila in enumerate(hoja.iter_rows(values_only=True), start=1):
    if fila and "Número de material" in [str(celda).strip() for celda in fila if celda]:
        cabeceras = [str(celda).strip() for celda in fila]
        fila_inicio = i + 1  # Los datos empiezan justo después
        break
else:
    raise ValueError("No se encontró la fila con cabeceras esperadas")

print("Cabeceras detectadas:", cabeceras)

# Posiciones de las columnas necesarias
i_codigo = cabeceras.index("Número de material")
i_almacen = cabeceras.index("Alm.")
i_unidad = cabeceras.index("UMB")
i_cantidad = cabeceras.index("Libre utilización")

# Recorrer datos
for fila in hoja.iter_rows(min_row=fila_inicio, values_only=True):
    try:
        codigo = str(fila[i_codigo]).strip()
        ubicacion = str(fila[i_almacen]).strip()
        unidad = str(fila[i_unidad]).strip()
        cantidad = int(fila[i_cantidad]) if fila[i_cantidad] is not None else 0
    except (TypeError, ValueError, IndexError):
        continue

    Material.objects.update_or_create(
        codigo=codigo,
        defaults={
            'nombre': f"Material {codigo}",
            'cantidad': cantidad,
            'unidad': unidad,
            'ubicacion': ubicacion
        }
    )

    print(f"Actualizado: {codigo}")
