Wine Spa - Sistema de Gestión

Este proyecto es un *sistema de gestión para Wine Spa*, un negocio de manicure y pedicure que busca optimizar sus procesos internos como:

- Gestión de citas y agendamientos.  
- Gestión de insumos y proveedores.  
- Control de abastecimientos.  
- Liquidación de trabajadoras.  
- Administración de clientes y usuarios.  

El proyecto fue desarrollado en el marco de la formación *Tecnólogo en Análisis y Desarrollo de Software (SENA)*.


Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.10+  
- Django 4.x  
- pip  
- MySQL Server + MySQL Workbench  
- Un entorno virtual recomendado: venv o virtualenv


⚙ Instalación y Configuración

1. Clonar el repositorio
   ```bash
   git clone https://github.com/usuario/winespa.git
   cd winespa

2. Instalar dependencias
  -pip install -r requirements.txt

3. Aplicar migraciones de base de datos
  -python manage.py migrate

4.Crear la base de datos en MySQL Workbench
Abre Workbench y ejecuta:
  -CREATE DATABASE winespaapi;
  
5.Configurar las credenciales de base de datos en settings.py (sección DATABASES)

Ejemplo:
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'winespaapi',
        'USER': 'tu usuario',
        'PASSWORD': 'tu contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

6. Ejecutar el Proyecto

Para iniciar el servidor de desarrollo:
  -python manage.py runserver
7. Ejecutar Pruebas

El proyecto incluye pruebas automatizadas en la carpeta tests/.

Ejemplo para correr las pruebas de categoría de insumos:

  -python manage.py test api.tests.test_categoriainsumos
