"""Testes dos critérios CA1 a CA4 e da persistência das reservas.

Pra rodar o teste:
python -m unittest discover -s codigo -p "test_*.py" -v
"""

import unittest
from datetime import date, time
from pathlib import Path
from tempfile import TemporaryDirectory

from excecoes import HorarioCanceladoError, HorarioLotadoError
from modelos import Aluno, Disciplina, HorarioAtendimento, Reserva
from repositorio import RepositorioAgendamento
from servico import ServicoReserva


class TestConsultaEReserva(unittest.TestCase):
    def setUp(self):
        # Cada teste recebe um arquivo novo, separado do banco do sistema.
        self.pasta = TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(self.pasta.cleanup)
        self.caminho = Path(self.pasta.name) / "teste.db"
        self.repo = RepositorioAgendamento(self.caminho)
        # A conexão deve fechar antes de remover a pasta, inclusive em falhas.
        self.addCleanup(lambda: self.repo.fechar())
        self.servico = ServicoReserva(self.repo)

        self.ana = Aluno("1001", "Ana")
        self.bruno = Aluno("1002", "Bruno")
        self.calculo = Disciplina(1, "Cálculo")
        self.fisica = Disciplina(2, "Física")
        for aluno in (self.ana, self.bruno):
            self.repo.salvar_aluno(aluno)
        for disciplina in (self.calculo, self.fisica):
            self.repo.salvar_disciplina(disciplina)

        dia = date(2026, 10, 20)
        self.disponivel = HorarioAtendimento(
            1, self.calculo, "Marcos", dia, time(14), 2
        )
        self.lotado = HorarioAtendimento(
            2, self.calculo, "Marcos", dia, time(15), 1
        )
        self.cancelado = HorarioAtendimento(
            3, self.calculo, "Marcos", dia, time(16), 2, cancelado=True
        )
        self.outra_disciplina = HorarioAtendimento(
            4, self.fisica, "Paula", dia, time(17), 1
        )
        for horario in (
            self.disponivel, self.lotado, self.cancelado, self.outra_disciplina
        ):
            self.repo.salvar_horario(horario)
        self.repo.inserir_reserva(Reserva(self.bruno, self.lotado))

    def reservas_gravadas(self):
        """Fotografia dos registros para detectar alterações em uma recusa."""
        linhas = self.repo.conexao.execute(
            "SELECT id, aluno_ra, horario_id FROM reservas ORDER BY id"
        ).fetchall()
        return [tuple(linha) for linha in linhas]

    def test_consulta_filtra_disciplina_vagas_e_cancelamento(self):
        horarios = self.servico.listar_horarios_livres(self.calculo)

        self.assertEqual(horarios, [self.disponivel])

    def test_consulta_sem_horarios_disponiveis(self):
        self.repo.inserir_reserva(Reserva(self.ana, self.outra_disciplina))

        horarios = self.servico.listar_horarios_livres(self.fisica)

        self.assertEqual(horarios, [])

    def test_reserva_registra_aluno_e_reduz_vagas(self):
        antes = self.reservas_gravadas()
        self.assertEqual(self.disponivel.vagas_disponiveis([]), 2)

        reserva = self.servico.reservar(self.ana, self.disponivel)

        gravadas = self.repo.listar_reservas_do_horario(self.disponivel)
        self.assertEqual(reserva.aluno, self.ana)
        self.assertEqual(reserva.horario, self.disponivel)
        self.assertEqual(gravadas, [reserva])
        self.assertEqual(self.disponivel.vagas_disponiveis(gravadas), 1)
        self.assertEqual(len(self.reservas_gravadas()), len(antes) + 1)

    def test_reserva_recusa_horario_lotado(self):
        antes = self.reservas_gravadas()

        with self.assertRaisesRegex(HorarioLotadoError, "Não há vagas"):
            self.servico.reservar(self.ana, self.lotado)

        self.assertEqual(self.reservas_gravadas(), antes)
        gravadas = self.repo.listar_reservas_do_horario(self.lotado)
        self.assertEqual(gravadas, [Reserva(self.bruno, self.lotado)])
        self.assertEqual(self.lotado.vagas_disponiveis(gravadas), 0)

    def test_reserva_recusa_horario_cancelado(self):
        antes = self.reservas_gravadas()

        with self.assertRaisesRegex(HorarioCanceladoError, "cancelado"):
            self.servico.reservar(self.ana, self.cancelado)

        self.assertEqual(self.reservas_gravadas(), antes)
        self.assertEqual(
            self.repo.listar_reservas_do_horario(self.cancelado), []
        )

    def test_reserva_persiste_apos_reabrir_banco(self):
        self.servico.reservar(self.ana, self.disponivel)
        self.repo.fechar()

        self.repo = RepositorioAgendamento(self.caminho)
        self.servico = ServicoReserva(self.repo)

        horario = self.repo.buscar_horario(self.disponivel.id)
        self.assertEqual(horario, self.disponivel)
        gravadas = self.repo.listar_reservas_do_horario(horario)
        self.assertEqual(gravadas, [Reserva(self.ana, horario)])
        self.assertEqual(horario.vagas_disponiveis(gravadas), 1)


if __name__ == "__main__":
    unittest.main()
