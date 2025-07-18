from django.shortcuts import render, redirect
from django.db.models import Q
from rest_framework import generics
from .models import Curriculo, Vaga
from .serializers import VagaSerializer, CurriculoSerializer
from .forms import CurriculoForm, VagaForm  # Adicionei VagaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import EscolaridadeForm, EscolaridadeDetalhadaForm, ExperienciaDetalhadaForm
import base64
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ConsentimentoCookie
from django.contrib.auth import logout

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
    uploaded_file = None
    file_name = None
    file_content = None
    if request.method == "POST" and request.FILES.get('curriculo_file'):
        uploaded_file = request.FILES['curriculo_file']
        file_name = uploaded_file.name
        file_content = base64.b64encode(uploaded_file.read()).decode('utf-8')
        request.session['curriculo_file_name'] = file_name
        request.session['curriculo_file_content'] = file_content
    else:
        file_name = request.session.get('curriculo_file_name')

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

    return render(request, "core/cadastrar_curriculo.html", {"form": form, "file_name": file_name})

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

def ajuda(request):
    return render(request, 'core/ajuda.html')

def cadastro_manual_pessoal(request):
    if request.method == 'POST':
        request.session['nome'] = request.POST.get('nome', '')
        request.session['sobrenome'] = request.POST.get('sobrenome', '')
        request.session['telefone'] = request.POST.get('telefone', '')
        request.session['mostrar_telefone'] = bool(request.POST.get('mostrar_telefone'))
        request.session['pais'] = request.POST.get('pais', 'Brasil')
        request.session['endereco'] = request.POST.get('endereco', '')
        request.session['cidade_estado'] = request.POST.get('cidade_estado', '')
        request.session['cep'] = request.POST.get('cep', '')
        return redirect('cadastro_manual_escolaridade')
    return render(request, 'core/cadastro_manual_pessoal.html')

def cadastro_manual_escolaridade(request):
    if request.method == 'POST':
        if 'pular' in request.POST:
            return redirect('cadastro_manual_experiencia')
        form = EscolaridadeDetalhadaForm(request.POST)
        if form.is_valid():
            escolaridades = request.session.get('escolaridades', [])
            escolaridade = form.cleaned_data.copy()
            escolaridades.append(escolaridade)
            request.session['escolaridades'] = escolaridades
            return redirect('cadastro_manual_escolaridade_revisao')
    else:
        form = EscolaridadeDetalhadaForm()
    return render(request, 'core/cadastro_manual_escolaridade.html', {'form': form})

def cadastro_manual_revisao(request):
    return render(request, "core/cadastro_manual_revisao.html")

def cadastro_manual_escolaridade_revisao(request):
    escolaridades = request.session.get('escolaridades', [])
    edit_idx = request.GET.get('edit')
    del_idx = request.GET.get('del')
    if del_idx is not None:
        try:
            escolaridades.pop(int(del_idx))
            request.session['escolaridades'] = escolaridades
        except Exception:
            pass
        return redirect('cadastro_manual_escolaridade_revisao')
    if edit_idx is not None:
        try:
            dados = escolaridades[int(edit_idx)]
            form = EscolaridadeDetalhadaForm(initial=dados)
            if request.method == 'POST' and 'salvar_edicao' in request.POST:
                form = EscolaridadeDetalhadaForm(request.POST)
                if form.is_valid():
                    escolaridades[int(edit_idx)] = form.cleaned_data.copy()
                    request.session['escolaridades'] = escolaridades
                    return redirect('cadastro_manual_escolaridade_revisao')
            return render(request, 'core/cadastro_manual_escolaridade.html', {'form': form, 'edit_idx': edit_idx})
        except Exception:
            pass
    if request.method == 'POST':
        if 'adicionar' in request.POST:
            return redirect('cadastro_manual_escolaridade')
        return redirect('cadastro_manual_experiencia')
    return render(request, 'core/cadastro_manual_escolaridade_revisao.html', {'escolaridades': escolaridades})

def cadastro_manual_experiencia(request):
    if request.method == 'POST':
        if 'pular' in request.POST:
            return redirect('cadastro_manual_revisao_final')
        form = ExperienciaDetalhadaForm(request.POST)
        if form.is_valid():
            experiencias = request.session.get('experiencias', [])
            experiencia = form.cleaned_data.copy()
            experiencias.append(experiencia)
            request.session['experiencias'] = experiencias
            return redirect('cadastro_manual_revisao_final')
    else:
        form = ExperienciaDetalhadaForm()
    return render(request, 'core/cadastro_manual_experiencia.html', {'form': form})

def cadastro_manual_experiencia_revisao(request):
    experiencias = request.session.get('experiencias', [])
    edit_idx = request.GET.get('edit')
    del_idx = request.GET.get('del')
    if del_idx is not None:
        try:
            experiencias.pop(int(del_idx))
            request.session['experiencias'] = experiencias
        except Exception:
            pass
        return redirect('cadastro_manual_experiencia_revisao')
    if edit_idx is not None:
        try:
            dados = experiencias[int(edit_idx)]
            form = ExperienciaDetalhadaForm(initial=dados)
            if request.method == 'POST' and 'salvar_edicao' in request.POST:
                form = ExperienciaDetalhadaForm(request.POST)
                if form.is_valid():
                    experiencias[int(edit_idx)] = form.cleaned_data.copy()
                    request.session['experiencias'] = experiencias
                    return redirect('cadastro_manual_experiencia_revisao')
            return render(request, 'core/cadastro_manual_experiencia.html', {'form': form, 'edit_idx': edit_idx})
        except Exception:
            pass
    if request.method == 'POST':
        if 'adicionar' in request.POST:
            return redirect('cadastro_manual_experiencia')
        return redirect('cadastro_manual_revisao_final')
    return render(request, 'core/cadastro_manual_experiencia_revisao.html', {'experiencias': experiencias})

def cadastro_manual_certificacoes(request):
    certificacoes = request.session.get('certificacoes', [])
    edit_idx = request.GET.get('edit')
    del_idx = request.GET.get('del')
    if del_idx is not None:
        try:
            certificacoes.pop(int(del_idx))
            request.session['certificacoes'] = certificacoes
        except Exception:
            pass
        return redirect('cadastro_manual_certificacoes')
    if edit_idx is not None:
        try:
            valor = certificacoes[int(edit_idx)]
            if request.method == 'POST' and 'salvar_edicao' in request.POST:
                novo = request.POST.get('nova_certificacao', '').strip()
                if novo:
                    certificacoes[int(edit_idx)] = novo
                    request.session['certificacoes'] = certificacoes
                    return redirect('cadastro_manual_certificacoes')
            return render(request, 'core/cadastro_manual_certificacoes.html', {'certificacoes': certificacoes, 'edit_idx': edit_idx, 'edit_val': valor})
        except Exception:
            pass
    if request.method == 'POST':
        if 'continuar' in request.POST:
            return redirect('cadastro_manual_revisao_final')
        nova = request.POST.get('nova_certificacao', '').strip()
        if nova:
            certificacoes.append(nova)
            request.session['certificacoes'] = certificacoes
    return render(request, 'core/cadastro_manual_certificacoes.html', {'certificacoes': certificacoes})

def cadastro_manual_revisao_final(request):
    nome = request.session.get('nome', '')
    sobrenome = request.session.get('sobrenome', '')
    telefone = request.session.get('telefone', '')
    mostrar_telefone = request.session.get('mostrar_telefone', False)
    pais = request.session.get('pais', 'Brasil')
    endereco = request.session.get('endereco', '')
    cidade_estado = request.session.get('cidade_estado', '')
    cep = request.session.get('cep', '')
    escolaridades = request.session.get('escolaridades', [])
    experiencias = request.session.get('experiencias', [])
    certificacoes = request.session.get('certificacoes', [])
    competencias = request.session.get('competencias', [])
    email = request.user.email if request.user.is_authenticated else ''
    context = {
        'nome': nome,
        'sobrenome': sobrenome,
        'telefone': telefone,
        'mostrar_telefone': mostrar_telefone,
        'pais': pais,
        'endereco': endereco,
        'cidade_estado': cidade_estado,
        'cep': cep,
        'escolaridades': escolaridades,
        'experiencias': experiencias,
        'certificacoes': certificacoes,
        'competencias': competencias,
        'email': email,
    }
    if request.method == 'POST':
        # Aqui pode salvar tudo no banco
        return redirect('index')
    return render(request, 'core/cadastro_manual_revisao_final.html', context)

def baixar_curriculo(request):
    file_name = request.session.get('curriculo_file_name')
    file_content = request.session.get('curriculo_file_content')
    if not file_name or not file_content:
        return HttpResponse('Arquivo não encontrado.'.encode('utf-8'), status=404)
    import base64
    file_bytes = base64.b64decode(file_content)
    response = HttpResponse(file_bytes, content_type='application/octet-stream')
    response['Content-Disposition'] = f'inline; filename="{file_name}"'
    return response

class ConsentimentoCookieAPI(APIView):
    def post(self, request):
        consentimento = request.data.get('consentimento')
        if consentimento not in ['accepted', 'rejected']:
            return Response({'erro': 'Valor de consentimento inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        usuario = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        obj, created = ConsentimentoCookie.objects.update_or_create(
            usuario=usuario,
            session_key=session_key if not usuario else None,
            defaults={'consentimento': consentimento}
        )
        return Response({'mensagem': 'Consentimento registrado com sucesso.'}, status=status.HTTP_200_OK)

@login_required
def perfil(request):
    return render(request, 'core/perfil.html', {'usuario': request.user})

@login_required
def configuracoes(request):
    return render(request, 'core/configuracoes.html', {'usuario': request.user})

@login_required
def excluir_conta(request):
    if request.method == 'POST':
        usuario = request.user
        logout(request)
        usuario.delete()
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('index')
    return render(request, 'core/excluir_conta.html', {'usuario': request.user})