from django import forms
from .models import Curriculo, Vaga

class CurriculoForm(forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = ['resumo', 'habilidades', 'experiencia', 'educacao']

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['empresa', 'titulo', 'descricao', 'requisitos', 'link_aplicacao', 'localidade', 'modalidade', 'tipo_contrato', 'experiencia']
