from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q, F 
from django.db import models 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView  
from .models import Servico
from .forms import ServicoForm, ServicoFilterForm
from .models import Funcionario
from .forms import FuncionarioForm
from .models import Aluno
from .forms import AlunoForm
from .models import Plano, ContaReceber, Pagamento, Aula, AulaAluno, HorarioDisponivel, Agendamento
from .forms import PlanoForm, ContaReceberForm, PagamentoForm, AulaForm, AulaAlunoFrequenciaForm, HorarioDisponivelForm, AgendamentoForm
from .forms import CustomLoginForm
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.views import View
from django.http import HttpResponseNotAllowed
from django.db.models import ProtectedError


LISTAR_SERVICOS = 'studio:lista_servicos'
LISTAR_FUNCIONARIO = 'studio:listar_funcionario'
LISTAR_ALUNOS = 'studio:listar_alunos'
LISTAR_PLANOS = 'studio:listar_planos'
LISTAR_AULAS = 'studio:listar_aulas'
DETALHES_AULA = 'studio:detalhes_aula'
LISTAR_CONTAS = 'studio:listar_contas'
LISTAR_PAGAMENTOS = 'studio:listar_pagamentos'
LISTAR_HORARIOS = 'studio:listar_horarios'
LISTAR_AGENDAMENTOS = 'studio:listar_agendamentos'


#View Serviços

class ServicoListView(ListView):
    model = Servico
    template_name = 'studio/servicos/listar_servicos.html'
    context_object_name = 'lista_servicos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('modalidade')
        self.filter_form = ServicoFilterForm(self.request.GET or None)

        if self.filter_form.is_valid():
            modalidade = self.filter_form.cleaned_data.get('modalidade')
            niveis = self.filter_form.cleaned_data.get('niveis_dificuldade')

            if modalidade:
                queryset = queryset.filter(modalidade__icontains=modalidade)

            if niveis:
                queryset = queryset.filter(niveis_dificuldade=niveis)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context


class ServicoCreateView(CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'studio/servicos/cadastrar_servicos.html'
    success_url = reverse_lazy(LISTAR_SERVICOS)

    def form_valid(self, form):
        messages.success(self.request, "Serviço cadastrado com sucesso!")
        return super().form_valid(form)


class ServicoUpdateView(UpdateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'studio/servicos/cadastrar_servicos.html'
    success_url = reverse_lazy(LISTAR_SERVICOS)

    def form_valid(self, form):
        messages.success(self.request, "Serviço atualizado com sucesso!")
        return super().form_valid(form)


class ServicoDeleteView(DeleteView):
    model = Servico
    template_name = 'studio/servicos/confirmar_exclusao_servico.html'
    success_url = reverse_lazy(LISTAR_SERVICOS)

    def form_valid(self, form):
        nome_servico = self.object.modalidade
        messages.success(self.request, f'Serviço "{nome_servico}" excluído com sucesso.')
        return super().form_valid(form)

# View Funcionario

@require_http_methods(["GET", "POST"])
def cadastro_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_FUNCIONARIO)
    else:
        form = FuncionarioForm()
    return render(request, 'studio/funcionario/cadastro_funcionario.html', {'form': form})


@require_GET
def listar_funcionario(request):
    funcionario = Funcionario.objects.all()
    return render(request, 'studio/funcionario/listar_funcionario.html', {'funcionario': funcionario})


@require_http_methods(["GET", "POST"])
def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
        return redirect(LISTAR_FUNCIONARIO)
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'studio/funcionario/editar_funcionario.html', {'form': form, 'funcionario': funcionario})


@require_POST
def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    try:
        funcionario.delete()
        messages.success(request, "Funcionário excluído com sucesso!")
    except ProtectedError:
        messages.error(request, f"Não é possível excluir o funcionário '{funcionario.nome}' porque ele está vinculado a uma ou mais aulas.")
    return redirect('studio:listar_funcionario')


# View Aluno

class AlunoListView(ListView):
    model = Aluno
    template_name = 'studio/aluno/listar_alunos.html'
    context_object_name = 'alunos'
    
    def get_queryset(self):
        qs = super().get_queryset()
        nome = self.request.GET.get('nome')
        cpf = self.request.GET.get('cpf')
        status = self.request.GET.get('status') 
        if nome:
            qs = qs.filter(nome__icontains=nome) 
        if cpf:
            qs = qs.filter(cpf=cpf)
        if status:
            if status == 'ativos':
                qs = qs.filter(plano_ativo=True)
            elif status == 'inativos':
                qs = qs.filter(plano_ativo=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'nome_filtro': self.request.GET.get('nome', ''),
            'cpf_filtro': self.request.GET.get('cpf', ''),
            'status_filtro': self.request.GET.get('status', ''),
        })
        return ctx



class AlunoCreateView(CreateView):
    model = Aluno
    form_class = AlunoForm
    template_name = 'studio/aluno/cadastrar_aluno.html'
    success_url = reverse_lazy(LISTAR_ALUNOS)
    def dispatch(self, request, *args, **kwargs):
        if not Plano.objects.exists():
            messages.warning(request, 'Você precisa cadastrar pelo menos um plano antes de adicionar um aluno.')
            return redirect(LISTAR_PLANOS)
        return super().dispatch(request, *args, **kwargs)


class AlunoUpdateView(UpdateView):
    model = Aluno
    form_class = AlunoForm
    template_name = 'studio/aluno/editar_aluno.html'
    success_url = reverse_lazy(LISTAR_ALUNOS)
    pk_url_kwarg = 'id'


class AlunoDeleteView(DeleteView):
    model = Aluno
    template_name = 'studio/aluno/confirmar_exclusao_aluno.html'
    success_url = reverse_lazy(LISTAR_ALUNOS)
    pk_url_kwarg = 'id'

    def delete(self, request, *args, **kwargs):
        aluno = self.get_object()
        aluno.delete()
        messages.success(request, "Aluno excluído com sucesso!")
        return redirect(self.success_url)



class EvolucoesAlunoView(View):
    template_name = "studio/aluno/evolucoes_aluno.html"
    http_method_names = ["get"] 

    def get(self, request, id):
        aluno = get_object_or_404(Aluno, id=id)
        participacoes = (
            AulaAluno.objects.filter(aluno=aluno)
            .exclude(evolucao_na_aula__isnull=True)
            .exclude(evolucao_na_aula__exact="")
            .select_related("aula")
            .order_by("-aula__data")
        )
        evolucoes = [(p.aula, p.evolucao_na_aula) for p in participacoes]
        return render(
            request,
            self.template_name,
            {"aluno": aluno, "evolucoes": evolucoes},
        )


# View Plano

class PlanoListView(ListView):
    model = Plano
    template_name = 'studio/plano/listar_planos.html'
    context_object_name = 'planos'

    def get_queryset(self):
        qs = super().get_queryset()
        codigo = self.request.GET.get('codigo')
        nome = self.request.GET.get('nome')
        status = self.request.GET.get('status')
        if codigo:
            qs = qs.filter(codigo=codigo)
        if nome:
            qs = qs.filter(nome__icontains=nome) 
        if status:
            if status == 'ativos':
                qs = qs.filter(status=True)
            elif status == 'inativos':
                qs = qs.filter(status=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'codigo_filtro': self.request.GET.get('codigo', ''),
            'nome_filtro': self.request.GET.get('nome', ''),
            'status_filtro': self.request.GET.get('status', ''),
        })
        return ctx

class PlanoCreateView(CreateView):
    model = Plano
    form_class = PlanoForm
    template_name = 'studio/plano/cadastrar_plano.html'
    success_url = reverse_lazy(LISTAR_PLANOS)


class PlanoUpdateView(UpdateView):
    model = Plano
    form_class = PlanoForm
    template_name = 'studio/plano/editar_plano.html'
    success_url = reverse_lazy(LISTAR_PLANOS)
    slug_field = 'codigo'
    slug_url_kwarg = 'codigo'


class PlanoDeleteView(DeleteView):
    model = Plano
    template_name = 'studio/plano/confirmar_exclusao_plano.html'
    success_url = reverse_lazy(LISTAR_PLANOS)
    slug_field = 'codigo'
    slug_url_kwarg = 'codigo'

    def delete(self, request, *args, **kwargs):
        plano = self.get_object()
        plano.delete()
        messages.success(request, "Plano excluído com sucesso!")
        return redirect(self.success_url)

# Views aula

class AulaListView(ListView):
    template_name = "studio/aula/listar_aulas.html"
    context_object_name = "aulas"
    model = Aula

    def get_queryset(self):
        qs = super().get_queryset()
        data = self.request.GET.get("data")
        horario = self.request.GET.get("horario")
        status = self.request.GET.get("status")

        if status == "ativas":
            qs = qs.filter(cancelada=False)
        elif status == "canceladas":
            qs = qs.filter(cancelada=True)

        if data:
            qs = qs.filter(data=data)
            if horario:
                qs = qs.filter(horario=horario)
        elif horario:
            messages.warning(self.request, "Para filtrar por horário, você deve informar a data.")
            qs = qs.none()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "data": self.request.GET.get("data", ""),
            "horario": self.request.GET.get("horario", ""),
            "status": self.request.GET.get("status", ""),
        })
        return ctx


class AulaDetailView(DetailView):
    template_name = "studio/aula/detalhar_aula.html"
    model = Aula
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["participacoes"] = AulaAluno.objects.filter(aula=self.object)
        return ctx


class FrequenciaAulaView(View):
    template_name = "studio/aula/frequencia_aula.html"

    def get(self, request, pk):
        aula = get_object_or_404(Aula, pk=pk)
        formset = self._criar_formset(instance=aula)
        return self._render(request, aula, formset)

    def post(self, request, pk):
        aula = get_object_or_404(Aula, pk=pk)
        formset = self._criar_formset(request.POST, aula)
        if formset.is_valid():
            for form in formset:
                inst = form.save(commit=False)
                inst.aula = aula
                inst.save()
            messages.success(request, "Frequência e evolução salvas com sucesso.")
            return redirect(DETALHES_AULA, pk=aula.pk)

        for form in formset:
            for errors in form.errors.values():
                for err in errors:
                    messages.error(request, err)
        return self._render(request, aula, formset)

    @staticmethod
    def _criar_formset(data=None, instance=None):
        form_set = modelformset_factory(AulaAluno, form=AulaAlunoFrequenciaForm, extra=0)
        qs = AulaAluno.objects.filter(aula=instance)
        return form_set(data, queryset=qs) if data else form_set(queryset=qs)

    def _render(self, request, aula, formset):
        return render(request, self.template_name, {"aula": aula, "formset": formset})


class AulaCreateView(CreateView):
    template_name = "studio/aula/cadastrar_aula.html"
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy("studio:listar_aulas")

    def form_valid(self, form):
        messages.success(self.request, "Aula cadastrada com sucesso.")
        return super().form_valid(form)


class AulaUpdateView(UpdateView):
    template_name = "studio/aula/editar_aula.html"
    model = Aula
    form_class = AulaForm
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        aula = self.get_object()
        if aula.cancelada:
            messages.error(request, "Não é possível editar uma aula cancelada.")
            return redirect(DETALHES_AULA, pk=aula.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Aula atualizada com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(DETALHES_AULA, kwargs={"pk": self.object.pk})


class AulaCancelView(View):
    http_method_names = ["post"]

    def post(self, request, codigo):
        aula = get_object_or_404(Aula, codigo=codigo)
        aula.cancelada = True
        aula.save()
        messages.success(request, f"Aula {aula.codigo} foi cancelada com sucesso.")
        return redirect("studio:listar_aulas")


# Views contas/pagamentos

class ContaReceberListView(ListView):
    model = ContaReceber
    template_name = 'studio/conta/listar_contas.html'
    context_object_name = 'contas'

    def get_queryset(self):
        contas = super().get_queryset()
        aluno_id = self.request.GET.get('aluno')
        estado = self.request.GET.get('estado')
        inicio = self.request.GET.get('inicio')
        fim = self.request.GET.get('fim')

        if aluno_id:
            contas = contas.filter(aluno_id=aluno_id)
        if estado:
            estado = estado.lower()
            if estado == 'vencido':
                contas = contas.filter(vencimento__lt=date.today()).exclude(status='pago')
            elif estado in ['pendente', 'pago']:
                contas = contas.filter(status=estado)
        if inicio and fim:
            contas = contas.filter(vencimento__range=[inicio, fim])
        return contas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alunos'] = Aluno.objects.all()
        return context

class ContaReceberCreateView(CreateView):
    model = ContaReceber
    form_class = ContaReceberForm
    template_name = 'studio/conta/registrar_conta.html'
    success_url = reverse_lazy(LISTAR_CONTAS)

    def form_valid(self, form):
        messages.success(self.request, 'Conta registrada com sucesso.')
        return super().form_valid(form)

class ContaReceberUpdateView(UpdateView):
    model = ContaReceber
    form_class = ContaReceberForm
    template_name = 'studio/conta/registrar_conta.html'
    success_url = reverse_lazy(LISTAR_CONTAS)

    def dispatch(self, request, *args, **kwargs):
        conta = self.get_object()
        if conta.status.lower() == 'pago':
            messages.warning(request, 'Esta conta já foi paga e não pode mais ser editada.')
            return redirect(LISTAR_CONTAS)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.aluno = self.get_object().aluno
        messages.success(self.request, 'Conta atualizada com sucesso.')
        return super().form_valid(form)

class ContaReceberDeleteView(View):
    def post(self, request, pk):
        conta = get_object_or_404(ContaReceber, pk=pk)
        conta.delete()
        messages.success(request, "Conta excluída com sucesso!")
        return redirect(LISTAR_CONTAS)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

class ContaReceberDetailView(DetailView):
    model = ContaReceber
    template_name = 'studio/conta/detalhar_conta.html'
    context_object_name = 'conta'

class PagamentoListView(ListView):
    model = Pagamento
    template_name = 'studio/pagamento/listar_pagamentos.html'
    context_object_name = 'pagamentos'

    def get_queryset(self):
        pagamentos = super().get_queryset()
        metodo = self.request.GET.get('metodo')
        data_inicial = self.request.GET.get('data_inicial')
        data_final = self.request.GET.get('data_final')
        aluno = self.request.GET.get('aluno')

        if metodo:
            pagamentos = pagamentos.filter(metodo_pagamento=metodo)
        if data_inicial and data_final:
            pagamentos = pagamentos.filter(data_pagamento__range=[data_inicial, data_final])
        if aluno:
            pagamentos = pagamentos.filter(conta__aluno__nome__icontains=aluno)

        return pagamentos
    
class PagamentoCreateView(CreateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'studio/pagamento/registrar_pagamento.html'
    success_url = reverse_lazy(LISTAR_PAGAMENTOS)

    def get_initial(self):
        initial = super().get_initial()
        conta_id = self.request.GET.get('conta_id')
        if conta_id:
            conta = get_object_or_404(ContaReceber, id=conta_id)
            initial.update({
                'conta': conta,
                'data_pagamento': timezone.now().date().strftime('%Y-%m-%d'),
            })
        return initial

    def form_valid(self, form):
        pagamento = form.save(commit=False)
        pagamento.valor = pagamento.conta.valor
        pagamento.status = 'Efetivado'
        pagamento.save()

        pagamento.conta.status = 'pago'
        pagamento.conta.save()

        messages.success(self.request, 'Pagamento registrado com sucesso.')
        return redirect(self.success_url)

class PagamentoDetailView(DetailView):
    model = Pagamento
    template_name = 'studio/pagamento/detalhar_pagamento.html'
    context_object_name = 'pagamento'

# LoginView (usado para login real)
#class StudioLoginView(LoginView):
    #template_name = 'studio/login.html'
    #authentication_form = AuthenticationForm
    #next_page = reverse_lazy('home')

# Login direto (para entrar sem autenticação real)
def login_view_simples(request):
    # Se o usuário enviou o formulário (clicou em Entrar)
    if request.method == 'POST':
        # Redireciona direto para a página 'home'sem verificar nada.
        return redirect('studio:home') 
    return render(request, 'studio/login.html')

# Views Horarios/Agendamento

@require_GET
def listar_horarios(request):
    horarios = HorarioDisponivel.objects.filter(
        data__gte=date.today()
    ).order_by('data', 'horario_inicio').select_related('servico', 'funcionario')

    context = {
        'horarios': horarios,
        'hoje': date.today(),
    }

    return render(request, 'studio/agendamento/listar_horarios.html', context)


@require_http_methods(["GET", "POST"])
def agendar_aluno(request, horario_id):
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)

    if horario.esta_cheio:
        messages.error(request, 'Este horário não possui mais vagas disponíveis. Vagas esgotadas.')
        return redirect(LISTAR_HORARIOS)

    if request.method == 'POST':
        aluno_id = request.POST.get('aluno_id')
        try:
            aluno = Aluno.objects.get(id=aluno_id)

            agendamento, created = Agendamento.objects.get_or_create(
                horario_disponivel=horario,
                aluno=aluno,
                defaults={'cancelado': False}
            )

            if not created and agendamento.cancelado:
                agendamento.reativar_agendamento()
                messages.success(request, f'Agendamento de {aluno.nome} reativado com sucesso para {horario}.')
            elif created:
                messages.success(request, f'Aluno {aluno.nome} agendado com sucesso para {horario}.')
            else:
                messages.info(request, f'Aluno {aluno.nome} já está agendado para {horario}.')

        except Aluno.DoesNotExist:
            messages.error(request, 'Aluno não encontrado. Por favor, selecione um aluno válido.')
        except Exception as e:
            messages.error(request, f'Erro ao agendar: {e}.')

        return redirect(LISTAR_HORARIOS)

    alunos = Aluno.objects.all().order_by('nome')
    context = {
        'horario': horario,
        'alunos': alunos,
    }
    return render(request, 'studio/agendamento/agendar_aluno.html', context)


@require_GET
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.select_related('horario_disponivel', 'aluno').order_by(
        'horario_disponivel__data', 'horario_disponivel__horario_inicio', 'aluno__nome'
    )

    query_aluno = request.GET.get('aluno_nome', '').strip()
    if query_aluno:
        agendamentos = agendamentos.filter(aluno__nome__icontains=query_aluno)
        if not agendamentos.exists() and query_aluno:
            messages.info(request, f'Nenhum agendamento encontrado para o aluno "{query_aluno}".')

    query_data = request.GET.get('data_aula')
    if query_data:
        try:
            parsed_date = datetime.strptime(query_data, '%Y-%m-%d').date()
            agendamentos = agendamentos.filter(horario_disponivel__data=parsed_date)
        except ValueError:
            messages.error(request, 'Formato de data inválido para pesquisa. Use AAAA-MM-DD.')

    context = {
        'agendamentos': agendamentos,
        'query_aluno': query_aluno,
        'query_data': query_data,
    }
    return render(request, 'studio/agendamento/listar_agendamentos.html', context)


@require_http_methods(["GET", "POST"])
def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect(LISTAR_AGENDAMENTOS)
        else:
            messages.error(request, 'Erro ao atualizar agendamento. Verifique os dados e tente novamente.')
    else:
        form = AgendamentoForm(instance=agendamento)

    context = {
        'form': form,
        'agendamento': agendamento,
    }
    return render(request, 'studio/agendamento/editar_agendamento.html', context)

@require_http_methods(["GET", "POST"])
def excluir_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method == 'POST':
        motivo = request.POST.get('motivo_cancelamento', '').strip()
        if not agendamento.cancelado:
            agendamento.cancelar_agendamento(motivo=motivo)
            messages.success(
                request,
                f'Agendamento de {agendamento.aluno.nome} em {agendamento.horario_disponivel} cancelado com sucesso. A vaga foi liberada.'
            )
        else:
            messages.info(request, 'Este agendamento já estava cancelado.')
        return redirect(LISTAR_AGENDAMENTOS)

    return render(request, 'studio/agendamento/excluir_agendamento.html', {'agendamento': agendamento})

@require_http_methods(["GET", "POST"])
def cadastrar_horario_disponivel(request):
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário disponível cadastrado com sucesso!')
            return redirect(LISTAR_HORARIOS)
        else:
            messages.error(request, 'Erro ao cadastrar horário. Verifique os dados e tente novamente.')
    else:
        form = HorarioDisponivelForm()

    context = {
        'form': form,
    }
    return render(request, 'studio/agendamento/cadastrar_horario_disponivel.html', context)


@require_http_methods(["GET", "POST"])
def editar_horario(request, horario_id):
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)

    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário disponível atualizado com sucesso!')
            return redirect(LISTAR_HORARIOS)
        else:
            messages.error(request, 'Erro ao atualizar horário. Verifique os dados e tente novamente.')
    else:
        form = HorarioDisponivelForm(instance=horario)

    context = {
        'form': form,
        'horario': horario,
    }
    return render(request, 'studio/agendamento/editar_horario.html', context)


@require_http_methods(["GET", "POST"])
def excluir_horario(request, horario_id):
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)

    agendamentos_ativos = horario.agendamentos.filter(cancelado=False).exists()

    if request.method == 'POST':
        if agendamentos_ativos:
            messages.error(request, 'Não é possível excluir este horário porque existem agendamentos ativos vinculados a ele.')
            return redirect(LISTAR_HORARIOS)
        else:
            horario.delete()
            messages.success(request, 'Horário disponível excluído com sucesso!')
            return redirect(LISTAR_HORARIOS)

    return render(request, 'studio/agendamento/excluir_horario.html', {'horario': horario})

@require_GET
def home(request):
    hoje = date.today()
    agora = timezone.now()

    total_alunos_ativos = Aluno.objects.filter(status=True).count()

    aulas_com_vagas_hoje = HorarioDisponivel.objects.filter(
        data=hoje,
    ).annotate(
        agendamentos_ativos_count=Count('agendamentos', filter=Q(agendamentos__cancelado=False))
    ).filter(
        agendamentos_ativos_count__lt=models.F('capacidade_maxima')
    ).count()

    contas_em_atraso_qtd = ContaReceber.objects.filter(
        vencimento__lt=hoje,
        status='pendente'
    ).count()

    contas_em_atraso_valor = ContaReceber.objects.filter(
        vencimento__lt=hoje,
        status='pendente'
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    data_vencimento_proximo = hoje + timedelta(days=7)
    contas_a_vencer_proximo_valor = ContaReceber.objects.filter(
        vencimento__range=(hoje, data_vencimento_proximo),
        status='pendente'
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    # monta texto para aviso
    texto_vencimentos = None
    if contas_a_vencer_proximo_valor > 0:
        texto_vencimentos = f"Há R$ {contas_a_vencer_proximo_valor:.2f} em contas que vencem nos próximos 7 dias."

    proximos_agendamentos_hoje = Agendamento.objects.filter(
        horario_disponivel__data=hoje,
        horario_disponivel__horario_inicio__gte=agora.time(),
        cancelado=False
    ).select_related('aluno', 'horario_disponivel__funcionario').order_by('horario_disponivel__horario_inicio')

    aniversariantes_mes = Aluno.objects.filter(
        data_nascimento__month=hoje.month,
        status=True 
    ).order_by('data_nascimento__day')

    aulas_confirmadas_hoje = Aula.objects.filter(
        data=hoje,
        cancelada=False
    ).count()

    faltas_hoje = AulaAluno.objects.filter(
        aula__data=hoje,
        frequencia=False
    ).count()

    context = {
        'dashboard_data': {
            'total_alunos_ativos': total_alunos_ativos,
            'aulas_com_vagas': aulas_com_vagas_hoje,
            'contas_a_receber': contas_em_atraso_valor + contas_a_vencer_proximo_valor,
            'aulas_confirmadas_hoje': aulas_confirmadas_hoje,
            'faltas_hoje': faltas_hoje,
            'proximos_agendamentos': [
                {
                    'id': ag.id,
                    'data': ag.horario_disponivel.data.strftime('%d/%m/%Y'),
                    'hora_inicio': ag.horario_disponivel.horario_inicio.strftime('%H:%M'),
                    'servico': ag.horario_disponivel.servico.modalidade if ag.horario_disponivel.servico else 'N/A',
                    'instrutor': ag.horario_disponivel.funcionario.nome if ag.horario_disponivel.funcionario else 'N/A',
                    'aluno_nome': ag.aluno.nome,
                } for ag in proximos_agendamentos_hoje
            ],
            'aniversariantes_mes': [
                {'nome': aluno.nome, 'aniversario': aluno.data_nascimento}
                for aluno in aniversariantes_mes
            ],
            'alertas_financeiros': {
                'contas_em_atraso': contas_em_atraso_qtd,
                'proximos_vencimentos': texto_vencimentos,
                'inicio': hoje.strftime('%Y-%m-%d'),
                'fim': data_vencimento_proximo.strftime('%Y-%m-%d'),
            }
        }
    }
    return render(request, 'studio/home.html', context)
