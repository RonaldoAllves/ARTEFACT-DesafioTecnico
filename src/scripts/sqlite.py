import sqlite3
import csv

def criarBanco(PASTA_CSV, conexao):
    try:
        for arquivo in PASTA_CSV.glob("*.csv"):
            nome_tabela = arquivo.stem.split(" - ")[-1]

            with open(arquivo, "r", encoding="utf-8-sig", newline="") as f:
                leitor = csv.reader(f)

                cabecalho = next(leitor)

                # Remove espaços dos nomes das colunas
                cabecalho = [col.strip() for col in cabecalho]

                colunas = ", ".join(
                    f'"{col}" TEXT'
                    for col in cabecalho
                )

                conexao.execute(
                    f'DROP TABLE IF EXISTS "{nome_tabela}"'
                )

                conexao.execute(
                    f'CREATE TABLE "{nome_tabela}" ({colunas})'
                )

                placeholders = ", ".join(
                    "?" for _ in cabecalho
                )

                sql_insert = (
                    f'INSERT INTO "{nome_tabela}" '
                    f'VALUES ({placeholders})'
                )

                conexao.executemany(
                    sql_insert,
                    leitor
                )

        conexao.commit()

    finally:
        conexao.close()


def consultarSQL(sql, conexao):   
    try:
        cursor = conexao.execute(sql)
        colunas = [descricao[0] for descricao in cursor.description]
        resultados = cursor.fetchall()

        return colunas, resultados

    finally:
        conexao.close()