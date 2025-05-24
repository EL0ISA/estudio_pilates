# studio/models.py
from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.hashers import make_password, check_password


class Servico(models.Model):

    # Opções para niveis_dificuldade
    NIVEIS_DIFICULDADE_CHOICES = [
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    ]

    modalidade = models.CharField(max_length=50) # Not Null por padrão (null=False, blank=False)
    niveis_dificuldade = models.CharField(
        max_length=30,
        choices=NIVEIS_DIFICULDADE_CHOICES # Usando as choices definidas acima
        # blank=False, null=False por padrão, atendendo "Not Null"
    )
    descricao = models.TextField(blank=True, null=True) # Mantido como opcional

    def __str__(self):
        return f"{self.modalidade} ({self.niveis_dificuldade})" # Sugestão para melhorar o __str__

class Pessoa(models.Model):
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    data_nascimento = models.DateField()
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True  # Isso define a herança abstrata

    def calcular_idade(self):
        today = date.today()
        return today.year - self.data_nascimento.year - (
            (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

class Funcionario(Pessoa):
    funcao = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=4)
    carga_horaria = models.FloatField()
    horarios_trabalho = models.TextField(blank=True)
    login = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    ultimo_acesso =  models.DateTimeField(default=timezone.now, editable=False)

    def autenticar(self, senha: str) -> bool:
        return check_password(senha, self.senha)

    # Vai calcular a carga horária a partir da quantidade de horários no array, e dps multiplica pelos dias da semana, retornando a carga horária semanal.
    def gerar_carga_horaria(self, horarios_trabalho: list) -> int:
        return len(horarios_trabalho) * 5 
    
    # Altera a carga horária com base nas horas extras trabalhadas
    def alterar_carga_horaria(self, horas_extras: float = 0.0) -> float:
        self.carga_horaria += horas_extras
        self.save()  # Salva automaticamente no banco de dados
        return self.carga_horaria

    def save(self, *args, **kwargs):
        if not self.senha.startswith('pbkdf2_sha256$'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.login} ({self.funcao}) ({self.nome})"
    
    
class Plano(models.Model):
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    qtd_aulas = models.IntegerField()
    valor_aula = models.FloatField()
    status = models.BooleanField(default=True)
    limite_vigencia = models.DateField()

    def __str__(self):
        return f"{self.nome} (Código: {self.codigo})"

class Aluno(Pessoa):
    profissao = models.CharField(max_length=100)
    historico_saude = models.TextField()
    data_inicio_plano = models.DateField()
    data_vencimento_plano = models.DateField()
    plano = models.ForeignKey('studio.Plano', on_delete=models.SET_NULL, null=True, blank=True)
    plano_ativo = models.BooleanField(default=True)
    evolucao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.cpf} ({self.nome})"

class Aula(models.Model):
    # agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE)  # aguardando implementação de agendamento
    servicos = models.ManyToManyField(Servico)
    codigo = models.AutoField(primary_key=True)
    data = models.DateField()
    horario = models.TimeField()
    cancelada = models.BooleanField(default=False)

    def __str__(self):
        return f'Aula {self.codigo} em {self.data} às {self.horario}'

    def cancelar(self, motivo=None):
        """Marca a aula como cancelada."""
        self.cancelada = True
        self.save()

    # def gerar_participacoes(self):
    #     """Cria entradas de AulaAluno para todos os alunos do agendamento."""
    #     alunos = self.agendamento.alunos.all()
    #     for aluno in alunos:
    #         AulaAluno.objects.get_or_create(aula=self, aluno=aluno)

    def alunos_confirmados(self):
        return self.participacoes.filter(frequencia=True).values_list('aluno', flat=True)

    def total_presentes(self):
        return self.participacoes.filter(frequencia=True).count()

    def total_ausentes(self):
        return self.participacoes.filter(frequencia=False).count()

    def lista_alunos(self):
        return [p.aluno for p in self.participacoes.all()]


class AulaAluno(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='participacoes')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    frequencia = models.BooleanField(default=False)

    def __str__(self):
        return f'Aluno {self.aluno} na Aula {self.aula}'

    def marcar_presenca(self):
        self.frequencia = True
        self.save()

    def marcar_ausencia(self):
        self.frequencia = False
        self.save()

    def status_presenca(self):
        return 'Presente' if self.frequencia else 'Ausente'

class ContaReceber(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"Conta de {self.aluno} - {self.vencimento} - {self.status.upper()}"
    
    @property
    def estado_atual(self):
        if self.status == 'pago':
            return 'Pago'
        elif self.vencimento < date.today():
            return 'Vencido'
        else:
            return 'Pendente'

class Pagamento(models.Model):
    METODOS = [
        ('PIX', 'PIX'),
        ('Cartão', 'Cartão'),
        ('Dinheiro', 'Dinheiro'),
        ('Transferência', 'Transferência'),
    ]

    conta = models.OneToOneField(ContaReceber, on_delete=models.CASCADE)
    data_pagamento = models.DateField()
    metodo_pagamento = models.CharField(max_length=20, choices=METODOS)
    valor = models.DecimalField(max_digits=8, decimal_places=2)  # Mesmo tamanho da conta
    status = models.CharField(max_length=20, default='Efetivado')

    def __str__(self):
        return f'Pagamento #{self.id} - {self.conta}'
