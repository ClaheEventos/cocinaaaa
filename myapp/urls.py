from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.buscar_o_crear_cliente, name='inicio'),
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
     path('<int:cliente_id>/plan/', views.elegir_plan, name='elegir_plan'),

    # URL para elegir las Bebidas de un cliente
    path('<int:cliente_id>/bebidas/', views.elegir_bebidas, name='elegir_bebidas'),
    path('seleccionar_cliente_para_editar/', views.seleccionar_cliente_para_editar, name='seleccionar_cliente_para_editar'),
    path('list', views.lista_clientes, name='lista_clientes'),
    path('crear', views.crear_cliente, name='crear_cliente'),
    path('<int:cliente_id>/cantidades/', views.elegir_cantidades, name='elegir_cantidades'),
    path('<int:cliente_id>/recepcion/', views.elegir_recepcion, name='elegir_recepcion'),
    path('<int:cliente_id>/barra-tragos/', views.elegir_barra_tragos, name='elegir_barra_tragos'),
    path('<int:cliente_id>/islas/', views.elegir_islas, name='elegir_islas'),
    path('<int:cliente_id>/islas-premium/', views.elegir_islas_premium, name='elegir_islas_premium'),
    path('<int:cliente_id>/elegir-platos/', views.elegir_platos, name='elegir_platos'),
    path('<int:cliente_id>/postres/', views.elegir_postres, name='elegir_postres'),
    path('<int:cliente_id>/extras/', views.elegir_extras, name='elegir_extras'),
    path('<int:cliente_id>/shows/', views.elegir_shows, name='elegir_shows'),
    path('<int:cliente_id>/fin-de-fiesta/', views.elegir_fin_de_fiesta, name='elegir_fin_de_fiesta'),
    path('<int:cliente_id>/mesa-dulce-premium/', views.elegir_mesa_dulce_premium, name='elegir_mesa_dulce_premium'),
    path('<int:cliente_id>/telefonos/', views.agregar_telefonos, name='agregar_telefonos'),
    path('<int:cliente_id>/resumen/', views.resumen_cliente, name='resumen_cliente'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]