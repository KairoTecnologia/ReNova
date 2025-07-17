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
    path('cadastrar-curriculo/manual/', views.cadastro_manual_pessoal, name='cadastro_manual_pessoal'),
    path('cadastro/manual/escolaridade/', views.cadastro_manual_escolaridade, name='cadastro_manual_escolaridade'),
    path('cadastro/manual/escolaridade/revisao/', views.cadastro_manual_escolaridade_revisao, name='cadastro_manual_escolaridade_revisao'),
    path('cadastrar-curriculo/revisao/', views.cadastro_manual_revisao, name='cadastro_manual_revisao'),
    path('cadastro/manual/experiencia/', views.cadastro_manual_experiencia, name='cadastro_manual_experiencia'),
    path('cadastro/manual/experiencia/revisao/', views.cadastro_manual_experiencia_revisao, name='cadastro_manual_experiencia_revisao'),
    path('cadastro/manual/certificacoes/', views.cadastro_manual_certificacoes, name='cadastro_manual_certificacoes'),
    path('cadastro/manual/revisao-final/', views.cadastro_manual_revisao_final, name='cadastro_manual_revisao_final'),
    path('curriculo/baixar/', views.baixar_curriculo, name='baixar_curriculo'),
   
]
