import sqlite3
import csv


tipos_colunas = {
    # categories
    "category_id": "INTEGER",

    # customers
    "customer_id": "INTEGER",

    # order_items
    "order_id": "INTEGER",
    "quantity": "INTEGER",
    "product_id": "INTEGER",

    # orders
    "order_id": "INTEGER",
    "customer_id": "INTEGER",
    "order_date": "TEXT",
    "total_brl": "REAL",
    "estimated_delivery": "TEXT",

    # products
    "product_id": "INTEGER",
    "price_brl": "REAL",
    "category_id": "INTEGER",
    "stock_quantity": "INTEGER",
    "created_at": "TEXT",

    # promotions
    "promotion_id": "INTEGER",
    "product_id": "INTEGER",
    "discount_percent": "REAL",
    "is_active": "INTEGER"
}


def converter_valor(valor, tipo):
    if valor == "":
        return None

    if tipo == "INTEGER":
        return int(valor)

    if tipo == "REAL":
        return float(valor.replace(",", "."))

    return valor


def criarBanco(PASTA_CSV, conexao):    
    for arquivo in PASTA_CSV.glob("*.csv"):
        nome_tabela = arquivo.stem.split(" - ")[-1]

        with open(arquivo, "r", encoding="utf-8-sig", newline="") as f:
            leitor = csv.reader(f)

            cabecalho = next(leitor)

            # Remove espaços dos nomes das colunas
            cabecalho = [col.strip() for col in cabecalho]

            colunas = ", ".join(
                f'"{col}" {tipos_colunas.get(col, "TEXT")}'
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

            dados = []

            for linha in leitor:
                linha_convertida = [
                    converter_valor(
                        valor,
                        tipos_colunas.get(col, "TEXT")
                    )
                    for col, valor in zip(cabecalho, linha)
                ]

                dados.append(linha_convertida)

            conexao.executemany(
                sql_insert,
                dados
            )

    conexao.commit()


def consultarSQL(sql, conexao):
    cursor = conexao.execute(sql)
    colunas = [descricao[0] for descricao in cursor.description]
    resultados = cursor.fetchall()

    return colunas, resultados