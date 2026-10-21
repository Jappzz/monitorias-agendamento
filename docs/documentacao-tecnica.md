# Documentação técnica

**Integrantes:** Thiago Wesley Pasquim de Melo e Andre Nacamura.

## 1. Histórias de usuário

No início do trabalho, escrevemos estas cinco histórias. Escolhemos a História 1 para fazer no programa.

### 1.1. Reserva de atendimento

Como aluno, eu quero escolher uma disciplina, ver os horários livres e reservar um atendimento para ser atendido pelo monitor sem conflito de horário.

**Critérios de aceitação:**

- CA1: Mostrar só os horários da disciplina escolhida que ainda têm vagas.
- CA2: Ao reservar, registrar o aluno no horário e diminuir uma vaga.
- CA3: Se o horário estiver lotado, mostrar um erro e não mudar as reservas existentes.
- CA4: Se o horário estiver cancelado, não permitir a reserva e mostrar um erro.
- CA5: Permitir no máximo uma reserva por aluno na mesma disciplina por semana. Esse limite pode ser alterado.

**Prioridade: Alta.** A reserva é a parte principal do sistema e ajuda a distribuir os alunos entre os horários disponíveis.

**Trechos do e-mail:**

> A ideia é que o aluno escolha a disciplina, veja os horários livres e reserve um atendimento.

> Não precisa resolver tudo de uma vez. Se a reserva de horários funcionar, já ajuda muito.

### 1.2. Cancelamento pelo monitor

Como monitor, eu quero cancelar um horário em que não posso atender para que os alunos reservados sejam avisados antes de chegarem à sala.

**Critérios de aceitação:**

- O monitor só pode cancelar os próprios horários.
- O horário fica marcado como cancelado e sai da lista de horários livres.
- Os alunos que reservaram esse horário recebem um aviso de cancelamento.
- Tentar cancelar o mesmo horário de novo gera erro.

**Prioridade: Alta.** Evita que os alunos cheguem à sala sem saber que o atendimento foi cancelado.

**Trecho do e-mail:**

> às vezes precisa cancelar por causa de prova. Os alunos reclamam que só descobrem o cancelamento quando chegam na sala.

### 1.3. Cadastro de horários

Como monitor, eu quero cadastrar os horários em que posso atender, definindo o número de vagas, para que os alunos possam reservá-los em atendimento individual ou em grupo.

**Critérios de aceitação:**

- Informar a disciplina, o dia e a hora de início. O atendimento dura 30 minutos.
- Não permitir horários que se sobreponham para o mesmo monitor.
- O horário precisa ter pelo menos uma vaga. Uma vaga significa atendimento individual; mais de uma, em grupo. Zero ou menos vagas gera erro.
- O horário cadastrado aparece na consulta de horários livres.

**Prioridade: Média.** Precisamos dos horários para reservar, mas na primeira versão podemos deixar os dados preparados no código.

**Trechos do e-mail:**

> No início do semestre, cada monitor informa os horários em que pode atender.

> Cada atendimento dura 30 minutos, mas alguns monitores preferem atender em grupo, quando várias pessoas têm a mesma dúvida.

### 1.4. Relatório de horas dos monitores

Como coordenador, eu quero consultar o histórico e o total mensal de horas atendidas por cada monitor para contabilizar e pagar as bolsas.

**Critérios de aceitação:**

- Somar as horas atendidas por cada monitor no mês escolhido.
- Não contar atendimentos cancelados.
- Só o coordenador pode acessar o relatório. Outros usuários recebem um erro de permissão.
- Se não houver atendimentos no mês, mostrar zero horas, sem gerar erro.

**Prioridade: Média.** A coordenação precisa dessas informações para as bolsas, mas primeiro precisamos registrar os atendimentos.

**Trecho do e-mail:**

> A coordenação precisa de um relatório mensal com as horas atendidas por cada monitor, porque isso conta para o pagamento da bolsa. Essas informações de bolsa não podem ficar visíveis para todo mundo.

### 1.5. Consulta dos conteúdos com mais dúvidas

Como professor, eu quero ver quais conteúdos geraram mais atendimentos na minha disciplina para reforçá-los em sala de aula.

**Critérios de aceitação:**

- O monitor registra o conteúdo depois do atendimento.
- Mostrar os conteúdos da disciplina do professor, do mais atendido para o menos atendido.
- O professor não pode consultar os conteúdos de outras disciplinas.
- Agrupar atendimentos sem conteúdo registrado como "Não informado".

**Prioridade: Baixa.** Ajuda o professor a preparar as aulas, mas o sistema de reservas funciona sem essa parte.

**Trecho do e-mail:**

> Os professores das disciplinas gostariam de saber quais conteúdos geram mais dúvidas, para reforçar em aula.

## 2. Testes de aceitação

*Em elaboração.*
