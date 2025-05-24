# studio/forms.py
from django import forms
from .models import Servico
from .models import Funcionario
from .models import Aluno
from .models import Plano, ContaReceber, Pagamento, Aula, AulaAluno
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField 
from django.utils import timezone
from datetime import date, datetime

 

class ServicoForm(forms.ModelForm): 
    class Meta:
        model = Servico
        fields = ['modalidade', 'niveis_dificuldade', 'descricao'] #

        widgets = {
            'modalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'niveis_dificuldade': forms.Select(attrs={'class': 'form-select'}), 
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'modalidade': 'Modalidade*',
            'niveis_dificuldade': 'Níveis de Dificuldade*', 
            'descricao': 'Descrição',
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'

NIVEL_CHOICES_FILTER = [('', 'Todos')] + Servico.NIVEIS_DIFICULDADE_CHOICES

class ServicoFilterForm(forms.Form):
    modalidade = forms.CharField(
        required=False, #
        label='Filtrar por Modalidade',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parte do nome...'})
    )
    
    niveis_dificuldade = forms.ChoiceField(
        required=False, 
        choices=NIVEL_CHOICES_FILTER,
        label='Filtrar por Nível',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class FuncionarioForm(forms.ModelForm):

    HORARIOS_CHOICES = [(f"{h:02d}:00", f"{h:02d}:00") for h in range(6, 21)]

    horarios_trabalho = forms.MultipleChoiceField(
        choices=HORARIOS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Horários de Trabalho",
        required=False,
    )

    class Meta:
        model = Funcionario
        fields = '__all__'  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Oculta campos senha e login da tela de edição
        if self.instance and self.instance.pk:
            self.fields.pop('login', None)
            self.fields.pop('senha', None)
            self.fields.pop('is_admin', None)


        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.label_class = 'form-label'
        self.helper.layout = Layout(

            # Dados Pessoais
            Fieldset(
                "Dados Pessoais",
                Row(
                    Column('nome', css_class='col-md-6'),
                    Column('cpf', css_class='col-md-6'),
                    Column('data_nascimento', css_class='col-md-6'),
                    Column('telefone', css_class='col-md-6'),
                )
            ),

            # Dados Profissionais
            Fieldset(
                "Dados Profissionais",
                Row(
                    Column('funcao', css_class='col-md-6'),
                    Column('carga_horaria', css_class='col-md-6'),
                    Column('salario', css_class='col-md-6'),
                    Column('data_contratacao', css_class='col-md-6'),
                )
            ),

            # Acesso ao Sistema
            Fieldset(
                "Acesso ao Sistema",
                Row(
                    Column('login', css_class='col-md-6'),
                    Column('senha', css_class='col-md-6'),
                    Column('is_admin', css_class='col-md-6'),
                )
            ),

            # Horários e Observações
            Fieldset(
                "Horários de Trabalho",
                'horarios_trabalho',
                'observacoes'
            ),

        )


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            'nome', 'cpf', 'rg', 'telefone', 'email', 'data_nascimento',
            'profissao', 'historico_saude', 'data_inicio_plano',
            'data_vencimento_plano', 'plano_ativo', 'evolucao', 'plano'
        ]
    plano = forms.ModelChoiceField(
        queryset=Plano.objects.all(),
        empty_label="Selecione o Plano",
        required=True,
        label="Código do Plano",
        widget=forms.Select(attrs={'class': 'form-select'}),
        to_field_name='codigo' 
    )
        
class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = ['codigo', 'nome', 'qtd_aulas', 'valor_aula', 'status', 'limite_vigencia']

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('login', 'Entrar', css_class='btn btn-primary w-100'))

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['data', 'horario', 'servicos']
        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date', 'min': date.today().isoformat()}
            ),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'servicos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Formato ISO para input date
            self.initial['data'] = self.instance.data.strftime('%Y-%m-%d')
            self.initial['horario'] = self.instance.horario.strftime('%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')

        if data and horario:
            data_hora = datetime.combine(data, horario)
            if timezone.is_naive(data_hora):
                data_hora = timezone.make_aware(data_hora)

            agora = timezone.now()

            if data_hora < agora:
                raise forms.ValidationError('Não é possível agendar aulas para datas/horários passados.')

class AulaAlunoFrequenciaForm(forms.ModelForm):
    class Meta:
        model = AulaAluno
        fields = ['frequencia']
        widgets = {
            'frequencia': forms.CheckboxInput(),
        }

class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = ['aluno', 'valor', 'vencimento', 'status']
    aluno = forms.ModelChoiceField(queryset=Aluno.objects.all(), empty_label="Selecione o aluno", widget=forms.Select)
class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['conta', 'data_pagamento', 'metodo_pagamento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas contas pendentes
        self.fields['conta'].queryset = ContaReceber.objects.filter(status='pendente')