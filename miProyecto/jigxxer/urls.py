from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    # Otras URLs
    path('redireccion/', views.mi_vista_de_redireccion, name='redireccion'),
    path('accounts/profile/', views.mi_vista_de_redireccion, name='mi_vista_de_redireccion'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('registro/', views.registro, name="registro"),
    path('negociof', views.crear_negocio, name="formularioNegocio"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), 
    
    # URLs de administrador
    path("inicio", login_required(views.inicio), name='inicio'),
    path("nosotros", login_required(views.nosotros), name="nosotros"),
    path("productos/", login_required(views.producto), name="productos"),
    path("productos/crear", login_required(views.crear), name="crear"),
    path("productos/editar", login_required(views.editar), name="editar"),
    path("negocios", login_required(views.negocio), name="negocio"),
    path('eliminar/<int:Id_venta>', login_required(views.eliminar), name='eliminar'),
    path("productos/editar/<int:Id_venta>", login_required(views.editar), name="editar"),
    path('productos', login_required(views.buscar_producto), name='buscar_producto'),
    
    # URLs de clientes
    path('cliente', login_required(views.cliente), name='cliente'),
    path('bienvenido', login_required(views.bienvenido), name='bienvenido'),
    path('sobre_nosotros', login_required(views.sobre_nosotros), name='sobre_nosotros'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
