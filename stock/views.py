from django.shortcuts import render
from .models import Material

def buscar_material(request):
    resultado = None
    if request.method == 'GET':
        codigo = request.GET.get('codigo')
        if codigo:
            try:
                resultado = Material.objects.get(codigo=codigo)
            except Material.DoesNotExist:
                resultado = "No encontrado"
    return render(request, 'buscar_material.html', {'resultado': resultado})
