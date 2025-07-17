from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar-curriculo/', views.cadastrar_curriculo, name='cadastrar_curriculo'),
    path('anunciar-vaga/', views.cadastrar_vaga, name='anunciar_vaga'),
    path('avaliacao-empresa/', views.avaliacao_empresa, name='avaliacao_empresa'),
    path('cargos-salarios/', views.cargos_salarios, name='cargos_salarios'),
    path('api/vagas/', views.VagaListAPI.as_view(), name='api_vagas'),
    path('api/curriculos/', views.CurriculoCreateAPI.as_view(), name='api_curriculos'),
   
]
