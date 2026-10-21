"""Erros de regra de negócio do agendamento."""


class AgendamentoError(Exception):
    """Base de todos os erros do agendamento."""


class HorarioNaoEncontradoError(AgendamentoError):
    """O horário informado não existe no banco."""


class HorarioCanceladoError(AgendamentoError):
    """O monitor cancelou este horário."""


class HorarioLotadoError(AgendamentoError):
    """Não há vagas disponíveis neste horário."""


class LimiteSemanalError(AgendamentoError):
    """O aluno atingiu o limite de reservas da semana na disciplina."""

class ReservaDuplicadaError(AgendamentoError):
    """O aluno já tem reserva neste mesmo horário."""