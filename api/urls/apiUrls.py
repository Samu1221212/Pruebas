from django.urls import path, include

urlpatterns = [
    path('', include('api.urls')),  # Esto incluirá todas las URLs definidas en __init__.py
]