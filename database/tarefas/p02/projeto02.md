# Tarefa 02 – Funções e Procedimentos

Este documento reúne as descrições e os links dos arquivos SQL criados por cada membro da equipe referentes à Tarefa 02 da disciplina de Projeto de Banco de Dados. Cada membro foi responsável por desenvolver duas funções e dois procedimentos relacionados ao projeto do estúdio de pilates.

---

## 👤 Aron

### 🔧 Função 1: 



- [Função 1]()

---

### 🔧 Função 2: 



- [Função 2]()

---

### ⚙️ Procedimento 1: 



- [Procedimento 1]()

---

### ⚙️ Procedimento 2: 



- [Procedimento 2]()

---

## 👤 Beatriz

### 🔧 Função 1: 



- [Função 1]()

---

### 🔧 Função 2: 



- [Função 2]()

---

### ⚙️ Procedimento 1: 



- [Procedimento 1]()

---

### ⚙️ Procedimento 2: 



- [Procedimento 2]()

---

## 👤 Eloisa

### 🔧 Função 1: 



- [Função 1]()

---

### 🔧 Função 2: 



- [Função 2]()

---

### ⚙️ Procedimento 1: 



- [Procedimento 1]()

---

### ⚙️ Procedimento 2: 



- [Procedimento 2]()

---

## 👤 Giovanna

### 🔧 Função 1: Soma dos pagamentos de um plano específico

Esta função recebe o código de um plano como parâmetro e retorna a soma total de todos os pagamentos realizados por alunos vinculados a esse plano. A função realiza junções entre as tabelas `pagamento`, `conta_receber` e `aluno`, considerando o campo `plano_codigo`.

- [Função 1](projeto02-giovanna-melo-q01.sql)

---

### 🔧 Função 2: Número de alunos vinculados a um plano

Esta função retorna a quantidade de alunos que estão atualmente vinculados a um determinado plano. É útil para fins administrativos, como verificar a popularidade de diferentes planos ofertados.

- [Função 2](projeto02-giovanna-melo-q02.sql)

---

### ⚙️ Procedimento 1: Registro de novo pagamento

Este procedimento registra um novo pagamento para uma conta a receber existente. Ele insere os dados do pagamento na tabela `pagamento` e atualiza o status da conta correspondente para `TRUE`, indicando que a conta foi quitada.

- [Procedimento 1](projeto02-giovanna-melo-q03.sql)

---

### ⚙️ Procedimento 2: Cancelamento de plano de um aluno

Este procedimento desativa o plano ativo de um aluno, limpando os campos de vínculo (`plano_codigo`, `data_inicio_plano`, `data_vencimento_plano`) e marcando o plano como inativo (`plano_ativo = FALSE`). É útil em casos de cancelamento ou suspensão do serviço.

- [Procedimento 2](projeto02-giovanna-melo-q04.sql)

---

## 👤 Mariana

### 🔧 Função 1: 



- [Função 1]()

---

### 🔧 Função 2: 



- [Função 2]()

---

### ⚙️ Procedimento 1: 



- [Procedimento 1]()

---

### ⚙️ Procedimento 2: 



- [Procedimento 2]()

---

## 👤 Virlânia

### 🔧 Função 1: 



- [Função 1]()

---

### 🔧 Função 2: 



- [Função 2]()

---

### ⚙️ Procedimento 1: 



- [Procedimento 1]()

---

### ⚙️ Procedimento 2: 



- [Procedimento 2]()

---
