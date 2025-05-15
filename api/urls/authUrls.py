from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api.views.authViews import LoginView, LogoutView, RegistroClienteView, user_info

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/cliente/', RegistroClienteView.as_view(), name='registro_cliente'),
    path('me/', user_info, name='user_info'),
]

auth_urlpatterns = urlpatterns