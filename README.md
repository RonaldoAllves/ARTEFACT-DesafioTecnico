## 📦 Requisitos

- Python 3.8+
- Ollama instalado e rodando

### Modelos Ollama Necessários

```bash
ollama pull qwen2.5-coder:7b      # LLM Principal (~5GB)
```

### Dependências Python

pandas>=1.3.0
numpy>=1.21.0
torch>=1.10.0
scikit-learn>=1.0.0
sentence-transformers>=2.2.0
pypdf>=3.0.0
sqlite3 # Built-in

---

# Todas as instruções necessárias para rodar o projeto

O código principal do projeto está localizado em:

./src/instrument_rag.ipynb

O diretório ./test foi usado inicialmente para validar as etapas, esse diretório não é necessário, ele foi excluído, mas nos commits tem a evolução dele.

O notebook contém toda a implementação do pipeline desenvolvido para o desafio técnico, incluindo:

- Criação do banco de dados SQLite a partir dos arquivos CSV;
- Processamento do PDF de políticas da empresa;
- Geração dos embeddings;
- Indexação dos documentos;
- Recuperação híbrida (BM25 + BGE-M3);
- Reordenação (reranking);
- Classificação do tipo de consulta (RAG, SQL ou HYBRID);
- Geração da resposta final utilizando um LLM local.

O projeto foi desenvolvido utilizando um modelo local executado através do Ollama, eliminando custos com APIs e facilitando a reprodução do ambiente.
Os arquivos CSV fornecidos são utilizados para gerar automaticamente o banco de dados SQLite, enquanto o PDF de políticas é processado para criação dos embeddings utilizados pelo mecanismo de RAG.

Embora o desafio possua apenas um PDF, TODA a estrutura foi preparada para suportar a adição de novos documentos futuramente.

---

# Justificativa das decisões técnicas

Antes do desenvolvimento, foi realizada uma pesquisa bibliográfica sobre os avanços mais recentes em arquiteturas RAG. Como essa área evoluiu significativamente nos últimos anos, optei por revisar a literatura científica para entender quais abordagens vêm sendo utilizadas atualmente.

Essa etapa foi realizada com auxílio da funcionalidade "Pesquisa Aprofundada" do ChatGPT, que serviu como ponto de partida para localizar artigos científicos recentes. Após essa pesquisa, foram dedicadas algumas horas à leitura dos trabalhos e ao planejamento da arquitetura utilizada no desafio.

Como o prazo de desenvolvimento era de apenas dois dias, optei por não realizar fine-tuning de modelos de recuperação. Além disso, escolhi utilizar um LLM local através do Ollama, por ser uma solução gratuita, simples de configurar e suficiente para a quantidade relativamente pequena de dados disponibilizada no desafio.

Como já havia trabalhado anteriormente com RAG durante minha pós-graduação, considerei algumas alternativas de recuperação de informação.

- Uma possibilidade seria utilizar MPNet, porém esse modelo normalmente apresenta melhores resultados após fine-tuning, o que estava fora do escopo devido ao tempo disponível.
- Também considerei o uso do ColBERT, que possui excelente desempenho, porém apresenta maior complexidade de instalação e configuração.

Com base na literatura recente e buscando uma solução simples, eficiente e rápida de implementar, optei pela seguinte arquitetura de recuperação:

- BM25 para recuperação lexical;
- BGE-M3 para recuperação semântica;
- Fusão dos resultados utilizando Reciprocal Rank Fusion (RRF);
- Reordenação dos documentos utilizando BGE-Reranker-v2-M3.

Essa abordagem permite combinar as vantagens da busca lexical e da busca semântica, aumentando a qualidade dos documentos recuperados antes da geração da resposta.

Em relação aos documentos, havia apenas um PDF contendo as políticas da empresa. Embora fosse possível enviar o documento inteiro como contexto, essa estratégia não seria adequada devido às limitações de janela de contexto do modelo local utilizado. Por esse motivo, o PDF foi particionado por páginas, sendo gerado um embedding para cada uma delas. Além de reduzir o contexto enviado ao modelo, essa estratégia deixa o pipeline preparado para suportar múltiplos PDFs futuramente.

Para o armazenamento estruturado das informações, foi utilizado SQLite.
A escolha foi motivada principalmente pela facilidade de distribuição do projeto, já que o SQLite não exige instalação de servidores adicionais e permite que qualquer avaliador execute o sistema imediatamente.
Inicialmente o banco foi criado diretamente a partir dos arquivos CSV. Durante os testes, entretanto, observei que era importante identificar corretamente o tipo de cada coluna, principalmente colunas numéricas, para aumentar a assertividade das consultas SQL geradas automaticamente pelo modelo.

A estratégia utilizada para responder às perguntas consiste em identificar primeiro qual mecanismo é mais adequado para cada consulta.
Foi utilizada uma LLM responsável apenas por classificar a pergunta em uma das seguintes categorias:

- RAG: perguntas respondidas utilizando apenas os documentos.
- SQL: perguntas respondidas consultando o banco de dados.
- HYBRID: perguntas que necessitam combinar informações provenientes tanto do banco quanto dos documentos.

Essa decisão permite utilizar a estratégia mais apropriada para cada tipo de pergunta, evitando consultas desnecessárias e melhorando a qualidade das respostas.

Uma decisão proposital foi utilizar apenas o documento de maior relevância (k = 1) após o reranking.
Durante os testes, verifiquei que enviar vários chunks ao modelo local aumentava significativamente as alucinações e, em diversos casos, impedia que o modelo produzisse uma resposta adequada devido ao aumento do tamanho do contexto.

Caso fosse utilizado um modelo com maior janela de contexto, a estratégia ideal seria recuperar mais documentos e incluir também páginas vizinhas do documento recuperado (por exemplo, páginas anterior e posterior), reduzindo a perda de informações importantes.

A construção dos prompts também levou em consideração as limitações do modelo local. Ou seja, todos os prompts foram desenvolvidos buscando um equilíbrio entre serem suficientemente informativos e, ao mesmo tempo, compactos, evitando consumir desnecessariamente a janela de contexto.
Os prompts foram refinados iterativamente durante os testes até atingir um desempenho satisfatório.

Já o prompt responsável pela geração da resposta final foi elaborado utilizando o próprio documento de políticas da empresa como referência. O PDF foi fornecido ao ChatGPT com a solicitação de construir um prompt que seguisse as orientações do desafio, principalmente no aspecto de assumir uma persona alinhada à identidade e ao tom de atendimento da loja.

---

# Limitações conhecidas e o que eu faria com mais tempo

Embora o projeto tenha atingido resultados satisfatórios dentro do prazo disponível, existem diversas melhorias que seriam implementadas caso eu tivesse mais tempo de desenvolvimento.

- A primeira delas seria migrar toda a arquitetura para LangChain, aproveitando principalmente o gerenciamento do histórico de conversas e outras abstrações que facilitam a construção de agentes conversacionais.
- Também seria realizado um tratamento mais robusto do PDF, preservando de forma consistente tabelas, imagens e demais elementos estruturais do documento. Nesse aspecto, o próprio LangChain oferece integrações que simplificam esse processo.
- Outra melhoria importante seria utilizar um modelo de linguagem mais robusto. Isso permitiria construir prompts mais completos, especialmente para a etapa de Text-to-SQL, onde fornecer um maior número de exemplos costuma aumentar a qualidade das consultas SQL geradas.
- Também seria desenvolvido um front-end mais elaborado, proporcionando uma melhor experiência de uso para o usuário final.

Por fim, o foco durante os dois dias de desenvolvimento foi extrair a melhor qualidade possível dentro das limitações de tempo e infraestrutura disponíveis.

Os testes realizados demonstraram que, mesmo utilizando um LLM local, o sistema foi capaz de produzir respostas coerentes e satisfatórias. Dessa forma, acredito que a simples substituição do modelo por um LLM proprietário ou de maior capacidade resultaria em ganhos adicionais de qualidade sem necessidade de alterações na arquitetura desenvolvida.

---

# Uso de assistentes de código

Durante o desenvolvimento foram utilizados assistentes de IA como apoio ao processo de implementação.

Inicialmente foi utilizada a funcionalidade "Pesquisa Aprofundada" do ChatGPT para realizar uma revisão rápida da literatura sobre arquiteturas RAG atuais. Essa etapa auxiliou na identificação de abordagens recentes utilizadas pela comunidade científica e serviu como base para o planejamento da solução adotada.

Ao longo da implementação, o ChatGPT também foi utilizado como apoio para esclarecer dúvidas pontuais, discutir alternativas de arquitetura, revisar trechos de código e acelerar o desenvolvimento de componentes específicos.

Toda a definição da arquitetura, seleção das tecnologias, testes e ajustes do sistema foram realizados manualmente. O assistente foi utilizado como uma ferramenta de apoio para pesquisa, validação de ideias e aumento da produtividade durante o curto período disponível para o desenvolvimento.
