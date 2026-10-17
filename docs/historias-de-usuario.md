1.
História
    como aluno, eu quero escolher uma disciplina, ver os horários livres e reservar um atendimento para ser atendido pelo monitor sem conflito de horário.

Critérios de aceitação
    Ao escolher uma disciplina, o sistema lista apenas os horários dela que ainda tem vaga
    Ao reservar um horário com vaga, a reserva é registrada para o alunos e o número de vagas disponíveis diminui em 1
    Resevervar uym horário sem vagas gera erro e não altera as reservas exigentes
    Reservar um horário cancelado pelo monitor gera erro
    O alunoi não pode reservar mais de um horário por semana na mesma disciplina(limite configurável)

Prioridade
    Alta. É o núcleo do sistema e resolve o problema central do e-mail(alunos em conflito num horário e monitores ociosos em outros).

Trecho do e-mail
    A ideia é que o aluno escolha a disciplina, veja os horários livres e reserve um atendimento." / "Não precisa resolver tudo de uma vez. Se a reserva de horários funcionar, já ajuda muito.

2.
História
    Como monitor, eu quero cancelar um horário em que não posso atender para que os alunos reservados sejam avisados antes de chegarem à sala.

critérios de aceitação
    O monitor só consegue cancelar horários cadastrados por ele.
    Ao cancelar, o horário passa a constar como cancelado e deixa de aparecer na lista de horários livres.
    Cada aluno com reserva no horário cancelado recebe uma notificação de cancelamento.
    Cancelar um horário que já está cancelado gera erro.

Prioridade
    Alta. Resolve uma reclamação explícita dos alunos e evita deslocamentos em vão, além de liberar o aluno para reservar outro horário.

Trecho do e-mail
    às vezes precisa cancelar por causa de prova. Os alunos reclamam que só descobrem o cancelamento quando chegam na sala

3.
História
    Como monitor, eu quero cadastrar os horários em que posso atender, definindo o número de vagas, para que os alunos possam reservá-los em atendimento individual ou em grupo.

Critérios de aceitação
    O monitor cadastra um horário informando disciplina, dia e hora de início, com duração fixa de 30 minutos.
    O sistema não aceita dois horários que se sobreponham para o mesmo monitor
    O número de vagas deve ser maior ou igual a 1 (1 = individual, mais de 1 = grupo); valores menores geram erro.
    Um horário recém-cadastrado aparece como livre na consulta dos alunos.

Prioridade
    Média. É pré-requisito da reserva, mas na primeira versão os horários podem ser carregados por dados iniciais, sem depender de uma tela de cadastro.
Trecho do e-mail
    No início do semestre, cada monitor informa os horários em que pode atender" / "Cada atendimento dura 30 minutos, mas alguns monitores preferem atender em grupo, quando várias pessoas têm a mesma dúvida.

4.
História
    Como coordenador, eu quero consultar o histórico e o total mensal de horas atendidas por cada monitor para contabilizar e pagar as bolsas.

Critérios de aceitação
    O relatório soma, por monitor, as horas dos atendimentos realizados no mês escolhido.
    Atendimentos cancelados não entram na soma.
    Apenas usuários com perfil de coordenador acessam o relatório; os demais recebem erro de permissão
    Um mês sem atendimentos retorna zero horas para os monitores, sem gerar erro

Prioridade
    Média. É uma obrigação da coordenação, mas só faz sentido depois que reservas e atendimentos existirem

Trecho do e-mail
    A coordenação precisa de um relatório mensal com as horas atendidas por cada monitor, porque isso conta para o pagamento da bolsa. Essas informações de bolsa não podem ficar visíveis para todo mundo

5.
História
    Como professor, eu quero ver quais conteúdos geraram mais atendimentos na minha disciplina para reforçá-los em sala de aula.
Critérios de aceitação
    Após o atendimento, o monitor registra o conteúdo abordado na sessão.
    O professor vê a lista de conteúdos da sua disciplina ordenada pela quantidade de atendimentos, do maior para o menor.
    O professor não consegue ver dados de conteúdos de outras disciplinas.
    Atendimentos sem conteúdo registrado aparecem agrupados como "Não informado".
Prioridade
    Baixa. Tem valor pedagógico, mas o agendamento funciona sem ela.

Trecho do e-mail 
    "Os professores das disciplinas gostariam de saber quais conteúdos geram mais dúvidas, para reforçar em aula."