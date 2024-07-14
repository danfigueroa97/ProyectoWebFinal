from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns=[
    path('',views.registro, name='registro'),
    path('index/',views.index, name='main'),
    path('peliculas/',views.peliculas, name='peliculas'),
    path('series/',views.series, name='series'),
    path('inicio/',views.inicio, name='inicio'),
    path('registro/',views.registro,name='registro'),
    path('login/',views.login_view,name='login'),
    path('multimedia/<int:idMultimedia>/',views.multimedia,name='multimedia'),
    path('crud1/',views.listaMultimedia,name='crud1'),
    path('editar/<int:pk>',views.updateMultimedia.as_view(),name='editar' ),
    path('borrar/<int:pk>',views.deleteMultimedia.as_view(),name='borrar' ),
    path('ver/<int:idMultimedia>/', views.verMultimedia, name='ver'),
    path('nuevo/',views.crearMultimedia,name='nuevo' ),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('buscar/', views.buscar_multimedia, name='buscar_multimedia'),
    path('add_to_list/<int:multimedia_id>/', views.add_to_list, name='add_to_list'),
    path('remove_from_list/<int:multimedia_id>/', views.remove_from_list, name='remove_from_list'),
    path('mi_lista/', views.mi_lista, name='mi_lista'),
    path('borrar_comentario/<int:comentario_id>/', views.borrar_comentario, name='borrar_comentario'),

    
    path('crud2/', views.crud2, name='crud2'),
    path('crud2/agregar_respuesta/<int:comentario_id>/', views.agregar_respuesta, name='agregar_respuesta'),
    path('crud2/<int:pk>/', views.ver_respuesta, name='ver_respuesta'),
    path('crud2/<int:pk>/editar/', views.update_respuesta, name='update_respuesta'),
    path('crud2/<int:pk>/borrar/', views.borrar_respuesta, name='borrar_respuesta'),

    path('registro/',views.registro,name='registro'),
    path('crud3/', views.verUser, name='verUser'),
    path('crud3/<int:user_id>/', views.detallesUser, name='detallesUser'),
    path('crud3/<int:user_id>/editar/', views.updateUser, name='updateUser'),
    path('crud3/<int:user_id>/eliminar/', views.deleteUser, name='deleteUser'),

]
