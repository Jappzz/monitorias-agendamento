"""Entidades usadas pelo futuro serviço de agendamento."""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta


@dataclass
class Aluno:
    ra: str
    nome: str


@dataclass
class Disciplina:
    id: int
    nome: str


@dataclass
class HorarioAtendimento:
    id: int
    disciplina: Disciplina
    monitor: str
    data: date
    inicio: time
    capacidade: int
    cancelado: bool = False

    def __post_init__(self):
        if self.capacidade < 1:
            raise ValueError("A capacidade deve ser maior ou igual a uma vaga.")

    @property
    def fim(self) -> datetime:
        """Todo atendimento termina 30 minutos após o início."""
        return datetime.combine(self.data, self.inicio) + timedelta(minutes=30)

    def vagas_disponiveis(self, reservas: list["Reserva"]) -> int:
        """Consulta as reservas do serviço sem manter um contador separado."""
        if self.cancelado:
            return 0

        ocupadas = sum(
            1 for reserva in reservas if reserva.horario.id == self.id
        )
        return max(0, self.capacidade - ocupadas)


@dataclass
class Reserva:
    aluno: Aluno
    horario: HorarioAtendimento

    @property
    def disciplina(self) -> Disciplina:
        return self.horario.disciplina

    @property
    def data(self) -> date:
        return self.horario.data
