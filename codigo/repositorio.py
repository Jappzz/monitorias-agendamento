"""Acesso ao banco: única camada que escreve SQL. Não tem regras de negócio."""

import sqlite3
from datetime import date, time

from modelos import Aluno, Disciplina, HorarioAtendimento, Reserva


_SELECT_HORARIO = """
    SELECT h.id, h.monitor, h.data, h.inicio, h.capacidade, h.cancelado,
           d.id AS disciplina_id, d.nome AS disciplina_nome
    FROM horarios h
    JOIN disciplinas d ON d.id = h.disciplina_id
"""


def _linha_para_horario(linha: sqlite3.Row) -> HorarioAtendimento:
    return HorarioAtendimento(
        id=linha["id"],
        disciplina=Disciplina(linha["disciplina_id"], linha["disciplina_nome"]),
        monitor=linha["monitor"],
        data=date.fromisoformat(linha["data"]),
        inicio=time.fromisoformat(linha["inicio"]),
        capacidade=linha["capacidade"],
        cancelado=bool(linha["cancelado"]),
    )


class RepositorioAgendamento:
    def __init__(self, conexao: sqlite3.Connection):
        self.conexao = conexao

    # --- carga de dados (usada pelos testes e por scripts de dados iniciais)

    def salvar_aluno(self, aluno: Aluno) -> None:
        self.conexao.execute(
            "INSERT INTO alunos (ra, nome) VALUES (?, ?)",
            (aluno.ra, aluno.nome),
        )
        self.conexao.commit()

    def salvar_disciplina(self, disciplina: Disciplina) -> None:
        self.conexao.execute(
            "INSERT INTO disciplinas (id, nome) VALUES (?, ?)",
            (disciplina.id, disciplina.nome),
        )
        self.conexao.commit()

    def salvar_horario(self, horario: HorarioAtendimento) -> None:
        self.conexao.execute(
            "INSERT INTO horarios "
            "(id, disciplina_id, monitor, data, inicio, capacidade, cancelado) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                horario.id,
                horario.disciplina.id,
                horario.monitor,
                horario.data.isoformat(),
                horario.inicio.isoformat(),
                horario.capacidade,
                int(horario.cancelado),
            ),
        )
        self.conexao.commit()

    # --- consultas

    def buscar_horario(self, horario_id: int) -> HorarioAtendimento | None:
        linha = self.conexao.execute(
            _SELECT_HORARIO + " WHERE h.id = ?", (horario_id,)
        ).fetchone()

        return _linha_para_horario(linha) if linha else None

    def listar_horarios_da_disciplina(
        self, disciplina_id: int
    ) -> list[HorarioAtendimento]:
        
        linhas = self.conexao.execute(
            _SELECT_HORARIO
            + " WHERE h.disciplina_id = ? ORDER BY h.data, h.inicio",
            (disciplina_id,),
        ).fetchall()
        
        return [_linha_para_horario(linha) for linha in linhas]

    def listar_reservas_do_horario(
        self, horario: HorarioAtendimento
    ) -> list[Reserva]:
        
        linhas = self.conexao.execute(
            "SELECT a.ra, a.nome FROM reservas r "
            "JOIN alunos a ON a.ra = r.aluno_ra WHERE r.horario_id = ?",
            (horario.id,),
        ).fetchall()

        return [Reserva(Aluno(l["ra"], l["nome"]), horario) for l in linhas]

    def contar_reservas_ativas_do_aluno(
        self, aluno_ra: str, disciplina_id: int, inicio: date, fim: date
    ) -> int:
        """Conta reservas do aluno na disciplina entre duas datas (inclusive),
        ignorando as que estão em horários cancelados."""
        linha = self.conexao.execute(
            "SELECT COUNT(*) AS total FROM reservas r "
            "JOIN horarios h ON h.id = r.horario_id "
            "WHERE r.aluno_ra = ? AND h.disciplina_id = ? "
            "AND h.cancelado = 0 AND h.data BETWEEN ? AND ?",
            (aluno_ra, disciplina_id, inicio.isoformat(), fim.isoformat()),
        ).fetchone()
        
        return linha["total"]

    # --- escrita da reserva

    def inserir_reserva(self, reserva: Reserva) -> None:
        self.conexao.execute(
            "INSERT INTO reservas (aluno_ra, horario_id) VALUES (?, ?)",
            (reserva.aluno.ra, reserva.horario.id),
        )
        self.conexao.commit()