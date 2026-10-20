"""Regras da História 1: reservar atendimento."""

from datetime import timedelta

from excecoes import (
    HorarioCanceladoError,
    HorarioLotadoError,
    HorarioNaoEncontradoError,
    LimiteSemanalError,
)
from modelos import Aluno, Disciplina, HorarioAtendimento, Reserva
from repositorio import RepositorioAgendamento


class ServicoReserva:
    def __init__(self, repositorio: RepositorioAgendamento, limite_semanal: int = 1):
        if limite_semanal < 1:
            
            raise ValueError("O limite semanal deve ser pelo menos 1.")
        self.repositorio = repositorio
        self.limite_semanal = limite_semanal


    def listar_horarios_livres(
        self, disciplina: Disciplina
    ) -> list[HorarioAtendimento]:
        
        """Horários da disciplina que não estão cancelados e têm vaga."""
        livres = []
        for horario in self.repositorio.listar_horarios_da_disciplina(disciplina.id):
            reservas = self.repositorio.listar_reservas_do_horario(horario)

            if horario.vagas_disponiveis(reservas) > 0:
                livres.append(horario)
        return livres

    def reservar(self, aluno: Aluno, horario: HorarioAtendimento) -> Reserva:
        """Registra a reserva ou lança um erro, sem alterar nada em caso de erro."""
        atual = self.repositorio.buscar_horario(horario.id)
        if atual is None:
            raise HorarioNaoEncontradoError("Horário não encontrado.")
        

        if atual.cancelado:
            raise HorarioCanceladoError("Este horário foi cancelado pelo monitor.")

        reservas = self.repositorio.listar_reservas_do_horario(atual)
        if atual.vagas_disponiveis(reservas) == 0:
            raise HorarioLotadoError("Não há vagas neste horário.")

        # Semana de segunda a domingo, a partir da data do atendimento.
        inicio_semana = atual.data - timedelta(days=atual.data.weekday())

        fim_semana = inicio_semana + timedelta(days=6)

        ja_reservadas = self.repositorio.contar_reservas_ativas_do_aluno(
            aluno.ra, atual.disciplina.id, inicio_semana, fim_semana
        )

        if ja_reservadas >= self.limite_semanal:
            raise LimiteSemanalError(
                "Limite de reservas da semana nesta disciplina atingido."

            )

        reserva = Reserva(aluno, atual)
        self.repositorio.inserir_reserva(reserva)
        return reserva