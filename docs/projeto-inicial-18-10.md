# Projeto inicial - 18/10

**Integrantes:** Thiago Wesley Pasquim de Melo e Andre Nacamura

## 1. História escolhida e escopo

**História 1 - Prioridade Alta:** Como aluno, eu quero escolher uma disciplina, ver os horários livres e reservar um atendimento para ser atendido pelo monitor sem conflito de horário.

A história foi escolhida porque a reserva é a necessidade central do cliente, que afirma: “Se a reserva de horários funcionar, já ajuda muito.” O protótipo ficará restrito à consulta e à reserva, com os cinco critérios de aceitação registrados na etapa anterior.

A solução será desenvolvida em Python, com dados em memória, sem necessidade de interface gráfica ou entrada pelo teclado. Alunos, disciplinas e horários serão preparados previamente, permitindo que os futuros testes chamem diretamente a lógica. Cada atendimento terá duração de 30 minutos e capacidade para uma ou mais pessoas. Cadastro, cancelamento pelo monitor, notificações e relatórios não serão implementados nesta história; horários previamente marcados como cancelados serão reconhecidos nas consultas e reservas.

## 2. Classes e responsabilidades

**Aluno:** identifica quem solicita a reserva, por RA e nome.

**Disciplina:** identifica a matéria escolhida e permite agrupar seus horários.

**Horário de atendimento:** reúne disciplina, monitor responsável, data, início, capacidade e indicação de cancelamento. Calcula as vagas disponíveis pela capacidade menos as reservas existentes; se estiver cancelado, fica indisponível.

**Reserva:** associa um aluno a um horário, ocupando uma vaga. A disciplina e a data são obtidas do horário associado.

**Serviço de agendamento:** mantém os dados e oferece funções para listar disciplinas, consultar horários livres, contar reservas semanais e efetuar uma reserva. Antes de registrar, verifica a existência do aluno e do horário, o cancelamento, as vagas e o limite semanal. Uma recusa gera erro descritivo sem modificar os registros.

## 3. Fluxo e decisões iniciais

O aluno escolhe a disciplina, consulta seus horários disponíveis e solicita uma reserva. O serviço verifica novamente as condições e, se forem atendidas, registra a reserva; a disponibilidade diminui em uma vaga. Se alguma condição falhar, os dados permanecem iguais.

O cliente ainda não definiu o limite semanal. Para respeitar a história já escrita, será adotado provisoriamente o limite configurável de uma reserva por aluno na mesma disciplina. A semana será de segunda-feira a domingo, conforme a data do atendimento. Reservas de horários cancelados não contarão para esse limite, permitindo novo agendamento.

## 4. Previsão dos testes por critério de aceitação

Os testes de aceitação serão implementados posteriormente com unittest. A previsão abaixo faz parte do projeto inicial exigido no passo 5 do enunciado.

1. **Listar apenas horários da disciplina com vagas:** o teste de consulta preparará horários de duas disciplinas, incluindo um lotado e um cancelado. Espera-se somente o horário disponível da disciplina escolhida.
2. **Registrar a reserva e diminuir uma vaga:** o teste de reserva válida usará um horário com duas vagas. Espera-se uma reserva vinculada ao aluno e uma vaga restante.
3. **Recusar horário sem vagas:** o teste de lotação tentará reservar um horário cheio. Espera-se erro, sem criar ou alterar reservas.
4. **Recusar horário cancelado:** o teste de cancelamento tentará reservar um horário cancelado com capacidade restante. Espera-se erro e nenhuma nova reserva.
5. **Respeitar o limite semanal configurável:** os testes do limite verificarão a recusa da segunda reserva na mesma disciplina e semana, a permissão em outra semana ou disciplina e a permissão da segunda reserva quando o limite for alterado para dois.

O detalhamento dos testes fica para 19/10, conforme o cronograma