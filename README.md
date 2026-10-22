# Agendamento de monitorias

**Integrantes:** Thiago Wesley Pasquim de Melo e Andre Nacamura.

Neste trabalho, fizemos a História 1: o aluno consulta os horários disponíveis de uma disciplina e reserva um atendimento. Cada atendimento dura 30 minutos e pode ter uma ou mais vagas.

O sistema não aceita reservas em horários lotados ou cancelados, nem duas reservas do mesmo aluno no mesmo horário. O limite inicial é de uma reserva por aluno na mesma disciplina por semana, mas pode ser alterado. A semana vai de segunda a domingo, e reservas de horários cancelados não contam para esse limite.

## Como executar

Usamos **Python 3.15**, com `sqlite3` para o banco e `unittest` para os testes. Os dois fazem parte do Python, então não é preciso instalar bibliotecas extras.

Abra o terminal na pasta do repositório e execute:

```powershell
python codigo/principal.py
```

O arquivo principal é `codigo/principal.py`. Ele usa dados de exemplo e mostra consultas e tentativas de reserva no terminal, sem pedir dados pelo teclado. O banco `monitorias.db` é criado automaticamente na raiz do projeto e mantém os dados depois que o programa fecha. Por isso, ao executar de novo, uma reserva já feita será recusada. O arquivo do banco fica fora do Git; o programa cria um novo se ele não existir.

Para executar os testes:

```powershell
python -m unittest discover -s codigo -p "test_*.py" -v
```

Na conferência de 21/10, os **14 testes passaram**, com resultado `OK`. Cada teste usa seu próprio banco temporário, que é apagado no final. Também conferimos que a demonstração mantém os dados ao executar duas vezes.

## O que foi feito

| Data | O que foi feito ou planejado | Quem fez |
| :--- | :--- | :--- |
| 17/10 | Histórias de usuário registradas no repositório. | Andre |
| 18/10 | Escolha da História 1 e descrição das classes e responsabilidades. | Thiago |
| 19/10 | Thiago fez o mapeamento dos testes, as classes e a criação do banco. Andre fez a integração com o banco, as regras de reserva e a demonstração. | Thiago e Andre |
| 20/10 | Thiago fez seis testes. Andre fez mais oito e acrescentou a verificação de reserva duplicada. | Thiago e Andre |
| 21/10 | Thiago escreveu o README, conferiu a execução e organizou as cinco histórias na documentação técnica. A documentação dos testes ficou para Andre. | Thiago e Andre |
| 22/10 | Vamos revisar, gerar o PDF, conferir o ZIP e fazer o envio. Ainda não realizado. | Thiago e Andre, conforme o plano |

Até 20/10, os commits foram feitos nas datas do planejamento, sem atraso registrado. No plano, colocamos os dois em cada etapa, mas dividimos as tarefas como está na tabela.

## O que mudou no projeto

No começo, os dados ficariam só em memória. Depois escolhemos SQLite para não perder as reservas ao fechar o programa. Criamos `repositorio.py` para concentrar o acesso ao banco e deixar as regras em `servico.py`.

O projeto de 19/10 previa testes com banco em memória e dizia que a inicialização devolveria uma conexão aberta. Na implementação, ela fecha a conexão e devolve o caminho do arquivo. Por isso, os testes usam arquivos temporários, mantendo cada teste separado dos outros.

Durante os testes, percebemos que, com o limite semanal maior que um, o mesmo aluno poderia reservar duas vezes o mesmo horário e ocupar duas vagas de um atendimento em grupo. Por isso acrescentamos ao `servico.py` a verificação de reserva duplicada, com a exceção `ReservaDuplicadaError`, que não estava no projeto inicial. Também escrevemos quatro testes além dos dez mapeados: persistência após reabrir o banco, reserva duplicada, outro aluno no mesmo horário em grupo e horário inexistente.
