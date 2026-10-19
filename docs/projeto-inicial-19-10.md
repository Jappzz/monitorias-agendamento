# Projeto inicial - 19/10

**Integrantes:** Thiago Wesley Pasquim de Melo e Andre Nacamura

## 1. Continuação do projeto inicial

Este documento complementa o projeto de 18/10 com o mapeamento dos testes da história escolhida, mantendo o escopo, as classes e as responsabilidades já descritos.

**História 1 - Prioridade Alta:** Como aluno, eu quero escolher uma disciplina, ver os horários livres e reservar um atendimento para ser atendido pelo monitor sem conflito de horário.

Os testes serão escritos posteriormente com unittest e chamarão diretamente as funções do serviço de agendamento. Cada teste terá seus próprios dados em memória, sem depender da execução dos demais ou de entrada pelo teclado.

## 2. Mapeamento dos critérios de aceitação

Os nomes abaixo são os nomes previstos para os futuros testes. Os cenários descrevem a preparação, a ação e o resultado esperado; ainda não representam testes implementados ou executados.

| Critério de aceitação | Nome previsto do teste | Cenário e resultado esperado | Tipo |
| :--- | :--- | :--- | :--- |
| CA1 - Listar apenas horários da disciplina escolhida com vagas. | test_consulta_filtra_disciplina_vagas_e_cancelamento | Preparar horários de Cálculo e Física, incluindo um de Cálculo disponível, um lotado e um cancelado com vagas. Consultar Cálculo e verificar que somente seu horário disponível é retornado. | Sucesso |
| CA1 - Listar apenas horários da disciplina escolhida com vagas. | test_consulta_sem_horarios_disponiveis | Consultar uma disciplina cujos horários estão lotados ou cancelados. Esperar uma lista vazia, sem erro. | Sucesso, sem disponibilidade |
| CA2 - Registrar a reserva para o aluno e diminuir uma vaga. | test_reserva_registra_aluno_e_reduz_vagas | Reservar um horário com duas vagas para um aluno sem reservas anteriores. Verificar uma nova reserva vinculada ao aluno e ao horário, com apenas uma vaga restante. | Sucesso |
| CA3 - Recusar horário sem vagas, preservando as reservas existentes. | test_reserva_recusa_horario_lotado | Tentar reservar um horário já preenchido por outro aluno. Esperar um erro descritivo, mantendo as reservas existentes e o número de vagas. | Falha ou exceção |
| CA4 - Recusar reserva em horário cancelado. | test_reserva_recusa_horario_cancelado | Tentar reservar um horário cancelado que ainda teria vagas pela capacidade. Esperar um erro descritivo, sem criar uma reserva ou alterar os registros existentes. | Falha ou exceção |
| CA5 - Respeitar o limite semanal configurável por aluno e disciplina. | test_limite_recusa_segunda_reserva_na_mesma_semana | Com limite de uma reserva, preparar uma reserva na segunda-feira, 19/10/2026. Tentar reservar outro horário da mesma disciplina no domingo, 25/10/2026, para o mesmo aluno. Esperar erro e nenhuma alteração nos registros. | Falha ou exceção |
| CA5 - Respeitar o limite semanal configurável por aluno e disciplina. | test_limite_permite_reserva_em_outra_semana | Preparar uma reserva no domingo, 18/10/2026, e solicitar outra na segunda-feira, 19/10/2026, para o mesmo aluno e disciplina. Esperar sucesso, pois são semanas diferentes. | Sucesso |
| CA5 - Respeitar o limite semanal configurável por aluno e disciplina. | test_limite_permite_reserva_em_outra_disciplina | Preparar uma reserva em Cálculo e solicitar uma em Física para o mesmo aluno, na mesma semana e em outro horário. Esperar sucesso, pois o limite é por disciplina. | Sucesso |
| CA5 - Respeitar o limite semanal configurável por aluno e disciplina. | test_limite_configuravel_permite_duas_reservas | Configurar o limite como dois e preparar uma reserva. Solicitar a segunda na mesma disciplina e semana, esperando sucesso; tentar a terceira e esperar erro, preservando as duas anteriores. | Sucesso e falha ou exceção |
| CA5 - Respeitar o limite semanal configurável por aluno e disciplina. | test_limite_desconsidera_reserva_em_horario_cancelado | Preparar uma reserva associada a um horário cancelado. Com limite de uma reserva, solicitar outro horário disponível da mesma disciplina e semana. Esperar sucesso, pois a reserva do horário cancelado não conta para o limite. | Sucesso |

## 3. Decisões mantidas e conclusão da etapa

O limite inicial será de uma reserva por aluno na mesma disciplina, com possibilidade de configuração. A semana vai de segunda-feira a domingo, considerando a data do atendimento. As vagas serão calculadas pela capacidade menos as reservas; horários cancelados ficarão indisponíveis. Toda recusa deverá preservar os registros existentes.

Os cinco critérios estão associados a testes previstos, incluindo cenários de sucesso e de falha. Cadastro, cancelamento pelo monitor, notificações e relatórios continuam fora desta história; os dados necessários serão preparados previamente.