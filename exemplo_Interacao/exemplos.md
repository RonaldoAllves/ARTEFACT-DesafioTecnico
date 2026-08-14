Abaixo estão as respostas obtidas em algumas perguntas. O que de fato é gerado para o usuário é a resposta final,
no entanto eu coloquei também o resultado do sql e de ranqueamento.

### PRIMEIRA PERGUNTA (fora do escopo)

query = "Quantos Estados tem no Brasil?"

--- Resultados do SQL ---
SELECT COUNT(DISTINCT city) FROM customers;

Colunas: ['COUNT(DISTINCT city)']
(5,)

--- Resposta final (aparece para o usuário) ---

Olá! Obrigado por perguntar. Infelizmente, não posso fornecer informações sobre o número de estados no Brasil diretamente em resposta a essa pergunta.
No entanto, se você tiver alguma dúvida sobre instrumentos musicais, formas de pagamento ou qualquer outra coisa relacionada à Empório da Música, ficarei feliz em ajudar!

### SEGUNDA PERGUNTA (nivel simples - RAG)

query = "Qual é o prazo de devolução?"

--- Resultados do reranking ---

Score: 4.3272
Documento: politicas_da_loja.pdf
Página: 4
Chunk: politicas_da_loja_p4

--- Resposta final (aparece para o usuário) ---

Olá! Obrigado por perguntar. De acordo com nossa política, você tem até **7 dias corridos** para solicitar a devolução do produto que comprou conosco, desde que ele esteja em sua embalagem original, sem sinais de uso e com todos os acessórios e manuais intactos.

Se precisar de mais alguma ajuda ou tiver outras dúvidas, é só me chamar!

### TERCEIRA PERGUNTA (nivel SQL)

query = "Qual é o instrumento mais barato e o mais caro?"

--- Resultados do SQL ---
SELECT _ FROM ( SELECT name AS instrumento , description AS descricao , price_brl AS preco , 'Mais Barato' AS tipo FROM products WHERE status = 'active' ORDER BY price_brl ASC LIMIT 1 ) UNION ALL SELECT _ FROM ( SELECT name AS instrumento , description AS descricao , price_brl AS preco , 'Mais Caro' AS tipo FROM products WHERE status = 'active' ORDER BY price_brl DESC LIMIT 1 )

Colunas: ['instrumento', 'descricao', 'preco', 'tipo']
('Shelby SU-21S Soprano Sunburst', 'Ukulele soprano com acabamento Sunburst e escala em Rosewood. Visual clássico e som alegre para músicos de todos os níveis.', 159.9, 'Mais Barato')
('Teclado Sintetizador Nord Synth 2 Pro', 'Piano de palco Nord Stage com seções independentes de piano, órgão e synth. Interface intuitiva e qualidade sonora padrão da indústria.', 19567.0, 'Mais Caro')

--- Resposta final (aparece para o usuário) ---

Olá! Tudo ótimo aqui na Empório da Música. Vou te ajudar a encontrar os instrumentos que você está procurando.

**Instrumento Mais Barato:**

- **Ukulele Shelby SU-21S Soprano Sunburst**: R$ 159,90

**Instrumento Mais Caro:**

- **Teclado Sintetizador Nord Synth 2 Pro**: R$ 19.567,00

Se você quiser mais informações sobre qualquer um desses instrumentos ou precisar de ajuda com algo mais, é só me chamar!

### QUARTA PERGUNTA (nível menos trivial)

query = "Quais os intrumentos de percussão vocês vendem?"

--- Resultados do SQL ---
SELECT p.
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE
c.name LIKE '%percussão%'
OR c.description LIKE '%percussão%'
OR p.name LIKE '%percussão%'
OR p.description LIKE '%percussão%'
OR p.specs LIKE '%percussão%'

Colunas: ['product_id', 'price_brl', 'name', 'category_id', 'description', 'stock_quantity', 'status', 'specs', 'created_at']
(139, 4439.0, 'Bateria Acústica Yamaha Kit 1 Studio', 3, 'Bateria acústica Pearl Export com cascos em Poplar e mogno asiático. Sonoridade encorpada e ferragens reforçadas para o dia a dia.', 8, 'active', '{"shells": "Maple", "pieces": "5", "hardware": "included", "color": "Blue"}', '2024-01-10')
(140, 13285.0, 'Bateria Acústica Pearl Kit 2 Studio', 3, 'Bateria acústica Tama com cascos 100% Birch e sistema de suspensão Star-Mount. Ataque explosivo e excelente projeção em palcos.', 7, 'active', '{"shells": "Maple", "pieces": "5", "hardware": "included", "color": "Black"}', '2022-06-25')
(141, 14922.0, 'Bateria Acústica Yamaha Kit 3 Studio', 3, 'Bateria acústica Yamaha Stage Custom com bumbos profundos e ferragens inclusas. O padrão de confiabilidade e som focado para shows e ensaios.', 8, 'active', '{"shells": "Maple", "pieces": "5", "hardware": "included", "color": "Wine Red"}', '2021-04-18')

--- Resposta final (aparece para o usuário) ---

Olá! Tudo ótimo, e você? 🎶

Na Empório da Música, nós temos uma grande variedade de instrumentos de percussão para atender todas as suas necessidades. Aqui estão alguns dos principais que oferecemos:

- **Baterias Acústicas:** Nossas baterias acústicas são perfeitas para quem quer um som claro e natural em casa ou no palco. Temos opções de diferentes marcas como Yamaha, Tama e Pearl.
  - **Yamaha Kit 1 Studio:** Bateria com cascos em Poplar e mogno asiático, sonoridade encorpada e ferragens reforçadas.
  - **Pearl Kit 2 Studio:** Bateria com cascos 100% Birch e sistema de suspensão Star-Mount.
  - **Yamaha Kit 3 Studio:** Bateria profunda com bumbos profundos e ferragens inclusas.

- **Baterias Elétricas:** Se você gosta de um som mais potente, nossas baterias elétricas são a escolha perfeita. Temos diferentes modelos para atender todas as necessidades.

- **Timbaladas:** Para quem quer uma experiência única no palco, nossas timbaladas adicionam um toque especial ao seu setlist.

- **Xylofones e Maracas:** Se você gosta de algo mais leve e portátil, nossos xylofones e maracas são ideais para shows ou práticas em casa.

Se você tiver alguma dúvida específica sobre qualquer desses instrumentos ou precisar de ajuda com a escolha certa, estou aqui para ajudar! Quer ver mais detalhes sobre algum desses instrumentos?

# QUINTA PERGUNTA

query = "Quais opções de violões disponíveis custando até R$1000?"

--- Resultados do SQL ---
SELECT p.product_id, p.name, p.description, p.price_brl, c.name AS category, p.specs
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.status = 'active'
AND (
p.name LIKE '%violão%'
OR p.name LIKE '%acústico%'
OR p.description LIKE '%violão%'
OR p.description LIKE '%acústico%'
OR c.name LIKE '%violão%'
OR c.name LIKE '%acústico%'
OR c.description LIKE '%violão%'
OR c.description LIKE '%acústico%'
)
AND p.price_brl <= 1000;

Colunas: ['product_id', 'name', 'description', 'price_brl', 'category', 'specs']
(81, 'Yamaha C40 Nylon Natural', 'Violão clássico com tampo em Spruce e fundo/laterais em Meranti. Ideal para estudantes e iniciantes, com excelente projeção sonora.', 599.9, 'Violões', '{"top":"Spruce","back_sides":"Meranti","neck":"Nato","strings":"nylon","scale":"650mm","electronics":"no","color":"Natural"}')
(82, 'Yamaha C70 Nylon Natural', 'Violão clássico de nível intermediário com tampo em Spruce sólido. Acabamento de alta qualidade e timbre equilibrado.', 849.0, 'Violões', '{"top":"Spruce Sólido","back_sides":"Nato","neck":"Nato","strings":"nylon","scale":"650mm","electronics":"no","color":"Natural"}')
(83, 'Tagima Memphis AC-39 Nylon Natural', 'Violão clássico com cordas de nylon, perfeito para quem está começando. Corpo leve e confortável para longas sessões de estudo.', 429.9, 'Violões', '{"top":"Linden","back_sides":"Linden","neck":"Nato","strings":"nylon","scale":"650mm","electronics":"no","color":"Natural"}')
(84, 'Giannini GN-15 Nylon Cedr Natural', 'Violão clássico Giannini com tampo em cedro. Sonoridade quente e encorpada, excelente custo-benefício para estudantes avançados.', 689.0, 'Violões', '{"top":"Cedro","back_sides":"Sapele","neck":"Cedro","strings":"nylon","scale":"650mm","electronics":"no","color":"Natural"}')
(85, 'Rozini RC-104 Nylon Estudante', 'Violão clássico de estudo da Rozini, feito com madeiras nacionais. Acabamento caprichado e preço acessível para iniciantes.', 459.9, 'Violões', '{"top":"Spruce","back_sides":"Sapele","neck":"Nato","strings":"nylon","scale":"650mm","electronics":"no","color":"Natural"}')
(86, 'Tagima Dallas Tuner Aço Natural', 'Violão folk com cordas de aço e afinador integrado. Corpo confortável e som brilhante, ideal para acompanhamento vocal.', 749.0, 'Violões', '{"top":"Spruce","back_sides":"Sapele","neck":"Nato","strings":"steel","scale":"648mm","electronics":"no","color":"Natural"}')
(87, 'Yamaha F310 Aço Natural', 'Violão folk aço Yamaha com corpo robusto e timbre encorpado. Um dos modelos mais vendidos do mundo para iniciantes e intermediários.', 699.9, 'Violões', '{"top":"Spruce","back_sides":"Meranti","neck":"Nato","strings":"steel","scale":"634mm","electronics":"no","color":"Natural"}')
(88, 'Giannini GF-1R Aço Folk Sunburst', 'Violão folk com tampo em Spruce e acabamento Sunburst clássico. Som equilibrado e visual elegante para palco e estúdio.', 579.9, 'Violões', '{"top":"Spruce","back_sides":"Sapele","neck":"Nato","strings":"steel","scale":"648mm","electronics":"no","color":"Sunburst"}')
(89, 'Shelby SN-100 Folk Aço Preto', 'Violão folk aço com visual moderno em preto. Indicado para quem busca um instrumento versátil com boa relação custo-benefício.', 549.0, 'Violões', '{"top":"Linden","back_sides":"Linden","neck":"Nato","strings":"steel","scale":"648mm","electronics":"no","color":"Preto"}')
(91, 'Tagima Woodstock Dreadnought Natural', 'Violão dreadnought com corpo amplo e som potente. Excelente para fingerpicking e strumming com projeção impressionante.', 899.0, 'Violões', '{"top":"Spruce","back_sides":"Sapele","neck":"Nato","strings":"steel","scale":"650mm","electronics":"no","color":"Natural"}')
(96, 'Giannini GF-3D Dreadnought Sunburst', 'Violão dreadnought com corpo amplo e acabamento Sunburst. Volume alto e graves profundos, ideal para country e pop.', 799.9, 'Violões', '{"top":"Spruce","back_sides":"Sapele","neck":"Nato","strings":"steel","scale":"650mm","electronics":"no","color":"Sunburst"}')
(107, 'Shelby SGD-195E Elétrico Aço Sunburst', 'Violão eletroacústico dreadnought com captação e afinador integrado. Boa opção de custo-benefício para quem precisa de amplificação.', 799.0, 'Violões', '{"top":"Spruce","back_sides":"Sapele","neck":"Nato","strings":"steel","scale":"650mm","electronics":"yes","color":"Sunburst"}')
(112, 'Tagima TW-7 7 Cordas Aço Natural', 'Violão 7 cordas com cordas de aço para estilos que exigem projeção extra. Braço confortável com tensor regulável.', 999.0, 'Violões', '{"top":"Spruce","back_sides":"Sapele","neck":"Nato","strings":"steel","scale":"650mm","electronics":"no","color":"Natural"}')
(122, 'Kalani KAL-500C Concert Elétrico Natural', 'Ukulele concert eletroacústico com captação piezo e pré-amplificador. Versátil para palco e estúdio com timbre amplificado fiel.', 479.0, 'Ukuleles', '{"top":"Mogno","back_sides":"Mogno","neck":"Mogno","strings":"nylon","scale":"381mm","electronics":"yes","color":"Natural"}')
(123, 'Kala KA-SMHCE Concert Elétrico Mogno', 'Ukulele concert eletroacústico Kala com tampo sólido em mogno e captação. Acabamento premium e som rico para performances profissionais.', 899.0, 'Ukuleles', '{"top":"Mogno Sólido","back_sides":"Mogno","neck":"Mogno","strings":"nylon","scale":"381mm","electronics":"yes","color":"Natural"}')
(128, 'Kala KA-B Barítono Mogno', 'Ukulele barítono Kala em mogno com afinação em DGBE. Corpo amplo com graves profundos, uma ponte entre o ukulele e o violão.', 599.0, 'Ukuleles', '{"top":"Mogno","back_sides":"Mogno","neck":"Mogno","strings":"nylon","scale":"502mm","electronics":"no","color":"Natural"}')

--- Resposta final (aparece para o usuário) ---

Olá! Temos várias opções de violões disponíveis com preços até R$1.000,00. Aqui estão as principais sugestões para você:

### **Violões até R$ 800,00**

- **Tagima Memphis AC-39 Nylon Natural** – R$ 429,90  
  _Violão clássico leve e confortável para iniciantes._
- **Rozini RC-104 Nylon Estudante** – R$ 459,90  
  _Custo-benefício com madeiras nacionais e acabamento caprichado._
- **Giannini GN-15 Nylon Cedr Natural** – R$ 689,00  
  _Sonoridade quente e corpo confortável para longas sessões._
- **Shelby SN-100 Folk Aço Preto** – R$ 549,00  
  _Visual moderno e som brilhante para acompanhamento vocal._

### **Violões entre R$ 800,00 e R$ 1.000,00**

- **Yamaha C40 Nylon Natural** – R$ 599,90  
  _Violão clássico ideal para estudantes, com excelente projeção sonora._
- **Yamaha C70 Nylon Natural** – R$ 849,00  
  _Nível intermediário com tampo em Spruce sólido e acabamento de alta qualidade._
- **Tagima Woodstock Dreadnought Natural** – R$ 899,00  
  _Dreadnought potente, perfeito para fingerpicking e strumming._
- **Giannini GF-3D Dreadnought Sunburst** – R$ 799,90  
  _Volume alto e graves profundos, ideal para country e pop._
- **Tagima TW-7 7 Cordas Aço Natural** – R$ 999,00  
  _Versátil para estilos que exigem projeção extra, com braço confortável._

Se quiser, posso ajudar a filtrar por estilo (acústico, folk, dreadnought) ou características como acabamento e tipo de corda! 🎸
