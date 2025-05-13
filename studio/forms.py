# studio/forms.py
from django import forms
from .models import Servico, Funcionario, Aluno, Plano, ContaReceber, Pagamento
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField 
 

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['modalidade', 'niveis_dificuldade', 'descricao'] # Atualizado o nome do campo

        widgets = {
            'modalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'niveis_dificuldade': forms.Select(attrs={'class': 'form-select'}), # Mudado para Select por causa do 'choices' no model
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'modalidade': 'Modalidade*',
            'niveis_dificuldade': 'Níveis de Dificuldade*', # Atualizado nome e label (adicionado *)
            'descricao': 'Descrição',
        }

# Prepara as opções para o filtro de nível, adicionando uma opção "Todos"
NIVEL_CHOICES_FILTER = [('', 'Todos')] + Servico.NIVEIS_DIFICULDADE_CHOICES

class ServicoFilterForm(forms.Form):
    # Campo para buscar texto dentro da modalidade
    modalidade = forms.CharField(
        required=False, # Não obrigatório
        label='Filtrar por Modalidade',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parte do nome...'})
    )
    # Campo para selecionar um nível de dificuldade específico
    niveis_dificuldade = forms.ChoiceField(
        required=False, # Não obrigatório
        choices=NIVEL_CHOICES_FILTER, # Usa a lista com a opção "Todos"
        label='Filtrar por Nível',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
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
                    Column('senha_hash', css_class='col-md-6'),
                    Column('is_admin', css_class='col-md-6'),
                )
            ),

            # Horários e Observações
            Fieldset(
                "Horários de Trabalho",
                'horarios_trabalho',
                'observacoes'
            ),

            # Botão de envio (opcional — pode deixar no template)
            Submit('submit', 'Salvar Funcionário', css_class='btn btn-primary mt-3')
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

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('login', 'Entrar', css_class='btn btn-primary w-100'))