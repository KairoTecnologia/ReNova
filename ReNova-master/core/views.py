from django.shortcuts import render, redirect
from django.db.models import Q
from rest_framework import generics
from .models import Vaga, Curriculo
from .serializers import VagaSerializer, CurriculoSerializer
from .forms import CurriculoForm, VagaForm  # Adicionei VagaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# API para listar vagas
class VagaListAPI(generics.ListAPIView):
    queryset = Vaga.objects.all()
    serializer_class = VagaSerializer

# API para criar currículos
class CurriculoCreateAPI(generics.CreateAPIView):
    queryset = Curriculo.objects.all()
    serializer_class = CurriculoSerializer

# View para página inicial
def index(request):
    query = request.GET.get("q")
    modalidade = request.GET.getlist("modalidade")
    estado = request.GET.get("estado")
    cidade = request.GET.get("cidade")
    empresa_id = request.GET.get("empresa")
    tipo_vaga = request.GET.get("tipo_vaga")

    vagas = Vaga.objects.all()

    if query:
        vagas = vagas.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query)
        )
    if modalidade:
        vagas = vagas.filter(modalidade__in=modalidade)
    if estado:
        vagas = vagas.filter(empresa__estado__iexact=estado)
    if cidade:
        vagas = vagas.filter(empresa__cidade__iexact=cidade)
    if empresa_id:
        vagas = vagas.filter(empresa__id=empresa_id)
    if tipo_vaga:
        vagas = vagas.filter(tipo_contrato__iexact=tipo_vaga)

    # Para popular selects de filtro
    estados = Vaga.objects.values_list('empresa__estado', flat=True).distinct()
    cidades = Vaga.objects.values_list('empresa__cidade', flat=True).distinct()
    empresas = Vaga.objects.values('empresa__id', 'empresa__nome').distinct()
    tipos_vaga = Vaga.objects.values_list('tipo_contrato', flat=True).distinct()

    context = {
        "vagas": vagas,
        "estados": estados,
        "cidades": cidades,
        "empresas": empresas,
        "tipos_vaga": tipos_vaga,
        "filtros": {
            "modalidade": modalidade,
            "estado": estado,
            "cidade": cidade,
            "empresa_id": empresa_id,
            "tipo_vaga": tipo_vaga,
            "q": query,
        }
    }
    return render(request, "core/index.html", context)

# View para cadastrar currículo
@login_required
def cadastrar_curriculo(request):
    try:
        curriculo = request.user.curriculo  # Pega currículo existente (OneToOne)
    except Curriculo.DoesNotExist:
        curriculo = None

    if request.method == "POST":
        form = CurriculoForm(request.POST, instance=curriculo)
        if form.is_valid():
            curriculo = form.save(commit=False)
            curriculo.usuario = request.user
            curriculo.save()
            messages.success(request, "Currículo enviado/atualizado com sucesso!")
            return redirect("index")
    else:
        form = CurriculoForm(instance=curriculo)

    return render(request, "core/cadastrar_curriculo.html", {"form": form})

@login_required
def cadastrar_vaga(request):
    if request.method == "POST":
        form = VagaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaga cadastrada com sucesso!")
            return redirect("index")
    else:
        form = VagaForm()
    return render(request, "core/cadastrar_vaga.html", {"form": form})

def avaliacao_empresa(request):
    return render(request, "core/avaliacao_empresa.html")

def cargos_salarios(request):
    return render(request, "core/cargos_salarios.html")