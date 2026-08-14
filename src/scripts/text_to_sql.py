import sqlite3, logging
from ollama import chat

logging.basicConfig(level=logging.INFO)

def extrair_esquema(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = [r[0] for r in cursor.fetchall()]
    esquema_str = ""
    for t in tabelas:
        cols = [c[1] for c in conn.execute(f"PRAGMA table_info('{t}');")]
        esquema_str += f"CREATE TABLE {t} ({', '.join(cols)});\n"
    return esquema_str

def extrair_tabelas(conn):
    tabelas = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';")]
    return tabelas

import sqlglot

def validar_sql(sql, tabelas_permitidas):
    # Exemplo simplista: só permite SELECT e verifica tabelas
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Consulta deve ser SELECT")
    parsed = sqlglot.parse_one(sql)  # Valida sintaxe, lança se inválido
    # Checa se todas as tabelas usadas estão no esquema (pode-se extrair via parsed.sql())
    for table in tabelas_permitidas:
        # crude: remove tabela se presente
        if table in parsed.sql():
            continue
    # (Implementar verificação real usando parsed.find_all())
    return True

def executar_consulta(sql, conn):
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN")
        cursor.execute(sql)
        dados = cursor.fetchall()
        col_names = [d[0] for d in cursor.description] if cursor.description else []
        conn.commit()
        return col_names, dados
    except Exception as e:
        conn.rollback()
        logging.error("Erro ao executar SQL: %s", e)
        raise

def gerar_sql_llm(pergunta, esquema_str, modelo, temp=0.3):

    prompt = f"""
Você é um especialista em SQL SQLite.

Sua tarefa é transformar a pergunta do usuário em uma consulta SQL SQLite.
Sempre que possível as colunas devem trazer resultados coerentes com a pergunta, ou seja, seja proativo e traga informações relevantes para a pergunta.
Por exemplo:
    - Se a pergunta for sobre o preço de um produto, a consulta deve trazer o preço do produto e informações sobre o produto, como nome, descrição, categoria, etc.
    - Se a pergunta for sobre o preço de um instrumento musical, a consulta deve considerar os descontos também.
    - Se a pergunta for sobre um tipo de instrumento musical, a consulta deve buscar por esse tipo de instrumento musical, considerando o nome, descrição, categoria e especificações da tabela de produtos e também da de categorias.

Os dados são de uma loja de instrumentos musicais.

ESQUEMA DO BANCO:
{esquema_str}

Exemplo de registros por cada tabela:

categories
category_id,name,description
1,Guitarras,"Guitarras elétricas de todos os estilos, do rock ao jazz"

customers
customer_id,name,phone,email,city
1,Lucas Mendes da Silva,(67) 99812-3456,lucas.mendes@jmail.com,Campo Grande

order_items
order_id,quantity,product_id
1,1,93

order_id,customer_id,order_date,status,total_brl,payment_method,tracking_code,estimated_delivery,notes
1,3,2025-10-15,delivered,11499,pix,BRAB1234567BR,2025-10-25,
17,15,2026-01-28,cancelled,689,pix,,,Pedido cancelado pelo cliente antes do processamento

promotions
promotion_id,product_id,discount_percent,description,is_active
1,102,10,Black Friday,0

Os tipos de status possíveis são:
- products.status: 'active', 'discontinued', 'coming_soon'
- orders.status: 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'
- promotions.is_active: 0, 1

Os tipos de pagamento são:
- orders.payment_method: 'pix', 'credit_6x', 'credit_12x', 'boleto', 'credit_3x', 'debit'

EXEMPLO DE PERGUNTA E CONSULTA SQL (São exemplos reais):

PRIMEIRO EXEMPLO
PERGUNTA DE EXEMPLO: "Quais são os instrumentos elétricos?"
CONSULTA SQL DE EXEMPLO:

SELECT p.name, p.description 
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE 
            c.name LIKE '%elétrico%'
            OR c.name LIKE '%electric%'
            OR c.description LIKE '%elétrico%'
            OR c.description LIKE '%electric%'
            OR p.name LIKE '%elétrico%'
            OR p.description LIKE '%elétrico%' 
            OR p.specs LIKE '%elétrico%' 
            OR p.name LIKE '%electric%' 
            OR p.description LIKE '%electric%' 
            OR p.specs LIKE '%electric%'
        ;

SEGUNDO EXEMPLO
PERGUNTA DE EXEMPLO: "Qual é o instrumento mais barato e o mais caro?"
CONSULTA SQL DE EXEMPLO:

SELECT * FROM (
    SELECT
        name AS instrumento,
        description AS descricao,
        price_brl AS preco,
        'Mais Barato' AS tipo
    FROM products
    WHERE status = 'active'
    ORDER BY price_brl ASC
    LIMIT 1
)
UNION ALL
SELECT * FROM (
    SELECT
        name AS instrumento,
        description AS descricao,
        price_brl AS preco,
        'Mais Caro' AS tipo
    FROM products
    WHERE status = 'active'
    ORDER BY price_brl DESC
    LIMIT 1
);

TERCEIRO EXEMPLO
PERGUNTA DE EXEMPLO: "qual é o instrumento com o maior desconto?"
CONSULTA SQL DE EXEMPLO:

SELECT
    p.name AS instrumento,
    p.price_brl AS preco_original,
    pr.discount_percent AS desconto_percentual,
    ROUND(p.price_brl * (1 - pr.discount_percent / 100.0), 2) AS preco_final
FROM products p
JOIN promotions pr ON p.product_id = pr.product_id
WHERE pr.is_active = 1
  AND p.status = 'active'
ORDER BY pr.discount_percent DESC
LIMIT 1;

PERGUNTA:
{pergunta}

REGRAS:
- Gere somente SQL.
- Não explique a consulta.
- Não utilize Markdown.
- Não utilize ```sql.
- Use somente tabelas e colunas presentes no esquema.
- Gere apenas consultas SELECT.
- Não faça INSERT, UPDATE, DELETE, DROP, ALTER ou CREATE.
- Considere variações, sinônimos, singular/plural e termos equivalentes nas condições `LIKE`; por exemplo, para "teclado", considere também "teclados", "keyboard", "key" e termos relacionados.
- Sempre agrupe entre parênteses todas as condições `OR` quando houver um filtro `AND`, garantindo que o filtro seja aplicado a todas as condições alternativas.

SQL:
"""

    resposta = chat(
        model=modelo,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": temp
        }
    )

    sql = resposta.message.content.strip()

    return sql

def textToSQL(pergunta, modelo, temp, conn):
    try:
        esquema = extrair_esquema(conn)
        tabelas = extrair_tabelas(conn)

        sql_gerado = gerar_sql_llm(pergunta, esquema, modelo, temp)
        validar_sql(sql_gerado, tabelas)
        cols, resultados = executar_consulta(sql_gerado, conn)

        return sql_gerado, cols, resultados
    except Exception as e:
        print("Erro no fluxo:", e)
        return None, None, None
