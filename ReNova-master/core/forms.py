from django import forms
from .models import Curriculo, Vaga
from allauth.account.forms import SignupForm

class CurriculoForm(forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = ['resumo', 'habilidades', 'experiencia', 'educacao']

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['empresa', 'titulo', 'descricao', 'requisitos', 'link_aplicacao', 'localidade', 'modalidade', 'tipo_contrato', 'experiencia']

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ''

class EscolaridadeForm(forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = ['educacao']
        widgets = {
            'educacao': forms.Textarea(attrs={
                'class': 'w-full border border-gray-400 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 5,
                'placeholder': 'Descreva sua formação acadêmica, cursos, instituições, datas, etc.'
            })
        }

class EscolaridadeDetalhadaForm(forms.Form):
    ESCOLARIDADE_CHOICES = [
        ("", "Selecione"),
        ("Fundamental", "Ensino Fundamental"),
        ("Medio", "Ensino Médio"),
        ("Tecnologo", "Tecnólogo"),
        ("Graduacao", "Graduação"),
        ("Pos", "Pós-graduação"),
        ("Mestrado", "Mestrado"),
        ("Doutorado", "Doutorado"),
        ("Outro", "Outro")
    ]
    escolaridade = forms.ChoiceField(choices=ESCOLARIDADE_CHOICES, required=True, label="Escolaridade *")
    area_estudo = forms.CharField(required=False, label="Área de estudo")
    instituicao = forms.CharField(required=False, label="Instituição de ensino")
    pais = forms.CharField(required=False, initial="Brasil", label="País")
    local_instituicao = forms.CharField(required=False, label="Local da instituição de ensino")
    atualmente_matriculado = forms.BooleanField(required=False, label="Atualmente matriculado")
    de_mes = forms.ChoiceField(choices=[("", "Mês")] + [(str(i), str(i)) for i in range(1, 13)], required=False, label="De (Mês)")
    de_ano = forms.ChoiceField(choices=[("", "Ano")] + [(str(y), str(y)) for y in range(1980, 2031)], required=False, label="De (Ano)")
    ate_mes = forms.ChoiceField(choices=[("", "Mês")] + [(str(i), str(i)) for i in range(1, 13)], required=False, label="Até (Mês)")
    ate_ano = forms.ChoiceField(choices=[("", "Ano")] + [(str(y), str(y)) for y in range(1980, 2031)], required=False, label="Até (Ano)")

class ExperienciaDetalhadaForm(forms.Form):
    cargo = forms.CharField(required=True, label="Cargo *")
    empresa = forms.CharField(required=False, label="Empresa")
    pais = forms.CharField(required=False, initial="Brasil", label="País")
    cidade_estado = forms.CharField(required=False, label="Cidade, estado")
    emprego_atual = forms.BooleanField(required=False, label="Emprego atual")
    de_mes = forms.ChoiceField(choices=[("", "Mês")] + [(str(i), str(i)) for i in range(1, 13)], required=False, label="De (Mês)")
    de_ano = forms.ChoiceField(choices=[("", "Ano")] + [(str(y), str(y)) for y in range(1980, 2031)], required=False, label="De (Ano)")
    ate_mes = forms.ChoiceField(choices=[("", "Mês")] + [(str(i), str(i)) for i in range(1, 13)], required=False, label="Até (Mês)")
    ate_ano = forms.ChoiceField(choices=[("", "Ano")] + [(str(y), str(y)) for y in range(1980, 2031)], required=False, label="Até (Ano)")
    descricao = forms.CharField(required=False, label="Descrição", widget=forms.Textarea(attrs={
        'rows': 5,
        'class': 'w-full border border-gray-400 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500',
        'placeholder': ''
    }))
