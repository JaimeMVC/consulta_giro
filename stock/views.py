from django.shortcuts import render
from .models import Material

def buscar_material(request):
    material = None
    codigo = ""
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            material = Material.objects.get(codigo=codigo)
            material.cantidad_abs = abs(material.cantidad)  # 👈 agregamos este atributo para el template
        except Material.DoesNotExist:
            material = None
    return render(request, 'buscar_material.html', {'material': material, 'codigo': codigo})
