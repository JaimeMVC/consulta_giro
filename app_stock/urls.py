from django.contrib import admin
from django.urls import path, include  # 👈 necesario para incluir otras urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stock.urls')),  # 👈 esto conecta las urls de tu app 'stock'
]
