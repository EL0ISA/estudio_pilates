# studio/views.py

from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from .models import Servico
from .forms import ServicoForm, ServicoFilterForm
from .models import Funcionario
from .forms import FuncionarioForm 
from .models import Aluno
from .forms import AlunoForm 
from .models import Plano, ContaReceber, Pagamento, Aula, AulaAluno
from .forms import PlanoForm, ContaReceberForm, PagamentoForm, AulaForm, AulaAlunoFrequenciaForm
from .forms import CustomLoginForm


# View Serviços
def lista_servicos(request):
    queryset = Servico.objects.all() 
    filter_form = ServicoFilterForm(request.GET or None)
   
    if filter_form.is_valid():
        modalidade = filter_form.cleaned_data.get('modalidade')
        niveis = filter_form.cleaned_data.get('niveis_dificuldade')

        if modalidade:
            queryset = queryset.filter(modalidade__icontains=modalidade)

        if niveis: 
            queryset = queryset.filter(niveis_dificuldade=niveis)

    queryset = queryset.order_by('modalidade')
    contexto = {
        'lista_servicos': queryset,   
        'filter_form': filter_form, 
    }
    return render(request, 'studio/servicos/listar_servicos.html', contexto)


def novo_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('studio:lista_servicos')
    else:
        form = ServicoForm() 
    contexto = {
        'form': form,
    }
    return render(request, 'studio/servicos/cadastrar_servicos.html', contexto)


def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('studio:lista_servicos') #
    else:
        form = ServicoForm(instance=servico)
    contexto = {
        'form': form,
    }
    return render(request, 'studio/servicos/cadastrar_servicos.html', contexto)

def excluir_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        modalidade_servico = servico.modalidade
        servico.delete()
        messages.success(request, f'Serviço "{modalidade_servico}" excluído com sucesso.') # <--- USO DA FUNÇÃO
        return redirect('studio:lista_servicos')
    else:
        return redirect('studio:lista_servicos')


# View Funcionario 
def cadastro_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_funcionario')
    else:
        form = FuncionarioForm()
    return render(request, 'studio/funcionario/cadastro_funcionario.html', {'form': form})


def listar_funcionario(request):
    funcionario = Funcionario.objects.all()
    return render(request, 'studio/funcionario/listar_funcionario.html', {'funcionario': funcionario})


def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_funcionario')
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'studio/funcionario/editar_funcionario.html', {'form': form, 'funcionario': funcionario})


def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, "Funcionário excluído com sucesso!")
        return redirect('studio:listar_funcionario')
    return redirect('studio:listar_funcionario')  

#View Aluno
def listar_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, 'studio/aluno/listar_alunos.html', {'alunos': alunos})


def cadastro_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'studio/aluno/cadastrar_aluno.html', {'form': form})


def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'studio/aluno/editar_aluno.html', {'form': form})


def excluir_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    aluno.delete()
    messages.success(request, "Aluno excluído com sucesso!")
    return redirect('studio:listar_alunos')


#View Plano
def listar_planos(request):
    planos = Plano.objects.all()
    return render(request, 'studio/plano/listar_planos.html', {'planos': planos})


def cadastro_plano(request):
    if request.method == 'POST':
        form = PlanoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_planos')
    else:
        form = PlanoForm()
    return render(request, 'studio/plano/cadastrar_plano.html', {'form': form})


def editar_plano(request, id):
    plano = get_object_or_404(Plano, id=id)
    if request.method == 'POST':
        form = PlanoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_planos')
    else:
        form = PlanoForm(instance=plano)
    return render(request, 'studio/plano/editar_plano.html', {'form': form})


def excluir_plano(request, id):
    plano = get_object_or_404(Plano, id=id)
    plano.delete()
    messages.success(request, "Plano excluído com sucesso!")
    return redirect('studio:listar_planos')


# Views aula
def listar_aulas(request):
    aulas = Aula.objects.all()
    return render(request, 'studio/aula/listar_aulas.html', {'aulas': aulas})


def detalhes_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    return render(request, 'studio/aula/detalhar_aula.html', {'aula': aula})


def frequencia_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)

    if aula.cancelada:
        messages.error(request, 'Não é possível marcar frequência em uma aula cancelada.')
        return redirect('studio:detalhes_aula', pk=aula.pk)

    AulaAlunoFormSet = modelformset_factory(
        AulaAluno,
        form=AulaAlunoFrequenciaForm,
        extra=0  
    )

    queryset = AulaAluno.objects.filter(aula=aula)

    if request.method == 'POST':
        formset = AulaAlunoFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect('studio:detalhes_aula', pk=aula.pk)
    else:
        formset = AulaAlunoFormSet(queryset=queryset)

    return render(request, 'studio/aula/frequencia_aula.html', {
        'aula': aula,
        'formset': formset,
    })


def cadastro_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_aulas')
    else:
        form = AulaForm()
    return render(request, 'studio/aula/cadastrar_aula.html', {'form': form})


def editar_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    if aula.cancelada:
            messages.error(request, 'Não é possível editar uma aula cancelada.')
            return redirect('studio:detalhes_aula', pk=aula.pk)
    if request.method == 'POST':
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aula atualizada com sucesso.')
            return redirect('studio:detalhes_aula', pk=aula.pk)
    else:
        form = AulaForm(instance=aula)
    return render(request, 'studio/aula/editar_aula.html', {'form': form, 'aula': aula})


def cancelar_aula(request, codigo):
    aula = get_object_or_404(Aula, codigo=codigo)
    aula.cancelada = True
    aula.save()
    messages.success(request, f'Aula {aula.codigo} foi cancelada com sucesso.')
    return redirect('studio:listar_aulas')


# Views contas/pagamentos
def listar_contas(request):
    contas = ContaReceber.objects.all()  # Pega todas as contas a receber
    aluno_id = request.GET.get('aluno')
    estado = request.GET.get('estado')  # agora é estado, não status
    inicio = request.GET.get('inicio')
    fim = request.GET.get('fim')
    if aluno_id:
        contas = contas.filter(aluno_id=aluno_id)
    if estado:
        contas = [c for c in contas if c.estado_atual.lower() == estado.lower()]
    if inicio and fim:
        contas = contas.filter(vencimento__range=[inicio, fim])
    
    alunos = Aluno.objects.all()
    return render(request, 'studio/conta/listar_contas.html', {
        'contas': contas,
        'alunos':alunos,})

def registrar_conta(request):
    if request.method == 'POST':
        form = ContaReceberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta registrada com sucesso.')
            return redirect('studio:listar_contas')  # ou outro nome da view de listagem
    else:
        form = ContaReceberForm()

    contexto = {
        'form': form
    }
    return render(request, 'studio/conta/registrar_conta.html', contexto)

def editar_conta(request, pk):
    conta = get_object_or_404(ContaReceber, pk=pk)

    if request.method == 'POST':
        form = ContaReceberForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta atualizada com sucesso.')
            return redirect('studio:listar_contas')
    else:
        form = ContaReceberForm(instance=conta)

    contexto = {
        'form': form,
        'conta': conta,
    }
    return render(request, 'studio/conta/registrar_conta.html', contexto)

def registrar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.valor = pagamento.conta.valor  # valor vem da conta
            pagamento.status = 'Efetivado'
            pagamento.save()

            # Marca a conta como "pago"
            pagamento.conta.status = 'pago'
            pagamento.conta.save()

            messages.success(request, 'Pagamento registrado com sucesso.')
            return redirect('studio:listar_pagamentos')
    else:
        form = PagamentoForm()

    return render(request, 'studio/pagamento/registrar_pagamento.html', {'form': form})

def listar_pagamentos(request):
    pagamentos = Pagamento.objects.all()

    metodo = request.GET.get('metodo')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    aluno = request.GET.get('aluno')

    if metodo:
        pagamentos = pagamentos.filter(metodo_pagamento=metodo)
    if data_inicial and data_final:
        pagamentos = pagamentos.filter(data_pagamento__range=[data_inicial, data_final])
    if aluno:
        pagamentos = pagamentos.filter(conta__aluno__nome__icontains=aluno)

    return render(request, 'studio/pagamento/listar_pagamentos.html', {'pagamentos': pagamentos})

#LoginView - view pronta do Django para autenticação
class StudioLoginView(LoginView):
    template_name = 'studio/login.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('home')

def home(request):
    return render(request, 'studio/home.html')

