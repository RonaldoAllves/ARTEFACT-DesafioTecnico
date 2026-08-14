import re

def cleanText(texto):
    linhas = texto.splitlines()
    resultado = []

    atual = ""

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            continue

        if atual:
            atual += " " + linha
        else:
            atual = linha

        # Se terminou com ponto final, mantém como uma unidade
        if linha.endswith("."):
            resultado.append(atual)
            atual = ""

    # Caso tenha sobrado texto sem ponto final
    if atual:
        resultado.append(atual)

    return "\n".join(resultado)