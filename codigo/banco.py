"""Criação do banco SQLite, ainda sem operações de cadastro ou consulta."""

import sqlite3
from contextlib import closing
from pathlib import Path


CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "monitorias.db"


def inicializar_banco(caminho: str | Path = CAMINHO_BANCO) -> Path:
    """Cria as tabelas que ainda não existem, preservando os dados existentes."""
    caminho = Path(caminho)

    with closing(sqlite3.connect(caminho)) as conexao:
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS alunos (
                ra TEXT PRIMARY KEY NOT NULL,
                nome TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS disciplinas (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS horarios (
                id INTEGER PRIMARY KEY,
                disciplina_id INTEGER NOT NULL,
                monitor TEXT NOT NULL,
                data TEXT NOT NULL,
                inicio TEXT NOT NULL,
                capacidade INTEGER NOT NULL CHECK (capacidade >= 1),
                cancelado INTEGER NOT NULL DEFAULT 0
                    CHECK (cancelado IN (0, 1)),
                FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id)
            );

            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY,
                aluno_ra TEXT NOT NULL,
                horario_id INTEGER NOT NULL,
                FOREIGN KEY (aluno_ra) REFERENCES alunos(ra),
                FOREIGN KEY (horario_id) REFERENCES horarios(id)
            );
        """)
        conexao.commit()

    return caminho


if __name__ == "__main__":
    banco = inicializar_banco()
    print(f"Banco inicializado em: {banco}")
