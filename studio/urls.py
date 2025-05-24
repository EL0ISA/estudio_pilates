from django.urls import path
from . import views
from .views import StudioLoginView


app_name = 'studio'

urlpatterns = [

    #Login
    
    path('', StudioLoginView.as_view(), name='login'),

    #home
    path('home/', views.home, name='home'),

    # Serviços
    path('servicos', views.lista_servicos, name='lista_servicos'), 
    path('novo/', views.novo_servico, name='novo_servico'),
    path('editar/<int:pk>/', views.editar_servico, name='editar_servico'),
    path('excluir/<int:pk>/', views.excluir_servico, name='excluir_servico'),

    # Funcionario
    path('funcionarios/', views.listar_funcionario, name='listar_funcionario'),
    path('funcionarios/novo/', views.cadastro_funcionario, name='cadastro_funcionario'),
    path('funcionarios/editar/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/excluir/<int:id>/', views.excluir_funcionario, name='excluir_funcionario'),
    
    # Aluno
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/novo/', views.cadastro_aluno, name='cadastrar_aluno'),
    path('alunos/editar/<int:id>/', views.editar_aluno, name='editar_aluno'),
    path('alunos/excluir/<int:id>/', views.excluir_aluno, name='excluir_aluno'),

    # Plano
    path('planos/', views.listar_planos, name='listar_planos'),
    path('planos/novo/', views.cadastro_plano, name='cadastrar_plano'),
    path('planos/<int:id>/editar/', views.editar_plano, name='editar_plano'),
    path('planos/<int:id>/excluir/', views.excluir_plano, name='excluir_plano'),

    #Login
    path('login/', StudioLoginView.as_view(), name='login'),

    # Aula
    path('aulas/', views.listar_aulas, name='listar_aulas'),
    path('aulas/cadastrar/', views.cadastro_aula, name='cadastro_aula'),
    path('aulas/<int:pk>/', views.detalhes_aula, name='detalhes_aula'),
    path('aulas/<int:pk>/editar/', views.editar_aula, name='editar_aula'),
    path('aulas/<int:pk>/frequencia/', views.frequencia_aula, name='frequencia_aula'),
    path('aulas/cancelar/<int:codigo>/', views.cancelar_aula, name='cancelar_aula'),

    #Contas a receber
    path('contas/', views.listar_contas, name='listar_contas'),  
    path('contas/novo/', views.registrar_conta, name='registrar_conta'),
    path('contas/editar/<int:pk>/', views.editar_conta, name='editar_conta'),

    #Pagamentos
    path('pagamentos/novo/', views.registrar_pagamento, name='registrar_pagamento'),
    path('pagamentos/', views.listar_pagamentos, name='listar_pagamentos'),

]