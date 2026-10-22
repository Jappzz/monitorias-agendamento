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

Os testes da História 1 estão em codigo/test_reservas.py e usam unittest. Eles chamam diretamente o ServicoReserva e o RepositorioAgendamento, sem pedir dados pelo teclado. Cada teste cria um banco SQLite temporário com os mesmos dados iniciais (dois alunos, duas disciplinas e quatro horários: um com vagas, um lotado, um cancelado e um de outra disciplina) e o apaga no final. São 14 testes, e todos passam com o comando:

**python -m unittest discover -s codigo -p "test_*.py" -v**

### 2.1. Critérios de aceitação e testes

| Critério | Teste | O que verifica |
| :--- | :--- | :--- |
| CA1 | `test_consulta_filtra_disciplina_vagas_e_cancelamento` | Com horários de Cálculo e Física, incluindo um lotado e um cancelado, a consulta de Cálculo devolve só o horário com vaga. |
| CA1 | `test_consulta_sem_horarios_disponiveis` | Em uma disciplina cujo único horário está lotado, a lista volta vazia, sem erro. |
| CA2 | `test_reserva_registra_aluno_e_reduz_vagas` | Reservar um horário de 2 vagas devolve a reserva do aluno, grava no banco e deixa 1 vaga. |
| CA3 | `test_reserva_recusa_horario_lotado` | Reservar um horário já ocupado gera `HorarioLotadoError`; as reservas existentes e o número de vagas não mudam. |
| CA4 | `test_reserva_recusa_horario_cancelado` | Reservar um horário cancelado, que ainda teria vagas pela capacidade, gera `HorarioCanceladoError` e nada é gravado. |
| CA5 | `test_limite_recusa_segunda_reserva_na_mesma_semana` | Com limite 1 e uma reserva já feita, a segunda reserva em Cálculo na mesma semana gera `LimiteSemanalError` e nada é gravado. |
| CA5 | `test_limite_configuravel_permite_duas_reservas` | Com limite 2, as duas primeiras reservas passam e a terceira é recusada; o aluno fica com 2 reservas. |
| CA5 | `test_limite_permite_reserva_em_outra_semana` | Reservas no domingo (18/10) e na segunda (19/10) passam, pois são semanas diferentes. |
| CA5 | `test_limite_permite_reserva_em_outra_disciplina` | Uma reserva em Cálculo e outra em Física na mesma semana passam, pois o limite é por disciplina. |
| CA5 | `test_limite_desconsidera_reserva_em_horario_cancelado` | A reserva em um horário cancelado não conta; o aluno consegue reservar outro horário de Cálculo na mesma semana. |

### 2.2. Testes adicionais

Estes testes não estão ligados a um dos cinco critérios. A regra de reserva duplicada foi acrescentada durante a implementação, por isso seus testes ficam aqui.

| Teste | O que verifica |
| :--- | :--- |
| `test_reserva_persiste_apos_reabrir_banco` | Depois de fechar e reabrir o banco, a reserva e o número de vagas continuam gravados. |
| `test_reserva_recusa_mesmo_aluno_no_mesmo_horario` | Com limite 2, o mesmo aluno não reserva duas vezes o mesmo horário: gera `ReservaDuplicadaError` e nada é gravado. |
| `test_reserva_permite_outro_aluno_no_mesmo_horario_em_grupo` | Dois alunos diferentes reservam o mesmo horário de 2 vagas (atendimento em grupo) e o horário fica lotado. |
| `test_reserva_recusa_horario_inexistente` | Reservar um horário que não está no banco gera `HorarioNaoEncontradoError` e nada é gravado. |

### 2.3. Cenários de sucesso e de falha

Chamamos de cenário de sucesso aquele em que a operação é válida e o sistema a aceita. Nos cenários de falha, a operação é inválida e o sistema a recusa com um erro. Nesses testes, o resultado esperado é justamente o erro, então todos os 14 testes passam.

- **Sucesso (9 testes):** `test_consulta_filtra_disciplina_vagas_e_cancelamento`, `test_consulta_sem_horarios_disponiveis`, `test_reserva_registra_aluno_e_reduz_vagas`, `test_limite_configuravel_permite_duas_reservas`, `test_limite_permite_reserva_em_outra_semana`, `test_limite_permite_reserva_em_outra_disciplina`, `test_limite_desconsidera_reserva_em_horario_cancelado`, `test_reserva_persiste_apos_reabrir_banco` e `test_reserva_permite_outro_aluno_no_mesmo_horario_em_grupo`.
- **Falha ou exceção (6 testes):** `test_reserva_recusa_horario_lotado`, `test_reserva_recusa_horario_cancelado`, `test_limite_recusa_segunda_reserva_na_mesma_semana`, `test_limite_configuravel_permite_duas_reservas`, `test_reserva_recusa_mesmo_aluno_no_mesmo_horario` e `test_reserva_recusa_horario_inexistente`.

O `test_limite_configuravel_permite_duas_reservas` entra nas duas listas, pois verifica duas reservas aceitas e a terceira recusada. Em todos os testes de falha, conferimos também que as reservas gravadas continuam iguais. O CA1 e o CA2 não têm cenário de falha, pois a consulta e a reserva válida não geram erro; o caso extremo do CA1 é a lista vazia.

### 2.4. O que não foi testado

- **Histórias 2 a 5:** cancelamento pelo monitor, cadastro de horários, relatório de horas e consulta de conteúdos não foram implementadas, pois o plano previa fazer só a História 1.
- **`principal.py`:** é um roteiro de demonstração. Conferimos executando duas vezes e vendo que os dados permanecem, mas não há teste automático.
- **Banco e repositório isolados:** não há testes só do SQL. Todos os testes passam por eles, então erros apareceriam indiretamente, mas não testamos cada consulta separadamente.
- **Último dia da semana:** os testes do limite usam dias úteis (terça e quarta) para a mesma semana. A virada entre o domingo (18/10) e a segunda (19/10) está testada, mas a reserva em uma segunda e em um domingo da mesma semana não foi.
- **Reservas simultâneas:** não testamos dois alunos disputando a última vaga ao mesmo tempo. O programa roda em um único processo e não tem interface com acesso simultâneo.
- **Duração de 30 minutos e capacidade inválida:** pertencem ao cadastro de horários (História 3), e não à reserva.
- **Reserva duplicada no banco:** a regra existe só no serviço. O banco não a impõe, então uma gravação direta pelo repositório não passa por ela.