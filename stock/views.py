from django.shortcuts import render
from stock.models import Material

def buscar_material(request):
    resultado = None

    if request.method == "POST":
        codigo = request.POST.get("codigo", "").strip()
        try:
            resultado = Material.objects.get(codigo=codigo)
        except Material.DoesNotExist:
            resultado = "No encontrado"

    return render(request, "buscar_material.html", {"resultado": resultado})
