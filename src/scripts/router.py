from ollama import chat

def router(query, modelo, temp):
    prompt = f"""
    
Você é um roteador de consultas de um sistema de perguntas e respostas da loja "Empório da Música".
Sua função NÃO é responder à pergunta.
Sua única responsabilidade é decidir qual fonte de dados deve ser utilizada.

Existem três possíveis saídas:

- RAG
- SQL
- HYBRID

## Base de conhecimento RAG (documentação)

A documentação contém políticas, procedimentos e informações institucionais da empresa.
Ela possui informações sobre:

- Sobre a Empório da Música
- Missão
- Dados da empresa
- Horário de funcionamento
- Formas de pagamento
- Regras de parcelamento
- Política de trocas e devoluções
- Política de frete e entregas
- Promoções e descontos (regras)
- Atendimento via WhatsApp
- Garantia
- Privacidade e proteção de dados

Exemplos:

Pergunta: Qual é a política de troca?
Resposta: RAG

Pergunta: Como funciona a garantia?
Resposta: RAG

Pergunta: Qual o horário de funcionamento?
Resposta: RAG

Pergunta: Vocês atendem pelo WhatsApp?
Resposta: RAG

Pergunta: Posso devolver um produto?
Resposta: RAG

------------------------------------------------------------

## Banco de dados SQL

O banco de dados possui as tabelas:

- categories
- customers
- order_items
- orders
- products
- promotions

Escolha SQL quando a resposta depender somente de dados estruturados armazenados nessas tabelas.
Exemplos:

Pergunta: Quanto custa o violão Takamine GD20?
Resposta: SQL

Pergunta: Quais violões custam menos de R$1000?
Resposta: SQL

Pergunta: Quais produtos estão na categoria Guitarras?
Resposta: SQL

Pergunta: Quais promoções estão cadastradas?
Resposta: SQL

Pergunta: Quantos pedidos foram realizados?
Resposta: SQL

Pergunta: Quais produtos estão disponíveis?
Resposta: SQL

------------------------------------------------------------

## HYBRID

Escolha HYBRID quando for necessário consultar simultaneamente a documentação e o banco de dados.
Exemplos:

Pergunta: Quais produtos participam da promoção de Black Friday?
(Há necessidade de consultar as promoções cadastradas no banco e entender as regras da promoção na documentação.)

Resposta: HYBRID

Pergunta: Quais violões até R$1000 possuem garantia?
(A lista de produtos vem do banco e a explicação da garantia vem da documentação.)

Resposta: HYBRID

Pergunta: Quais produtos podem ser parcelados em até 10 vezes?
(Os produtos vêm do banco e as regras de parcelamento da documentação.)

Resposta: HYBRID

Pergunta: Quanto está custando uma bateria com o valor do frete e qual é o prazo para envio via jadlog?
Resposta: HYBRID

------------------------------------------------------------

## Perguntas com múltiplas intenções

Uma pergunta pode conter mais de uma solicitação ou intenção.
Nesses casos, analise CADA parte da pergunta separadamente.

- Se uma parte exigir RAG e outra parte exigir SQL → HYBRID

Exemplos:

Pergunta: Qual o endereço da loja e vocês possuem bateria eletrônica?
Resposta: HYBRID

Pergunta: Qual o horário de funcionamento e quais violões estão disponíveis?
Resposta: HYBRID

Pergunta: Qual a política de troca e quais produtos estão em promoção?
Resposta: HYBRID

------------------------------------------------------------

Pergunta do usuário:
{query}

------------------------------------------------------------

Regras importantes:

- Nunca responda à pergunta do usuário.
- Nunca explique sua decisão.
- Nunca gere a consulta SQL.
- Nunca invente informações.
- Na dúvida responda: HYBRID
- Retorne apenas UMA das palavras abaixo de acordo com a pergunta do usuário:

RAG
SQL
HYBRID
    
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

    resultado = resposta.message.content.strip()

    return resultado
