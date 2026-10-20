"""Arquivo principal: liga o banco, o repositório e o serviço de reserva.

Execute dentro da pasta codigo/ com:  python principal.py
Os dados ficam gravados em monitorias.db entre as execuções.
"""

from datetime import date, time

from banco import CAMINHO_BANCO
from excecoes import AgendamentoError
from modelos import Aluno, Disciplina, HorarioAtendimento
from repositorio import RepositorioAgendamento
from servico import ServicoReserva


def carregar_dados_exemplo(repo, calculo, fisica, ana, bruno, horarios):
    """Grava os dados de exemplo, apenas se o banco ainda estiver vazio."""
    if repo.buscar_horario(horarios[0].id) is not None:
        return False

    repo.salvar_disciplina(calculo)
    repo.salvar_disciplina(fisica)
    repo.salvar_aluno(ana)
    repo.salvar_aluno(bruno)
    for horario in horarios:
        repo.salvar_horario(horario)
    return True


def imprimir_horarios(titulo, horarios, repo):
    print(titulo)
    if not horarios:
        print("  (nenhum)")
    for h in horarios:
        vagas = h.vagas_disponiveis(repo.listar_reservas_do_horario(h))
        print(f"  Horário {h.id}: {h.data} {h.inicio} - {h.monitor} - {vagas} vaga(s)")


def main(caminho=CAMINHO_BANCO):
    repo = RepositorioAgendamento(caminho)
    servico = ServicoReserva(repo)

    calculo = Disciplina(1, "Cálculo")
    fisica = Disciplina(2, "Física")
    ana = Aluno("1001", "Ana")
    bruno = Aluno("1002", "Bruno")
    horarios = [
        HorarioAtendimento(1, calculo, "Marcos", date(2026, 10, 26), time(14, 0), 2),
        HorarioAtendimento(2, calculo, "Marcos", date(2026, 10, 26), time(15, 0), 1),
        HorarioAtendimento(3, calculo, "Marcos", date(2026, 10, 27), time(14, 0), 1,
                           cancelado=True),
        HorarioAtendimento(4, fisica, "Paula", date(2026, 10, 27), time(10, 0), 1),
    ]

    if carregar_dados_exemplo(repo, calculo, fisica, ana, bruno, horarios):
        print("Dados de exemplo gravados no banco.\n")
    else:
        print("O banco já tinha dados; mantendo o que estava gravado.\n")

    imprimir_horarios("Horários livres de Cálculo:",
                      servico.listar_horarios_livres(calculo), repo)

    print("\nAna tenta reservar o horário 1...")
    try:
        servico.reservar(ana, horarios[0])
        print("  Reserva registrada.")
    except AgendamentoError as erro:
        print(f"  Recusada: {erro}")

    print("\nAna tenta reservar o horário 2 (mesma semana e disciplina)...")
    try:
        servico.reservar(ana, horarios[1])
        print("  Reserva registrada.")
    except AgendamentoError as erro:
        print(f"  Recusada: {erro}")

    print("\nBruno tenta reservar o horário 3 (cancelado)...")
    try:
        servico.reservar(bruno, horarios[2])
        print("  Reserva registrada.")
    except AgendamentoError as erro:
        print(f"  Recusada: {erro}")

    print()
    imprimir_horarios("Horários livres de Cálculo agora:",
                      servico.listar_horarios_livres(calculo), repo)

    print("\nQuem reservou o horário 1:")
    reservas = repo.listar_reservas_do_horario(horarios[0])
    if not reservas:
        print("  (ninguém)")
    for reserva in reservas:
        print(f"  {reserva.aluno.nome} (RA {reserva.aluno.ra})")

    repo.fechar()


if __name__ == "__main__":
    main()