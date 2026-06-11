---
name: analise-processual-minuta
version: 0.1.0
description: Diagnostica a fase de um processo cível ou trabalhista e redige a peça cabível — réplica, tutela antecedente, recursos (apelação, agravo, embargos de declaração, RE/REsp, agravo interno, recurso ordinário/inominado/trabalhista, embargos de divergência), cumprimento de sentença, impugnação, embargos à execução, exceção de pré-executividade, embargos de terceiro, oposição, reclamação, ação rescisória, suspensão de segurança e IRDR — fundamentada via MCP da Letra da Lei. Use para "o que faço agora?", "recebi a contestação", "perdi a sentença, como recorro?", "quero apelar/executar/embargar", "cabe [peça/recurso]?". Não use para petição inicial, contestação ou fundamentação judicial — há skills próprias.
argument-hint: "[fase do processo ou documento recebido — ex.: 'recebi a contestação' ou caminho do PDF da sentença]"
---

# /analise-processual-minuta

## ⚠️ PASSO ZERO — OBRIGATÓRIO ANTES DE QUALQUER RASCUNHO

**Não produza nenhuma peça antes de completar o intake.** Esta skill serve a múltiplos momentos processuais — uma peça feita sem diagnóstico da fase é, em regra, inútil ou danosa. Use `AskUserQuestion` para coletar as informações em bloco — máximo 4 perguntas por rodada.

### Perguntas obrigatórias — use AskUserQuestion

**Rodada 1 — Fase e documentos:**
- **O que acabou de acontecer no processo?** (Ex.: "recebi a contestação", "a sentença saiu ontem e perdi", "o juiz deferiu a tutela do autor", "ganhei e quero cobrar".) Se o usuário tiver o(s) documento(s) gerado(s) nessa fase, pedir o arquivo ou o texto colado.
- **Qual é o rito processual?** — procedimento comum, JEC (juizado especial), trabalhista, Fazenda Pública, outro?
- **Qual parte o usuário representa?** — autor(a), réu(é), ambos?
- **Há prazo correndo?** Se sim, qual é a data de publicação/intimação do ato e qual a data-limite que o usuário conhece?

> **Guardrail obrigatório:** Se o usuário não fornecer nenhuma informação sobre a fase do processo e nenhum documento, **não produza nada.** Explique que sem saber em que ponto o processo está, qualquer peça seria genérica e possivelmente inadequada. Ofereça as perguntas acima. **Não ceda se o usuário insistir.** Veja Passo 1 para o roteiro de recusa.

### Protocolo "Informar manualmente" — obrigatório

Após cada rodada de `AskUserQuestion`, verifique se alguma resposta foi **"Informar manualmente"**. Se sim, **não prossiga para a próxima etapa.** Compile todos os itens marcados dessa forma em uma única mensagem e solicite ao usuário que forneça os dados antes de continuar:

> "Você marcou os seguintes itens para preenchimento manual. Por favor, informe cada um antes de prosseguirmos:
> - [item 1]
> - [item 2]
> - ..."

Só avance para a redação quando **todos** os itens "Informar manualmente" tiverem sido respondidos ou explicitamente descartados pelo usuário (ex.: "não tenho esse dado" → marcar `[VERIFICAR]`).

---

1. Colete os documentos e a descrição da fase (Passo 0 acima).
2. **Diagnostique a fase processual** e mapeie qual peça é cabível (Passo 2).
3. **Confirme o diagnóstico com o usuário** antes de redigir qualquer linha.
4. Faça o intake específico para a peça identificada (Passo 3).
5. **Chame `buscar_artigos` para todo dispositivo que entrar na peça** — sem exceção.
6. Estruture e gere o `.docx` + `NOTAS.md` (Passos 4 a 6).

---

# Análise Processual e Minuta

## Propósito

O advogado sabe o que aconteceu; nem sempre sabe qual é a próxima peça, ou como estruturá-la com rigor. Esta skill lê o que está nos autos — ou o que o usuário descreveu — identifica o momento processual, propõe a peça mais adequada e redige o rascunho com fundamentação verificada lei por lei.

O que separa esta skill das demais:

1. **Ela diagnostica antes de redigir.** Nenhuma linha de peça sai sem que a fase processual esteja identificada e confirmada pelo usuário.
2. **Ela cobre a fase pós-postulação no rito comum e trabalhista:** réplica, recursos (apelação, recurso ordinário, agravo, embargos), cumprimento de sentença e execução de obrigação.
3. **Ela não adivinha intenção.** Se o usuário quer recorrer mas a sentença foi favorável, a skill pergunta antes de produzir.

O rascunho gerado **não é peça pronta** — é andaime revisável. Quem assina, ajusta tom e decide estratégia é a pessoa habilitada na OAB.

## Regra absoluta — fontes da peça

### Fonte 1 — Lei federal (MCP)

**Toda citação de lei federal nesta peça vem do MCP da Letra da Lei.** Sem exceção. **Carregue a skill `letra-da-lei:pesquisa-juridica` e siga-a** para qualquer busca — ela define as ferramentas (`buscar_artigos`, `acervo · consultar`, `acervo · listar`, `reclame_aqui`), os parâmetros (`query`, `norma`), os campos retornados e as verificações de vigência (`situacao`) e de texto integral (`is_truncated` → `consultar`). Memória do modelo é proibida para citar artigo — leis mudam.

Regras desta peça (além da `pesquisa-juridica`):
- Citação sem `citacao` + `source_url` da ferramenta → não entra; vira `[CITAÇÃO PENDENTE]`.
- `situacao` ≠ `vigente` → `[VERIFICAR VIGÊNCIA — situação: <X>]`.
- Norma estadual/municipal/infralegal → `[FORA DO CORPUS]`.

### Fonte 2 — Jurisprudência (MCP)

Jurisprudência verificada via MCP da Letra da Lei é uma fonte válida para **todas as peças**. Use as ferramentas conforme o escopo:

- **Federal (STF/STJ/TST/CARF):** `jurisprudencia-federal · buscar_precedentes` (busca ampla — súmulas, temas, OJs, acórdãos) ou `jurisprudencia-federal · buscar_vinculantes` (restringe a precedentes vinculantes do art. 927 CPC: súmulas vinculantes, temas de repercussão geral, temas repetitivos). Filtre por `autoridade` (`STF`, `STJ`, `TST`, `CARF`).
- **Estadual — IRDRs (TJs):** `jurisprudencia-estadual · buscar_vinculantes` (ferramenta distinta) com o parâmetro **obrigatório** `localidade` (sigla da UF, ex.: `"AM"`, ou `"BR"` para busca nacional). IRDR vincula apenas na UF que o decidiu.

**Força do precedente — campo `eficacia` retornado pelo MCP:**
- `vinculante` = observância obrigatória (art. 927 CPC) — citar em qualquer peça sem restrição adicional.
- `obrigatoria` = forte deferência (ex.: súmulas comuns) — citar com o enunciado literal.
- `persuasiva` = subsídio argumentativo — citar com o marcador `[JURISPRUDÊNCIA PERSUASIVA — revisar pertinência ao caso antes do protocolo]`.

**Formato de citação de jurisprudência no rascunho e no .docx:**

```
    [Enunciado literal retornado pelo MCP — sem aspas, recuado 1,25 cm à esquerda,
     alinhamento justificado, fonte 1pt menor que o corpo do texto]
    Fonte: [autoridade] | [tipo] | search_id: [search_id] | eficacia: [eficacia]

[Linha em branco — texto principal retoma aqui]
```

Se o MCP retornar enunciado truncado (`is_truncated: true`), chamar `acervo · consultar` (`dominio: "jurisprudencia"`, `esfera: "federal"` ou `"estadual"`, com os `search_ids` da busca ou uma `citacao` conhecida) para obter o texto integral antes de citar.

**Resultado zero ou precedente não pertinente:** inserir `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`. Nunca copiar enunciado de memória.

**Para o Recurso Extraordinário (RE ao STF):** jurisprudência do STF é estruturalmente necessária. Use `jurisprudencia-federal · buscar_precedentes` com `autoridade: "STF"` para localizar o Tema de Repercussão Geral aplicável. Se o MCP retornar resultado pertinente, cite com o formato acima (sem marcador adicional se `eficacia: vinculante`). Se não retornar, inserir `[JURISPRUDÊNCIA — confirmar Tema e tese antes do protocolo]` em vermelho no .docx.

### Fonte 3 — Autos do processo (petições anteriores)

Quando o usuário enviar o processo completo ou documentos dos autos, a skill pode **extrair e citar conteúdo das peças já produzidas** — especialmente petições anteriores da parte que o usuário representa (inicial, apelação, embargos de declaração etc.).

Regras para uso de fonte dos autos:
- Prioridade: petições anteriores assinadas pelo(a) advogado(a) do usuário, pois revelam as teses já sustentadas e o que foi prequestionado.
- O acórdão recorrido e outras decisões judiciais dos autos **não são jurisprudência** — são objeto do recurso e podem ser citados literalmente para demonstrar o cabimento ou o erro da decisão.
- Ao usar conteúdo dos autos, sinalizar a fonte: `Fonte: [nome do documento nos autos] — [data/ID do documento]`.
- Nunca atribuir à parte contrária argumento que não conste dos autos.

**Formato de citação de documento dos autos no .docx:**

```
    [Trecho literal extraído do documento — sem aspas, recuado 1,25 cm,
     alinhamento justificado, fonte 1pt menor que o corpo]
    Fonte: [nome do documento] — [data/ID] — autos nº [número do processo]

[Linha em branco — texto principal retoma aqui]
```

**Formato obrigatório de citação no rascunho e no .docx:**

```
    [Texto literal retornado pelo MCP — sem aspas, recuado 1,25 cm à esquerda,
     alinhamento justificado, fonte 1pt menor que o corpo do texto]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[Linha em branco — texto principal retoma aqui, com formatação normal]
```

Regras de formatação da citação no .docx:
- **Recuo:** margem esquerda deslocada 1,25 cm (720 DXA) em relação ao texto principal.
- **Alinhamento:** justificado.
- **Fonte:** 1pt menor que o corpo (se o corpo for 12pt, a citação é 11pt).
- **Sem aspas:** o texto da lei não leva aspas de abertura nem de fechamento.
- **Fonte abaixo:** a linha "Fonte: ..." vem imediatamente após o texto da lei, na mesma formatação recuada e menor. Não vem antes.
- **Linha em branco após:** após o bloco citação + fonte, uma linha em branco separa do próximo parágrafo de texto principal.

Se o bloco `Fonte:` não puder ser preenchido (citacao ou source_url ausentes), o artigo não foi buscado via MCP — não entra na peça.

## Passo 1 — Guardrail: sem fase, sem peça

Se o usuário não forneceu:
- nenhuma descrição do que aconteceu no processo, **E**
- nenhum documento (inicial, contestação, sentença, decisão, etc.),

responda com clareza e firmeza:

> "Para redigir a peça certa, preciso saber em que ponto o processo está. Sem essa informação, qualquer minuta seria genérica e possivelmente inadequada para o seu caso. Me conta: (a) o que acabou de acontecer? (b) qual é o documento mais recente do processo — contestação, sentença, decisão interlocutória, algo do tribunal? (c) você representa o(a) autor(a) ou o(a) réu(é)?"

Se o usuário insistir ("monta uma apelação genérica", "faz um modelo de réplica") **mantenha a recusa.** Uma apelação sem a sentença que se ataca não tem como ser fundamentada — ela é pura forma vazia. Explique isso de forma direta, sem julgamento. Não ceda nas duas insistências. Resposta direta, sem moralismo.

## Passo 2 — Diagnóstico da fase e mapa de peça cabível

Após receber os documentos ou a descrição da fase, diagnostique e mapeie:

| Fase identificada | Peça cabível | Base legal |
|---|---|---|
| Autor recebeu contestação — réu arguiu matérias do art. 337 ou fatos extintivos/modificativos/impeditivos | Réplica **obrigatória** | CPC arts. 350-351 |
| Autor recebeu contestação — réu não arguiu matérias novas | Réplica **facultativa** (estratégica) | CPC art. 350 |
| Parte precisa de medida urgente antes de ajuizar a ação principal — urgência que antecipa o próprio bem da vida pretendido | Tutela antecipada antecedente | CPC art. 303 |
| Parte precisa de medida urgente para **assegurar** o resultado da ação principal — não antecipa o bem da vida, mas garante a utilidade do processo futuro | Tutela cautelar antecedente | CPC arts. 305-310 |
| Parte perdeu sentença — rito comum ou especial (não JEC, não trabalhista) | Apelação | CPC arts. 1.009-1.014 |
| Parte recebeu decisão interlocutória que consta no rol do art. 1.015 do CPC | Agravo de instrumento | CPC arts. 1.015-1.020 |
| Parte recebeu sentença/decisão com omissão, contradição, obscuridade ou erro material | Embargos de declaração | CPC arts. 1.022-1.026 |
| Parte ganhou sentença de pagar quantia — quer cobrar | Cumprimento de sentença (quantia) | CPC arts. 523-527 |
| Parte ganhou sentença de obrigação de fazer/não fazer — quer cobrar | Cumprimento de sentença (obrigação) | CPC art. 536 |
| Parte ganhou sentença de entregar coisa — quer cobrar | Cumprimento de sentença (entrega) | CPC art. 538 |
| Executado quer se defender em cumprimento de sentença de quantia certa — transcorridos os 15 dias do art. 523 sem pagamento | Impugnação ao cumprimento de sentença | CPC art. 525 |
| Executado quer se defender em execução de **título extrajudicial** (cheque, nota promissória, contrato, CDA etc.) | Embargos à execução | CPC arts. 914-917 |
| Executado quer arguir matéria de **ordem pública** (prescrição, nulidade do título, ilegitimidade) **sem penhora prévia e sem dilação probatória**, em qualquer execução | Exceção de pré-executividade | Construção pretoriana — STJ Súmula 393; âncora normativa: CPC art. 803, par. único |
| **Terceiro que não é parte** no processo sofre penhora, arresto ou constrição sobre bem seu | Embargos de terceiro | CPC arts. 674-681 |
| Parte perdeu sentença da Vara do Trabalho | Recurso ordinário trabalhista | CLT art. 895, I |
| Parte perdeu sentença de juizado especial cível (JEC) | Recurso inominado | Lei 9.099 art. 41 |
| Parte perdeu acórdão de TRF, TJ ou TST e quer levar questão constitucional ao STF — após esgotadas as vias ordinárias (inclusive embargos de declaração para prequestionamento) | Recurso Extraordinário | CF art. 102, III, "a" + CPC arts. 1.029-1.035 |
| Parte perdeu acórdão de TRF ou TJ e quer levar questão de direito federal infraconstitucional ao STJ | Recurso Especial (REsp) | CF art. 105, III + CPC arts. 1.029-1.032 |
| ⚠️ Acórdão de TRF ou TJ viola **simultaneamente** lei federal infraconstitucional **e** a Constituição Federal | **RE + REsp interpostos simultaneamente** em petições separadas ao mesmo Presidente/VP do tribunal de origem | CF arts. 102 III "a" e 105 III + CPC art. 1.031 — a não interposição de um implica preclusão da matéria correspondente |
| Presidente/VP do tribunal de origem negou seguimento ao RE/REsp por inadmissibilidade geral (art. 1.030, V, CPC) — motivo não é conformidade com repetitivo/RG | Agravo em RE ou Agravo em REsp (ARE/AREsp) ao tribunal superior | CPC art. 1.042 |
| Acórdão de turma do STJ ou STF em RE/REsp **diverge de outro acórdão do mesmo tribunal** sobre a mesma questão | Embargos de divergência | CPC arts. 1.043-1.044 |
| Presidente/VP do tribunal de origem negou seguimento ao RE ou REsp **com fundamento em conformidade com entendimento de casos repetitivos ou RG** (art. 1.030, I ou III, CPC) | Agravo Interno ao próprio tribunal de origem | CPC arts. 1.021 + 1.030, §2º |
| Relator do tribunal (qualquer instância) proferiu decisão monocrática e a parte quer submeter ao colegiado | Agravo Interno | CPC art. 1.021 |
| Tribunal **denegou** HC/MS/HD/MI em **competência originária** (única instância) e a parte vencida quer recorrer | Recurso Ordinário Constitucional | CF art. 102, II (ao STF) ou 105, II (ao STJ) + CPC arts. 1.027-1.028 |
| Ato/decisão usurpou competência de tribunal, descumpriu decisão dele, ou contrariou súmula vinculante, decisão do STF em controle concentrado, IRDR ou IAC — **antes** do trânsito em julgado | Reclamação constitucional | CPC arts. 988-993 |
| Decisão **de mérito transitada em julgado** padece de um dos vícios do art. 966 (incompetência absoluta, violação manifesta de norma, prova falsa, prova nova, erro de fato etc.) | Ação Rescisória | CPC arts. 966-975 |
| Terceiro (que não é parte na ação) pretende a coisa ou o direito disputado entre autor e réu — sentença ainda não proferida | Oposição | CPC arts. 682-686 |
| **Poder Público** quer suspender liminar/sentença concessiva de MS ou tutela de urgência que cause grave lesão à ordem, saúde, segurança ou economia públicas | Suspensão de segurança | Lei 12.016/2009 art. 15 (MS) / Lei 8.437/1992 art. 4 [FORA DO CORPUS] (outras ações) |
| Há **múltiplos processos** com mesma questão unicamente de direito e risco de decisões divergentes — parte, MP ou Defensoria quer fixar tese vinculante no tribunal | Suscitação de IRDR | CPC arts. 976-987 |
| ⚠️ Situação não coberta por nenhum módulo acima | **Módulo subsidiário** — a skill diagnostica a fase e orienta o próximo passo, mas informa que não há minuta específica disponível | — |

**Antes de prosseguir, devolva o diagnóstico ao usuário para confirmação:**

> "Com base no(s) documento(s) fornecido(s), a fase que identifico é: [fase]. A peça mais adequada é: [peça], com fundamento no(s) art(s). [X] do [diploma]. Confirmo o entendimento antes de redigir — está correto?"

Só redigia após a confirmação. Se o usuário discordar, pergunte o que está errado e ajuste.

## Passo 3 — Intake específico por tipo de peça

Após confirmar o diagnóstico, faça o intake específico para a peça identificada. Use `AskUserQuestion` — máximo 4 perguntas por rodada.

> **Distinção estrutural — recursos × ações autônomas de impugnação (ler antes de qualquer módulo).**
> A natureza da peça molda o intake e a estrutura. Não tratar as duas categorias do mesmo jeito:
>
> - **Recursos** (apelação, agravo de instrumento, embargos de declaração, recurso ordinário trabalhista, recurso inominado, RE, REsp, ARE/AREsp, agravo interno, recurso ordinário constitucional): impugnam decisão **dentro do mesmo processo** e têm **prazo de interposição** (em regra em dias úteis, contados da intimação). A peça abre por uma seção de **tempestividade**.
> - **Ações autônomas de impugnação** (reclamação, ação rescisória): **não são recursos** — instauram **processo novo**. O intake e a estrutura aproximam-se de uma **petição inicial** (qualificação completa das partes, causa de pedir, pedido, valor da causa, instrução documental — requisitos do art. 319 e seguintes), não do fluxo recursal. **Não há "tempestividade recursal"** — há cabimento de ação e, conforme o caso, prazo decadencial ou limite negativo:
>   - **Ação rescisória:** prazo **decadencial** (não de interposição). 2 anos com termo inicial **variável** conforme a hipótese do art. 966 — regra geral do trânsito em julgado da última decisão; **descoberta da prova nova** no inciso VII (teto de 5 anos); **ciência da simulação/colusão** para terceiro prejudicado e MP (art. 975, §§2º e 3º). Ver módulo da rescisória.
>   - **Reclamação:** sem prazo de interposição, mas **inadmissível após o trânsito em julgado** da decisão reclamada (art. 988, §5º, I). Ver módulo da reclamação.
>
> Tratar uma ação autônoma como recurso (ou vice-versa) é erro estrutural — e é o erro que mais escapa em refatorações. Confirmar a natureza antes de escolher o esqueleto da peça.

---

**Grupo 3.1 — Fase de conhecimento — resposta**

### 3.1.1 — Réplica (CPC arts. 350-351)

**Intake:**
- A contestação foi lida? Pedir o arquivo ou texto.
- O(a) réu(é) arguiu alguma das matérias do art. 337 (preliminares)?
- O(a) réu(é) alegou fato extintivo, modificativo ou impeditivo do direito do autor (ex.: pagamento, prescrição, novação)?
- Há documentos novos que o autor quer juntar em réplica?

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO [...]

Processo nº [...]

[NOME DO AUTOR], por seu(sua) advogado(a), vem apresentar

                              R É P L I C A

à contestação apresentada por [NOME DO RÉU], nos seguintes termos:

I — DAS PRELIMINARES ARGUIDAS PELA DEFESA   (omitir se não houver)

I.1 — [Preliminar arguida — refutação com texto literal via MCP + subsunção ao caso]

    [texto literal do art. 337, [inciso], do CPC via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Aplicação ao caso. Por que a preliminar não se sustenta.]

II — DAS MATÉRIAS NOVAS ARGUIDAS NA CONTESTAÇÃO  (art. 350, primeira parte)

[Cada fato extintivo/modificativo/impeditivo alegado pelo réu → contraposição
factual + documental do autor. Referência a doc. nº: "[DOC. A NUMERAR]" se
o usuário não numerou os documentos.]

III — DOS DOCUMENTOS NOVOS  (se aplicável — buscar art. 435 via MCP)

    [texto literal do art. 435 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Justificar tempestividade ou razão de terem surgido após a inicial.]

IV — DO PEDIDO

Requer o(a) autor(a) que Vossa Excelência:
  a) rejeite as preliminares arguidas;
  b) afaste os fatos impeditivos/modificativos/extintivos alegados;
  c) prossiga no julgamento do feito, julgando procedentes os pedidos da inicial.

Termos em que pede deferimento.
[Cidade], [data].
```

---

### 3.1.2 — Tutela antecipada antecedente (CPC art. 303)

> ⚠️ **AÇÃO ANTECEDENTE — NÃO É RECURSO.** A tutela antecipada antecedente instaura **processo novo** com petição inicial (ainda que reduzida). Não há "tempestividade recursal". O intake segue a estrutura de petição inicial — qualificação das partes, causa de pedir sumária, pedido de tutela, valor da causa. O conteúdo completo vem depois, no **aditamento** (art. 303, §1º, I).

**Intake:**
- Qual é a urgência contemporânea ao ajuizamento que impede aguardar a instrução?
- Qual é o **pedido de tutela final** (o que o autor quer ao final do processo)? A petição inicial deve indicar esse pedido mesmo que de forma sumária.
- Já há elementos suficientes para demonstrar **probabilidade do direito** e **perigo de dano** (art. 300)?
- Qual o **valor da causa** — deve considerar o pedido final (art. 303, §4º)?
- Se a tutela for concedida, o autor sabe que tem **15 dias** para aditar a petição inicial com argumentação completa e documentos (art. 303, §1º, I)?

**Nota crítica — estabilização (art. 304):**
Se a tutela antecipada for concedida e o réu **não interpuser o recurso cabível** (agravo de instrumento), a tutela **estabiliza-se** e o processo é extinto (art. 304, §1º). Isso **não é coisa julgada** — a tutela estabilizada pode ser revista, reformada ou invalidada em ação autônoma, mas o direito de pleitear isso extingue-se em **2 anos** contados da extinção do processo (art. 304, §5º). Alertar o usuário sobre esse efeito antes de redigir.

**Nota crítica — aditamento obrigatório (art. 303, §1º, I + §2º):**
Concedida a tutela, o autor **deve** aditar a petição no prazo de 15 dias (ou prazo maior fixado pelo juiz). Não aditando, o processo é extinto sem resolução de mérito (art. 303, §2º). Esse prazo é fatal — mencionar expressamente nas notas da peça.

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [Nª VARA CÍVEL]
DA COMARCA DE [CIDADE/UF]

[NOME DO AUTOR], [qualificação completa: nacionalidade, estado civil, profissão,
RG, CPF, endereço], por seu(sua) advogado(a) infra-assinado(a) (procuração —
doc. [X]), vem propor a presente

        AÇÃO COM PEDIDO DE TUTELA ANTECIPADA EM CARÁTER ANTECEDENTE

em face de [NOME DO RÉU], [qualificação completa], com fundamento no art. 303
do Código de Processo Civil:

    [texto literal do art. 303, caput, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

pelos fundamentos a seguir.

I — DA URGÊNCIA CONTEMPORÂNEA AO AJUIZAMENTO

[Descrever de forma objetiva a situação de urgência que torna inviável aguardar
a instrução completa. Dois requisitos a demonstrar:]

I.1 — Da probabilidade do direito

[Indicar, de forma sumária, o direito material que se busca realizar. Referir
documentos que acompanham a inicial como prova de fumaça do bom direito —
doc. [X], doc. [Y].]

I.2 — Do perigo de dano ou do risco ao resultado útil do processo

[Demonstrar concretamente o dano que ocorrerá ou o resultado que será frustrado
se a tutela não for concedida imediatamente. 1-3 parágrafos objetivos.]

II — DO PEDIDO DE TUTELA FINAL

O objeto desta ação é [indicar o pedido de tutela final — o que o autor quer
que o juiz decida ao final]. O presente requerimento limita-se à tutela
antecipada antecedente, nos termos do art. 303, caput, e a petição inicial
será aditada no prazo legal para apresentação plena da argumentação e documentos
(art. 303, §1º, I):

    [texto literal do art. 303, §1º, I, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

III — DOS PEDIDOS

Requer o(a) autor(a):
  a) a concessão inaudita altera parte da tutela antecipada antecedente, para
     determinar [medida específica: ex.: que o réu se abstenha de / entregue /
     pague provisoriamente...], com fundamento no art. 303 c/c art. 300 do CPC;
  b) após a concessão, a citação do(a) réu(é) para, querendo, contestar a ação;
  c) ao final, a confirmação da tutela antecipada e o julgamento de procedência
     do pedido de tutela final para [resultado definitivo pretendido].

⚠️ [VERIFICAR: após a concessão da tutela, alertar o usuário que o aditamento
da petição inicial deve ocorrer em 15 dias (art. 303, §1º, I) — sem aditamento,
o processo será extinto sem resolução de mérito (art. 303, §2º).]

Dá-se à causa o valor de R$ [...] [VERIFICAR: valor deve considerar o pedido
final, nos termos do art. 303, §4º].

Termos em que pede deferimento.
[Cidade], [data].
```

**Nota sobre estabilização — incluir sempre nas NOTAS.md:**

> ⚠️ ATENÇÃO — ESTABILIZAÇÃO DA TUTELA ANTECIPADA (art. 304): Se a tutela for concedida e o réu não interpuser agravo de instrumento, a tutela se estabiliza e o processo é extinto. Isso **não é coisa julgada** — a tutela pode ser revista em ação autônoma, mas o prazo para isso extingue-se em 2 anos (art. 304, §5º). Avaliar com o(a) advogado(a) se o objetivo é obter tutela estabilizada ou prosseguir até sentença de mérito.

---

### 3.1.3 — Tutela cautelar antecedente (CPC arts. 305-310)

> ⚠️ **AÇÃO ANTECEDENTE — NÃO É RECURSO.** A tutela cautelar antecedente instaura processo novo com petição inicial própria. Diferença fundamental em relação à tutela antecipada antecedente (art. 303): **não estabiliza**. Concedida a tutela cautelar, o autor deve formular o **pedido principal em 30 dias** (art. 308), sob pena de cessação da eficácia (art. 309, I). O objetivo da cautelar é **assegurar** o resultado útil do processo principal — não antecipar o bem da vida.

**Intake:**
- Qual é a medida cautelar pretendida (ex.: arresto, sequestro, arrolamento, produção antecipada de provas, outra)?
- Qual é o **direito a ser assegurado** — o processo principal que virá depois?
- Qual é o **perigo de dano** concreto se a cautelar não for concedida agora?
- O usuário tem ciência de que, efetivada a cautelar, terá **30 dias** para formular o pedido principal (art. 308)?
- Há urgência que justifique pedido inaudita altera parte?

**Nota crítica — diferença tutela cautelar × tutela antecipada:**
- **Cautelar (arts. 305-310):** assegura o resultado útil do processo; não entrega o bem da vida de imediato. Exemplo: arresto de bens para garantir futura execução.
- **Antecipada (art. 303):** antecipa, provisoriamente, o próprio bem da vida pedido na ação. Se o juiz entender que o pedido tem natureza antecipada (não cautelar), converte para o art. 303 (art. 305, parágrafo único).

**Nota crítica — cessação de eficácia (art. 309):**
A tutela cautelar cessa em três hipóteses fatais: (i) autor não formula o pedido principal em 30 dias; (ii) a cautelar não é efetivada dentro de 30 dias; (iii) improcedência do pedido principal. Cessar a eficácia é irreversível — a parte **não pode renovar o pedido** com o mesmo fundamento (art. 309, parágrafo único). Alertar o usuário.

**Nota crítica — indeferimento (art. 310):**
O indeferimento da tutela cautelar não impede o ajuizamento do pedido principal, salvo se o motivo do indeferimento for reconhecimento de decadência ou prescrição.

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [Nª VARA CÍVEL]
DA COMARCA DE [CIDADE/UF]

[NOME DO REQUERENTE], [qualificação completa], por seu(sua) advogado(a)
infra-assinado(a) (procuração — doc. [X]), vem propor a presente

        AÇÃO COM PEDIDO DE TUTELA CAUTELAR EM CARÁTER ANTECEDENTE

em face de [NOME DO REQUERIDO], [qualificação completa], com fundamento no
art. 305 do Código de Processo Civil:

    [texto literal do art. 305 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

pelos fundamentos a seguir.

I — DA LIDE E DO DIREITO A SER ASSEGURADO

[Descrever a controvérsia de fundo — o que o requerente pretende obter na ação
principal que será ajuizada. A cautelar serve para assegurar o resultado dessa
ação. 1-2 parágrafos.]

II — DA MEDIDA CAUTELAR PLEITEADA E DO PERIGO DE DANO

[Identificar a medida cautelar concreta pedida — ex.: arresto dos bens
descritos no doc. [X]; exibição de documentos; produção antecipada de prova.]

II.1 — Do perigo de dano ou risco ao resultado útil do processo

[Demonstrar o risco concreto: que os bens serão dissipados / que a prova
desaparecerá / que o resultado da futura ação restará inútil se a cautelar
não for concedida agora. 2-3 parágrafos objetivos.]

II.2 — Da probabilidade do direito

[Indicar o direito material subjacente à lide e os elementos que demonstram
fumaça do bom direito. Referir documentos — doc. [X], doc. [Y].]

III — DA URGÊNCIA E DO PEDIDO INAUDITA ALTERA PARTE

[Se aplicável: demonstrar por que a citação prévia frustaria a eficácia
da medida. Solicitar concessão sem oitiva do requerido.]

IV — DOS PEDIDOS

Requer o(a) requerente:
  a) a concessão [inaudita altera parte] da tutela cautelar antecedente,
     para determinar [medida cautelar específica], com fundamento no art. 305
     c/c art. 300 do CPC;
  b) após efetivada a cautelar, a citação do(a) requerido(a) para contestar
     no prazo de 5 dias (art. 306 do CPC):

    [texto literal do art. 306 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

  c) ao final, a procedência do pedido e a manutenção da medida cautelar até
     o julgamento do pedido principal, que será formulado nos mesmos autos no
     prazo de 30 dias contados da efetivação da cautelar (art. 308 do CPC):

    [texto literal do art. 308, caput, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

⚠️ [VERIFICAR: lembrar o(a) advogado(a) que o pedido principal deve ser
formulado nos mesmos autos em 30 dias após a efetivação da cautelar (art. 308).
O descumprimento implica cessação da eficácia da medida (art. 309, I), que é
irreversível — vedada a renovação com o mesmo fundamento (art. 309, par. único).]

Dá-se à causa o valor de R$ [...].

Termos em que pede deferimento.
[Cidade], [data].
```

---

**Grupo 3.2 — Recursos de fundamentação livre (ordinários)**

### 3.2.1 — Apelação (CPC arts. 1.009-1.014)

**Intake:**
- A sentença foi lida? Pedir o arquivo ou texto.
- Qual é a data da publicação/intimação? (Prazo: 15 dias úteis — art. 1.003, §5º do CPC; verificar via MCP antes de confirmar qualquer data-limite.)
- Qual é a tese de erro da sentença? — error in judicando (juiz errou o direito ou o fato) ou error in procedendo (juiz errou o procedimento)?
- O(a) apelante quer requerer efeito suspensivo (art. 1.012 do CPC)? Em que hipótese?
- Há questões resolvidas interlocutoriamente sem agravo cabível que o apelante quer impugnar em preliminar (art. 1.009, §1º)?

**Nota crítica sobre prazo:** buscar o art. 1.003, §5º do CPC via MCP **antes** de qualquer cálculo de data. O prazo de 15 dias úteis está sujeito a suspensões e recesso (art. 220 do CPC) — os marcos locais do tribunal são `[FORA DO CORPUS]`.

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) DESEMBARGADOR(A) RELATOR(A) DO
[NÚMERO]º TRIBUNAL DE JUSTIÇA DO ESTADO DE [UF]

Processo nº [...]
Apelante: [...]
Apelado(a): [...]

[NOME DO APELANTE], já qualificado(a) nos autos, por seu(sua) advogado(a)
infra-assinado(a), vem, com fundamento nos arts. 1.009 a 1.014 do Código de
Processo Civil, interpor

                              A P E L A Ç Ã O

em face da sentença proferida em [data], pelos fundamentos que passa a expor.

I — DA TEMPESTIVIDADE E DO PREPARO

A sentença foi publicada em [data]. Prazo de 15 dias úteis (art. 1.003, §5º do CPC):

    [texto literal do art. 1.003, §5º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[VERIFICAR: data-limite exata no sistema do tribunal — feriados forenses e
recesso (art. 220 do CPC) são fora do corpus desta skill.]

Preparo: [FORA DO CORPUS — conferir tabela de custas do TJ[UF]].

II — DAS RAZÕES DO APELANTE

II.1 — DA SÍNTESE DA SENTENÇA RECORRIDA

[Resumir o que a sentença decidiu — sem atacar ainda. 1-2 parágrafos factuais.]

II.2 — DAS PRELIMINARES  (art. 1.009, §1º — omitir se não houver)

    [texto literal do art. 1.009, §1º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Questões resolvidas interlocutoriamente sem agravo cabível — trazer aqui.]

II.3 — DO MÉRITO — ERROR IN JUDICANDO   (se erro de direito ou de fato)

Dispõe o art. 1.009, caput, do CPC:

    [texto literal do art. 1.009 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

II.3.1 — [Tese de erro 1 — ex.: Da equivocada aplicação do art. X]

Dispõe o art. [...] do [...]:

    [texto literal via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[Aplicação: como a sentença errou ao aplicar ou não aplicar esse dispositivo
ao caso. Subsunção correta que o(a) apelante propõe. 2-4 parágrafos.]

II.3.2 — [Tese de erro 2] — mesma estrutura.

II.4 — DO MÉRITO — ERROR IN PROCEDENDO   (se erro de procedimento — omitir se não houver)

[O que a sentença omitiu, contrariou ou aplicou mal em termos procedimentais.
Citar o artigo violado via MCP.]

III — DO EFEITO SUSPENSIVO   (se aplicável — art. 1.012 — omitir se não for o caso)

    [texto literal do art. 1.012 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Requerer efeito suspensivo se a hipótese do §1º for aplicável; ou registrar
que a apelação tem efeito suspensivo automático pela regra geral.]

IV — DO PEDIDO

Requer o(a) apelante:
  a) o recebimento e processamento da apelação;
  b) a reforma da sentença para: [pedido específico — o que quer que o tribunal
     decida no lugar da sentença atacada];
  c) a condenação do(a) apelado(a) às custas e honorários recursais (art. 85,
     §11, do CPC):

    [texto literal do art. 85, §11, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

  d) [se efeito suspensivo] a concessão de efeito suspensivo na forma do art. 1.012.

Termos em que pede deferimento.
[Cidade], [data].
```

### 3.2.2 — Agravo de instrumento (CPC arts. 1.015-1.020)

**Intake:**
- Qual é a decisão interlocutória? Pedir o arquivo ou texto.
- Data da publicação/intimação. (Prazo: 15 dias úteis — art. 1.003, §5º + art. 1.016 do CPC; verificar via MCP.)
- A parte quer tutela recursal de urgência no tribunal (art. 1.019, I)?

**Nota crítica — cabimento taxativo:** o rol do art. 1.015 do CPC é taxativo — cabimento fora do rol é erro crasso. Buscar o texto literal do art. 1.015 via MCP e verificar, inciso por inciso, se a decisão se enquadra. Se não houver inciso aplicável, informar ao usuário:

> "Esta decisão não consta no rol taxativo do art. 1.015 do CPC — conferi o texto via MCP. Ela só poderá ser impugnada em preliminar de apelação (art. 1.009, §1º do CPC). Não há agravo de instrumento cabível aqui. Quer que eu estruture a impugnação para a apelação futura?"

Não produza o agravo se o cabimento não estiver verificado.

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) DESEMBARGADOR(A) RELATOR(A) DO
[NÚMERO]º TRIBUNAL DE JUSTIÇA DO ESTADO DE [UF]

Processo nº [...]  (1º grau — [Vara] — [Comarca])
Agravante: [...]
Agravado(a): [...]

[NOME DO AGRAVANTE], por seu(sua) advogado(a), vem interpor

                     AGRAVO DE INSTRUMENTO

em face da decisão interlocutória proferida em [data], com fundamento no
art. 1.015, [inciso], do CPC:

    [texto literal do art. 1.015, [inciso], via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

I — DA TEMPESTIVIDADE

    [texto literal do art. 1.016 + art. 1.003, §5º via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[VERIFICAR: data-limite — feriados forenses são [FORA DO CORPUS].]

II — DA DECISÃO AGRAVADA

[Resumir o que a decisão decidiu e qual o gravame sofrido pelo agravante.]

III — DAS RAZÕES

[Tese de erro da decisão. Dispositivo violado via MCP. 2-4 parágrafos de subsunção.]

IV — DA TUTELA RECURSAL   (art. 1.019, I — omitir se não houver)

    [texto literal do art. 1.019, I, via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Demonstrar probabilidade do direito + perigo de dano, se aplicável.]

V — DO PEDIDO

Requer o(a) agravante:
  a) o processamento do agravo e sua comunicação ao juízo de 1º grau (art. 1.018);
  b) [se tutela recursal] a concessão de tutela recursal liminar;
  c) o provimento do agravo para reformar a decisão.

Nota: em 3 dias, o agravante juntará cópia desta petição nos autos de origem,
nos termos do art. 1.018 do CPC (buscar texto via MCP).

Termos em que pede deferimento.
[Cidade], [data].
```

### 3.2.3 — Embargos de declaração (CPC arts. 1.022-1.026)

**Intake:**
- Qual é a decisão embargada? Pedir o arquivo.
- Qual é o vício: omissão, contradição, obscuridade ou erro material (art. 1.022, I e II)?
- Se omissão: qual argumento ou pedido não foi apreciado?
- Se contradição: onde a decisão contraria a si mesma?
- A parte quer que os embargos tenham efeito infringente (modificar o julgamento) — e em que fundamento?

**Prazo:** 5 dias úteis (art. 1.023 do CPC — buscar via MCP antes de confirmar).

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO [...]
(ou: EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) DESEMBARGADOR(A) RELATOR(A) [...])

Processo nº [...]
Embargante: [...]
Embargado(a): [...]

[NOME DO EMBARGANTE], por seu(sua) advogado(a), vem opor

                   EMBARGOS DE DECLARAÇÃO

à [sentença / decisão interlocutória / acórdão] proferida em [data],
com fundamento no art. 1.022 do CPC:

    [texto literal do art. 1.022 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

I — DA TEMPESTIVIDADE

Prazo de 5 dias úteis (art. 1.023 do CPC):

    [texto literal do art. 1.023 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

II — DA [OMISSÃO / CONTRADIÇÃO / OBSCURIDADE / ERRO MATERIAL]

[Identificação precisa do vício. Transcrever o trecho da decisão que demonstra
o problema. Indicar o argumento/pedido omitido ou o ponto contraditório.]

III — DO PEDIDO

Requer o(a) embargante o acolhimento dos embargos para, nos termos do art. 1.024
do CPC:

    [texto literal do art. 1.024 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[suprir a omissão de [argumento] / sanar a contradição entre [trecho A] e
[trecho B] / esclarecer a obscuridade em [ponto] / corrigir o erro material
de [detalhe].]

[Se efeito infringente] Com a sanação do vício, requer ainda a modificação do
julgamento no ponto correspondente.

Termos em que pede deferimento.
[Cidade], [data].
```

### 3.2.4 — Recurso ordinário trabalhista (CLT art. 895, I)

**Intake:**
- A sentença da Vara do Trabalho foi lida? Pedir o arquivo.
- O(a) recorrente é o empregador ou o empregado?
- Data da publicação/intimação. (Prazo: **8 dias corridos** — CLT art. 895; verificar via MCP. ATENÇÃO: prazo em dias **corridos**, não úteis como no CPC — erro crasso frequente.)
- Se empregador: confirmou o depósito recursal obrigatório? (CLT art. 899 — buscar via MCP; valor-limite vigente é `[FORA DO CORPUS]` — conferir tabela TST.)
- Quais são as teses de erro da sentença?

**Nota crítica — prazo:** buscar o art. 895, I, da CLT via MCP **antes** de qualquer cálculo de prazo. O prazo de 8 dias corridos é regra trabalhista — não confundir com os 15 dias úteis do CPC. Apresentar o texto literal ao usuário.

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) PRESIDENTE DO
TRIBUNAL REGIONAL DO TRABALHO DA [Nª] REGIÃO

Processo nº [...]
Recorrente: [...]
Recorrido(a): [...]

[NOME DO RECORRENTE], por seu(sua) advogado(a), vem interpor

                    RECURSO ORDINÁRIO

em face da sentença proferida em [data] pela [Nª] Vara do Trabalho de [Comarca],
com fundamento no art. 895, I, da CLT:

    [texto literal do art. 895, I, da CLT via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: DL-5452-1943

I — DA TEMPESTIVIDADE

A sentença foi publicada em [data]. Prazo: 8 dias corridos.

[VERIFICAR: data-limite exata — feriados forenses locais e eventuais suspensões
são [FORA DO CORPUS].]

[Se empregador] Depósito recursal recolhido nos termos do art. 899 da CLT:

    [texto literal do art. 899 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: DL-5452-1943

Valor do depósito: [FORA DO CORPUS — conferir tabela vigente do TST].

II — DAS RAZÕES RECURSAIS

II.1 — DA SÍNTESE DA SENTENÇA RECORRIDA

[Resumir as condenações. 1-2 parágrafos factuais.]

II.2 — [TESE DE ERRO 1 — ex.: Da inexistência de vínculo empregatício (CLT art. 3º)]

Dispõe o art. 3º da CLT:

    [texto literal via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: DL-5452-1943

[Aplicação ao caso. Como a sentença errou ao subsumir os fatos ao art. 3º.
2-4 parágrafos de subsunção correta.]

II.3 — [TESE DE ERRO 2] — mesma estrutura.

III — DO PEDIDO

Requer o(a) recorrente:
  a) o conhecimento e provimento do recurso;
  b) a reforma da sentença para: [o que quer que o TRT decida];
  c) [se empregador] a improcedência total dos pedidos / redução da condenação.

Termos em que pede deferimento.
[Cidade], [data].
```

### 3.2.5 — Recurso inominado — JEC (Lei 9.099, art. 41)

**Intake:**
- Sentença do JEC lida? Pedir arquivo.
- Data da publicação/intimação. (Prazo: 10 dias — verificar via MCP o art. 42 da Lei 9.099.)
- O recurso vai para a Turma Recursal — não para o TJ. Confirmar com o usuário.
- Há preparo obrigatório? (Verificar via MCP art. 42, §1º da Lei 9.099.)

**Nota crítica:** no JEC não se aplica o CPC de forma plena — verificar via MCP o que a Lei 9.099 diz expressamente. Não aplicar artigos do CPC sem confirmar a incidência subsidiária. Se o corpus do MCP não cobrir a Lei 9.099, marcar `[FORA DO CORPUS]` e informar ao usuário.

### 3.2.6 — Recurso Ordinário Constitucional (CF arts. 102, II, e 105, II + CPC arts. 1.027-1.028)

> ⚠️ **DOIS PORTÕES DE CABIMENTO — VERIFICAR ANTES DE REDIGIR.**
>
> **Portão 1 — a decisão tem de ser DENEGATÓRIA.** O ROC só cabe de decisão que **negou** o habeas corpus, o mandado de segurança, o habeas data ou o mandado de injunção. Se a ordem/segurança foi **concedida** e quem quer recorrer é a parte sucumbente (autoridade coatora, pessoa jurídica de direito público), **não cabe ROC** — cabe Recurso Extraordinário e/ou Recurso Especial (módulos 3.3.1/3.3.2). Confirmar isso primeiro.
>
> **Portão 2 — competência originária do tribunal.** O MS/HC tem de ter sido julgado **em única instância** (competência originária do tribunal), não em grau de recurso. MS impetrado originariamente no TJ/TRF contra ato de autoridade → cabe ROC da denegação. MS que subiu por apelação → não é ROC; a via é RE/REsp.

**Mapa de destino:**

| Decisão denegatória de... | Proferida por... | ROC vai para... | Base |
|---|---|---|---|
| HC, MS, HD ou MI | Tribunal Superior (STJ, TST, TSE, STM), em única instância | STF | CF art. 102, II, "a" + CPC art. 1.027, I |
| HC | TRF ou TJ, em única ou última instância | STJ | CF art. 105, II, "a" |
| MS | TRF ou TJ, em única instância | STJ | CF art. 105, II, "b" + CPC art. 1.027, II, "a" |

**Intake:**
- Qual é a decisão recorrida — acórdão que denegou HC, MS, HD ou MI? Pedir o arquivo completo.
- A decisão é **denegatória** (negou a ordem)? Confirmar expressamente. Se concessiva → não é ROC (ver portão 1).
- O writ foi julgado em **competência originária** do tribunal (única instância) ou em grau de recurso? (Portão 2.)
- Qual a data da publicação/intimação do acórdão? (Prazo: ver nota crítica abaixo — varia entre MS e HC.)
- Qual parte o usuário representa — impetrante/paciente vencido?

**Nota crítica — natureza do ROC (não confundir com RE/REsp):**
O ROC é **recurso ordinário** — devolve ao tribunal superior a matéria de **fato e de direito** em ampla devolutividade, como uma apelação (art. 1.028 do CPC manda aplicar o procedimento da apelação). Por isso, **o ROC NÃO exige prequestionamento, NÃO exige repercussão geral e NÃO exige demonstração de relevância.** Não estruturar o ROC como RE/REsp: não há seção de prequestionamento nem de repercussão geral. O recorrente pode rediscutir livremente os fatos, as provas e a aplicação do direito que levaram à denegação.

**Nota crítica — prazo (regra geral 15 dias; uma exceção de 5 dias):**
- **Regra geral — 15 dias úteis (art. 1.003, §5º, do CPC):** aplica-se à esmagadora maioria dos ROC — mandado de segurança, habeas data, mandado de injunção e também o **habeas corpus julgado por Tribunal Superior rumo ao STF** (CF art. 102, II, "a"). Buscar via MCP.
- **Exceção — 5 dias (Lei 8.038/1990, art. 30):** **apenas** o ROC em **habeas corpus decidido por TRF ou TJ rumo ao STJ** (CF art. 105, II, "a"). Dispositivo não revogado pelo CPC/2015. `[VERIFICAR: Lei 8.038/1990 provavelmente está fora do corpus do MCP — confirmar o prazo de 5 dias e o texto do art. 30 antes do protocolo.]`
- Confundir os dois prazos é erro grave. Identificar primeiro a alínea de cabimento (102 II "a" → 15 dias; 105 II "a" em HC → 5 dias); na dúvida sobre HC, adotar o menor (5 dias) e confirmar.

**Nota crítica — endereçamento:**
O ROC é interposto **perante o presidente do tribunal que proferiu a decisão recorrida** (tribunal a quo), mas **dirigido ao STF ou ao STJ** conforme o mapa acima. O cabeçalho endereça ao presidente do tribunal de origem; a peça identifica o tribunal superior competente para o julgamento.

**Nota crítica — jurisprudência:**
Aplicar a regra das peças ordinárias (Fonte 2): jurisprudência é **vedada** no corpo do ROC. Tese que dependa de precedente → `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`. O ROC se ganha demonstrando o erro da denegação à luz da lei e dos fatos — não citando julgados.

**Estrutura da peça:**

```
AO EXCELENTÍSSIMO SENHOR PRESIDENTE DO [TRIBUNAL DE ORIGEM —
TRIBUNAL SUPERIOR / TRF / TJ]
(Recurso ordinário a ser julgado pelo [SUPREMO TRIBUNAL FEDERAL /
SUPERIOR TRIBUNAL DE JUSTIÇA])

Processo nº [...]
Recorrente: [...]  (impetrante/paciente)
Recorrido(a): [autoridade coatora / pessoa jurídica de direito público]

[NOME DO RECORRENTE], já qualificado(a) nos autos, por seu(sua) advogado(a),
vem, com fundamento no art. [102, II, "a" / 105, II, "a"/"b"] da Constituição
Federal e nos arts. 1.027 e 1.028 do Código de Processo Civil, interpor

              RECURSO ORDINÁRIO [CONSTITUCIONAL]

em face do acórdão proferido em [data] pela [Turma/Seção/Órgão Especial] do
[Tribunal], que DENEGOU [a segurança / a ordem de habeas corpus / ...], nos
termos a seguir.

I — DA TEMPESTIVIDADE

[Regra geral — MS/HD/MI e HC ao STF (CF art. 102, II, "a"):] O acórdão foi
publicado em [data]. Prazo de 15 dias úteis (art. 1.003, §5º, do CPC):

    [texto literal do art. 1.003, §5º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Exceção — HC ao STJ (CF art. 105, II, "a"):] O acórdão foi publicado em [data].
Prazo de 5 dias (Lei 8.038/1990, art. 30).
[VERIFICAR: Lei 8.038/1990 provavelmente está fora do corpus — confirmar prazo de
5 dias e texto do art. 30. Esta exceção vale SÓ para HC rumo ao STJ; nas demais
hipóteses de ROC o prazo é de 15 dias úteis do CPC.]

[VERIFICAR: data-limite exata no sistema do tribunal — feriados forenses e
suspensões locais são [FORA DO CORPUS].]

II — DO CABIMENTO

O presente recurso é cabível com fundamento no art. [102, II, "a" / 105, II,
"a"/"b"] da Constituição Federal, pois o acórdão recorrido DENEGOU [o writ],
decidido em única instância pelo [Tribunal]:

    [texto literal do art. 102, II ou 105, II via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: CF-1988

    [texto literal do art. 1.027 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

São preenchidos os dois requisitos de cabimento: (i) a decisão é DENEGATÓRIA, e
(ii) foi proferida em competência originária ([única instância]) do [Tribunal].

III — DA DECISÃO RECORRIDA

[Resumir o que o acórdão decidiu e por que denegou o writ — 2-3 parágrafos
factuais. Citar literalmente o trecho da denegação, como Fonte 3 (autos):]

    [Citação literal do dispositivo do acórdão que denegou a ordem]
    Fonte: Acórdão ID [ID] — [data] — autos nº [número do processo]

IV — DAS RAZÕES DO RECURSO

[Como o ROC tem ampla devolutividade, atacar livremente fato e direito:]

IV.1 — [Tese 1 — ex.: Do direito líquido e certo violado / Da ilegalidade do
ato coator]

    [texto literal do dispositivo legal violado via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[Subsunção: por que o ato impugnado é ilegal/abusivo e por que a denegação
errou. Revolver os fatos e as provas dos autos livremente. 2-4 parágrafos.]

IV.2 — [Tese 2] — mesma estrutura.

[Se a tese depender de precedente:]
[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]

V — DO PEDIDO

Requer o(a) Recorrente:
  a) o recebimento e processamento do presente Recurso Ordinário, com a remessa
     dos autos ao [STF / STJ];
  b) o provimento do recurso para reformar o acórdão recorrido e CONCEDER
     [a segurança / a ordem de habeas corpus], determinando [a providência
     pleiteada no writ];
  c) [se MS] a condenação da autoridade/pessoa jurídica recorrida nos ônus de
     sucumbência cabíveis.

Termos em que pede deferimento.
[Cidade], [data].
```

### 3.2.7 — Agravo Interno (CPC art. 1.021) — duas hipóteses

> ⚠️ **ATENÇÃO — identificar a hipótese antes de redigir.** O Agravo Interno do art. 1.021 cobre duas situações distintas com fundamentos diferentes:
>
> **Hipótese 1 — Contra decisão monocrática do Relator (qualquer tribunal):**
> Qualquer decisão monocrática de relator — seja em TRF/TJ, seja no STJ/STF — pode ser submetida ao colegiado via Agravo Interno (art. 1.021). É o uso mais frequente.
>
> **Hipótese 2 — Contra decisão do Presidente/VP do tribunal de origem que negou seguimento por conformidade com repetitivos/RG:**
> Quando o Presidente/VP do TRF ou TJ inadmite o RE/REsp com fundamento no art. 1.030, I (conformidade com repetitivos/RG) ou art. 1.030, III (sobrestamento), o recurso cabível é Agravo Interno ao **próprio tribunal de origem** (art. 1.030, §2º), NÃO Agravo ao STJ/STF.

**Intake:**
- A decisão impugnada é de (a) relator/a ou (b) Presidente/VP?
- Se relator/a: em que tribunal? Qual o teor da decisão monocrática?
- Se Presidente/VP: qual o fundamento exato da inadmissão? (art. 1.030, I ou III?)
- Qual é a data da publicação/intimação? (Prazo: 15 dias úteis — art. 1.021, §2º CPC.)

**Nota crítica — prazo:** Verificar art. 1.021, §2º via MCP. Prazo de 15 dias úteis, contados da intimação da decisão monocrática ou da decisão do Presidente/VP.

**Nota crítica — vedação à inovação:** O Agravo Interno não pode inovar nas razões recursais (art. 1.021, §1º CPC). O agravante reproduz e reforça os argumentos do recurso principal — não apresenta tese nova.

**Nota crítica — multa por protelatório:** Se o Agravo Interno for unânime e manifestamente inadmissível ou improcedente, o tribunal aplica multa de 1% a 5% do valor da causa (art. 1.021, §4º CPC). Avaliar com o(a) advogado(a) se há tese séria antes de interpor.

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DESEMBARGADOR(A)/MINISTRO(A) RELATOR(A)
[ou: EGRÉGIA [N]ª TURMA / CÂMARA do [TRIBUNAL]]

Processo nº [...]
Agravante: [...]
Agravado(a): [...]

[NOME DO AGRAVANTE] vem interpor, com fundamento no art. 1.021 do Código de
Processo Civil, o presente

              AGRAVO INTERNO

em face da decisão monocrática [/ decisão do Presidente/Vice-Presidente]
proferida em [data], nos termos a seguir.

I — DA TEMPESTIVIDADE

    [texto literal do art. 1.021, §2º via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[VERIFICAR: data-limite — 15 dias úteis a partir de [data+1].]

II — DO CABIMENTO

[Hipótese 1 — decisão monocrática do relator:]
A decisão agravada é monocrática, proferida pelo(a) Exmo(a). Sr(a).
[Relator(a)] em [data]. O art. 1.021, caput, do CPC admite o Agravo Interno
para submeter ao colegiado qualquer decisão monocrática do relator:

    [texto literal do art. 1.021, caput, via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Hipótese 2 — decisão do Presidente/VP por conformidade com repetitivos:]
A decisão agravada foi proferida pelo(a) Presidente/Vice-Presidente do [Tribunal]
com fundamento no art. 1.030, inciso [I/III], do CPC, inadmitindo o Recurso
[Extraordinário/Especial] por [conformidade com entendimento de repetitivos /
sobrestamento indevido]. O art. 1.030, §2º, do CPC prevê que desta decisão
cabe Agravo Interno:

    [texto literal do art. 1.030, §2º via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

    [texto literal do art. 1.021, caput, via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

III — DA DECISÃO AGRAVADA

    [Citação literal do trecho relevante da decisão monocrática ou do Presidente/VP]
    Fonte: Decisão monocrática [ou "Decisão de inadmissão do Presidente/VP"] — [data/ID] — autos nº [número]

IV — DAS RAZÕES

[Reproduzir e reforçar os argumentos do recurso ou petição que gerou a decisão.
NÃO inovar nas teses — o Agravo Interno submete ao colegiado o que já foi
apresentado ao relator, apontando o erro da decisão singular. 2-4 parágrafos.]

V — DO PEDIDO

Requer o(a) Agravante que o Colegiado:
  a) conheça e dê provimento ao presente Agravo Interno;
  b) [Hipótese 1] reforme a decisão monocrática para [o que quer];
  b) [Hipótese 2] reforme a decisão do Presidente/VP e admita o Recurso
     [Extraordinário / Especial] para processamento no [STJ/STF].

Termos em que pede deferimento.
[Cidade], [data].
```

---

**Grupo 3.3 — Recursos excepcionais (fundamentação vinculada)**

### 3.3.1 — Recurso Extraordinário (CF art. 102, III, "a" + CPC arts. 1.029-1.035)

> ⚠️ **VERIFICAR INTERPOSIÇÃO SIMULTÂNEA COM REsp (CPC art. 1.031).**
> Antes de redigir o RE, perguntar ao usuário: **"O acórdão recorrido apresenta fundamentos de direito federal infraconstitucional além da questão constitucional? Há violação a lei federal além da Constituição?"**
> - Se **sim** → preparar RE **e** REsp simultaneamente, em petições separadas, ao mesmo Presidente/VP do tribunal de origem. A não interposição do REsp implica preclusão definitiva das matérias de direito federal infraconstitucional. Seguir também o módulo 3.3.2.
> - Se **não** → prosseguir só com o RE.
> Buscar o art. 1.031 do CPC via MCP para citar na peça quando houver interposição simultânea.

**Intake:**
- O acórdão recorrido foi lido? Pedir o arquivo completo do processo ou, no mínimo, o acórdão e os embargos de declaração.
- Qual é a data da publicação/intimação do acórdão dos embargos de declaração (última decisão)? (Prazo: 15 dias úteis — art. 1.003, §5º do CPC; verificar via MCP antes de confirmar qualquer data-limite.)
- Quais dispositivos constitucionais foram violados, na visão do recorrente?
- Os dispositivos constitucionais foram prequestionados? Em que fase (apelação? embargos?)

**Nota crítica — prequestionamento obrigatório:**
O RE só é admitido se a matéria constitucional tiver sido suscitada e debatida nas instâncias ordinárias. **Tudo que foi prequestionado nos embargos de declaração deve ser incluído no RE.** Antes de redigir, mapear todos os dispositivos invocados nos embargos e garantir que cada um apareça nas razões do RE, associado à tese de violação correspondente. Se os embargos forem de declaração com finalidade de prequestionamento (art. 1.025 do CPC), mencionar isso expressamente na seção de prequestionamento.

**Nota crítica — Tema de Repercussão Geral:**
Se o STF já reconheceu repercussão geral sobre a mesma matéria (RE repetitivo), verificar:
- O Tema está pendente de julgamento? → Requerer sobrestamento (art. 1.037, II, CPC).
- O Tema já foi julgado? → Requerer aplicação do entendimento firmado (art. 1.030 CPC) — adaptar o pedido conforme o resultado (favorável ou desfavorável ao recorrente).
- Marcar com `[VERIFICAR: status do Tema [N] antes do protocolo]`.

**Nota crítica — jurisprudência no RE:**
Ao contrário das peças ordinárias, no RE a invocação de precedentes do STF é estruturalmente necessária. Aplicar a regra da Fonte 2 (Jurisprudência) da seção "Regra absoluta": citar o precedente com busca web quando possível e marcar sempre com `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]`.

**Nota crítica — citação literal do acórdão recorrido:**
Na seção "Do acórdão recorrido", citar **textualmente** — como citação recuada, usando a Fonte 3 (autos) — os trechos do acórdão que demonstram: (a) que a matéria constitucional foi enfrentada (ou que houve omissão no enfrentamento), e (b) que o tribunal reconheceu a existência do Tema de Repercussão Geral correspondente, se for o caso. Essa citação literal é argumento de cabimento — não é jurisprudência — e não leva o marcador de jurisprudência.

**Estrutura da peça:**

```
AO EXCELENTÍSSIMO SENHOR PRESIDENTE DO [TRIBUNAL DE ORIGEM]

Processo nº [...]
Recorrente: [...]
Recorrido(a): [...]

[NOME DO RECORRENTE], já qualificado(a) nos autos, por seu(sua) advogado(a),
vem, com fundamento no art. 102, inciso III, alínea "a", da Constituição Federal,
e nos arts. 1.029 a 1.035 do Código de Processo Civil, interpor

              RECURSO EXTRAORDINÁRIO

em face do acórdão proferido em [data] pela [Turma/Câmara] do [Tribunal],
nos termos a seguir.

I — DA TEMPESTIVIDADE

O acórdão [ou "o acórdão que rejeitou os embargos de declaração"] foi publicado
em [data]. Prazo de 15 dias úteis (art. 1.003, §5º do CPC):

    [texto literal do art. 1.003, §5º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[VERIFICAR: data-limite exata — contar 15 dias úteis a partir de [data+1], descontando
feriados forenses nacionais e locais. Confirmar no sistema do tribunal antes do protocolo.]

Preparo: [FORA DO CORPUS — conferir tabela de custas do tribunal de origem e
do STF para fins de GRU. Recolher antes do protocolo.]

[Se interposto simultaneamente com REsp — incluir este parágrafo:]
O presente Recurso Extraordinário é interposto simultaneamente com o Recurso Especial
nº [deixar em branco — mesma petição/data], nos termos do art. 1.031 do Código de
Processo Civil:

    [texto literal do art. 1.031 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

O Recurso Especial será processado primeiro pelo Superior Tribunal de Justiça;
somente após a decisão do STJ — ou após a remessa por inadmissibilidade — os
autos serão enviados ao Supremo Tribunal Federal para exame do presente Recurso
Extraordinário.

II — DO CABIMENTO

O presente Recurso Extraordinário é cabível com fundamento no art. 102, inciso III,
alínea "a", da Constituição Federal, pois o acórdão recorrido contraria diretamente
os seguintes dispositivos constitucionais:

    [texto literal de cada dispositivo constitucional via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: CF-1988

Os requisitos do art. 1.029 do CPC estão presentes:

    [texto literal do art. 1.029 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

III — DO PREQUESTIONAMENTO

[Indicar as fases em que cada dispositivo constitucional foi suscitado — petição inicial,
apelação, embargos de declaração. Mencionar expressamente o art. 1.025 do CPC se
os embargos tiveram finalidade de prequestionamento.]

Os dispositivos constitucionais objeto deste recurso foram prequestionados nas
seguintes peças processuais:
  - [art. X da CF] → suscitado em [petição inicial / apelação / embargos de declaração de [data]]
  - [art. Y da CF] → suscitado em [...]

[VERIFICAR: conferir se cada dispositivo invocado neste RE consta de pelo menos
uma das peças processuais anteriores assinadas pela parte. Se algum dispositivo
não foi prequestionado, avaliar com o(a) advogado(a) o risco de inadmissão.]

IV — DO ACÓRDÃO RECORRIDO

O acórdão recorrido [identificar: número, relator, data do julgamento]:

[Resumir o que o tribunal decidiu — 2-3 parágrafos factuais, sem atacar ainda.]

O próprio acórdão registrou expressamente:

    [Citação literal do trecho do acórdão relevante ao cabimento — ex.: reconhecimento
     do Tema de Repercussão Geral, ou do caráter constitucional da controvérsia]
    Fonte: Acórdão ID [ID] — [data] — autos nº [número do processo]

[Se o acórdão reconheceu que a matéria é objeto de Tema de Repercussão Geral, citar
esse trecho aqui — isso reforça o cabimento e o pedido de sobrestamento.]

V — DA REPERCUSSÃO GERAL

[Se o STF já reconheceu repercussão geral sobre a matéria:]

A matéria constitucional debatida nestes autos é objeto do RE [número]/[UF]
(Tema [N] da Repercussão Geral do STF), ao qual foi reconhecida a repercussão geral,
nos termos do art. 1.035, §1º, do CPC:

    [texto literal do art. 1.035 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[VERIFICAR: confirmar o status atual do Tema [N] antes do protocolo — se pendente,
manter pedido de sobrestamento; se julgado, adaptar pedido para aplicação do resultado.]

[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]:
Reconhecimento da repercussão geral no RE [número]/[UF] (Tema [N]).

[Se não houver Tema de Repercussão Geral reconhecido, demonstrar a repercussão geral
nos termos do art. 1.035, §§1º e 2º, com argumentos de relevância econômica, política,
social ou jurídica que ultrapassem os interesses das partes.]

VI — DAS RAZÕES DO RECURSO

VI.[A] — VIOLAÇÃO AO [ART. X, INCISO Y, DA CF] — [NOME DA GARANTIA/PRINCÍPIO]

[Citar o dispositivo constitucional via MCP.]

    [texto literal do dispositivo constitucional via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: CF-1988

[Explicar o que o dispositivo garante e como o acórdão recorrido o violou.
2-4 parágrafos de subsunção: (i) o que a CF diz, (ii) o que o tribunal decidiu,
(iii) por que há incompatibilidade entre ambos.]

[Se houver precedente do STF relevante:]
[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]:
[Argumento com base no precedente — ex.: "No julgamento do RE [número] (Tema [N]),
o STF firmou que [tese]. A mesma ratio se aplica ao caso presente porque [...]"]
Fonte: pesquisa web — [URL se disponível, ou "não localizado — verificar manualmente"]

[Repetir a estrutura para cada dispositivo constitucional prequestionado.]

VII — DO PEDIDO DE SOBRESTAMENTO  (omitir se o Tema já foi julgado)

Requer a Recorrente o sobrestamento do presente recurso até o julgamento definitivo do
RE [número]/[UF] (Tema [N] da Repercussão Geral), nos termos do art. 1.037, II, do CPC:

    [texto literal do art. 1.037, II via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

VIII — DO PEDIDO

Requer a Recorrente:
  a) o recebimento e processamento do presente Recurso Extraordinário;
  b) [se Tema pendente] o sobrestamento do feito até o julgamento do Tema [N];
  c) [se Tema já julgado — favorável] a aplicação do entendimento firmado no Tema [N],
     com a reforma do acórdão recorrido para [o que quer que o STF decida];
  d) [se Tema não há ou complementarmente] o provimento do RE para reformar o
     acórdão recorrido e declarar [o direito pleiteado];
  e) [se aplicável] a condenação da Recorrida ao ressarcimento das custas judiciais
     (art. 82, §2º, do CPC).

Termos em que pede deferimento.
[Cidade], [data].
```

### 3.3.2 — Recurso Especial (CF art. 105, III + CPC arts. 1.029-1.032)

> ⚠️ **VERIFICAR INTERPOSIÇÃO SIMULTÂNEA COM RE (CPC art. 1.031).**
> Antes de redigir o REsp, perguntar ao usuário: **"O acórdão recorrido também viola a Constituição Federal — não apenas a lei federal infraconstitucional?"**
> - Se **sim** → preparar REsp **e** RE simultaneamente, em petições separadas, ao mesmo Presidente/VP do tribunal de origem. A não interposição do RE implica preclusão definitiva das matérias constitucionais. Seguir também o módulo 3.3.1.
> - Se **não** → prosseguir só com o REsp.
> Quando houver interposição simultânea, incluir na peça a menção ao art. 1.031 do CPC e informar que o REsp será processado primeiro no STJ; só após é que o RE segue ao STF.

**Intake:**
- O acórdão recorrido foi lido? Pedir arquivo do acórdão e dos embargos de declaração (se já opostos para prequestionamento).
- Qual é a data da publicação/intimação do último acórdão? (Prazo: 15 dias úteis — art. 1.003, §5º CPC.)
- Qual o fundamento do cabimento? — (a) contrariou lei federal ou negou-lhe vigência (art. 105, III, "a" CF); (b) julgou válido ato contestado em face de lei federal (art. 105, III, "b" CF); (c) deu à lei federal interpretação divergente da adotada por outro tribunal (art. 105, III, "c" CF — dissídio jurisprudencial)?
- Os dispositivos legais federais foram prequestionados nos autos?

**Nota crítica — cabimento:** O REsp exige violação a **lei federal infraconstitucional**. Questão puramente constitucional → RE (STF), não REsp. Verificar se a questão é legal ou constitucional antes de redigir. Se for constitucional, diagnosticar RE; se for legal, diagnosticar REsp.

**Nota crítica — prequestionamento:** Mesma regra do RE. Tudo que foi suscitado nos embargos de declaração (art. 1.025 CPC) deve aparecer no REsp. Listar os dispositivos de lei federal violados e confirmar que cada um foi prequestionado.

**Nota crítica — dissídio (alínea "c"):** Se o fundamento for divergência jurisprudencial, o recorrente deve demonstrar o dissídio com certidão, cópia ou URL do acórdão paradigma (art. 1.029, §1º, CPC). Usar fonte dos autos e/ou pesquisa web, com marcador `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP]` para o acórdão paradigma.

**Nota crítica — recursos repetitivos (Temas STJ):** Verificar se a matéria é objeto de Tema repetitivo no STJ. Se já julgado e desfavorável, avaliar a admissibilidade. Se pendente, requerer sobrestamento.

**Estrutura da peça:**

```
AO EXCELENTÍSSIMO SENHOR PRESIDENTE DO [TRIBUNAL DE ORIGEM — TRF ou TJ]

Processo nº [...]
Recorrente: [...]
Recorrido(a): [...]

[NOME DO RECORRENTE], já qualificado(a), vem interpor

              RECURSO ESPECIAL

com fundamento no art. 105, inciso III, alínea(s) "[a/b/c]", da Constituição Federal,
e nos arts. 1.029 a 1.032 do Código de Processo Civil.

I — DA TEMPESTIVIDADE

    [texto literal do art. 1.003, §5º via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[VERIFICAR: data-limite — 15 dias úteis a partir de [data+1], desconto de feriados.]
Preparo: [FORA DO CORPUS — conferir tabela do STJ e do tribunal de origem.]

[Se interposto simultaneamente com RE — incluir este parágrafo:]
O presente Recurso Especial é interposto simultaneamente com o Recurso Extraordinário
nº [deixar em branco — mesma petição/data], nos termos do art. 1.031 do Código de
Processo Civil:

    [texto literal do art. 1.031 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

O Superior Tribunal de Justiça examinará o presente Recurso Especial em primeiro
lugar; somente após o julgamento — ou remessa por inadmissibilidade — os autos
seguirão ao Supremo Tribunal Federal para exame do Recurso Extraordinário.

II — DO CABIMENTO

O presente Recurso Especial é cabível com fundamento no art. 105, inciso III,
alínea(s) "[a/b/c]", da Constituição Federal, pois o acórdão recorrido:

  [alínea "a"] contrariou / negou vigência ao(s) art(s). [X] da [lei federal],
  [alínea "b"] julgou válido ato contestado em face do art. [X] da [lei federal],
  [alínea "c"] deu ao art. [X] da [lei federal] interpretação divergente da adotada
               pelo [tribunal paradigma] no julgamento de [identificar acórdão]:
               [JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]
               Fonte: pesquisa web — [URL ou "não localizado — verificar manualmente"]

III — DO PREQUESTIONAMENTO

[Indicar em que peça cada dispositivo legal federal foi suscitado. Art. 1.025 CPC
para itens suscitados nos embargos de declaração.]

[VERIFICAR: confirmar que cada art. invocado neste REsp consta de peça anterior.]

IV — DOS TEMAS REPETITIVOS (se houver)

[VERIFICAR: pesquisar se a matéria é objeto de Tema repetitivo no STJ.
Se pendente, requerer sobrestamento (art. 1.037, II, CPC).
Se julgado, adaptar pedido conforme o resultado.]

V — DO ACÓRDÃO RECORRIDO

    [Citação literal do trecho relevante do acórdão — o que o tribunal decidiu
     e por que está errado em relação à lei federal]
    Fonte: Acórdão — [data/ID] — autos nº [número]

VI — DAS RAZÕES

VI.[A] — VIOLAÇÃO AO ART. [X] DA [LEI FEDERAL]

    [texto literal do dispositivo legal via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[Explicar o que a norma determina e como o acórdão a contrariou.
2-4 parágrafos de subsunção: (i) o que a lei diz, (ii) o que o tribunal decidiu,
(iii) por que há incompatibilidade. Sem jurisprudência ou com marcador se necessário.]

VII — DO PEDIDO

Requer o(a) Recorrente:
  a) o recebimento e processamento do Recurso Especial;
  b) [se Tema repetitivo pendente] o sobrestamento até julgamento do Tema [N];
  c) [se Tema já julgado favorável] a aplicação do entendimento do STJ;
  d) o provimento do REsp para reformar o acórdão recorrido e [o que quer];
  e) a condenação da parte contrária em custas e honorários recursais
     (art. 85, §11, CPC):

    [texto literal do art. 85, §11, via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

Termos em que pede deferimento.
[Cidade], [data].
```

### 3.3.3 — Agravo em RE / Agravo em REsp (CPC art. 1.042) — ao tribunal superior

> ⚠️ **ATENÇÃO — cabimento restrito.** O Agravo do art. 1.042 só cabe quando o Presidente/VP do tribunal de origem **inadmitiu** o RE ou REsp com fundamento no **juízo geral de admissibilidade** (art. 1.030, V, CPC). Se a inadmissão foi com base em **conformidade com entendimento de casos repetitivos ou RG** (art. 1.030, I ou III), o recurso cabível é o **Agravo Interno** ao próprio tribunal de origem (art. 1.021 + art. 1.030, §2º) — não o Agravo ao tribunal superior. Diagnosticar isso antes de redigir.

**Intake:**
- Qual foi o fundamento da decisão do Presidente/VP que inadmitiu o RE/REsp?
  - "Inadmitiu por razão geral" (art. 1.030, V) → ARE/AREsp ao tribunal superior
  - "Inadmitiu por conformidade com repetitivos/RG" (art. 1.030, I) → Agravo Interno ao tribunal de origem (ver 3.2.7)
  - "Sobrestou indevidamente" (art. 1.030, III) → Agravo Interno ao tribunal de origem (ver 3.2.7)
- Qual é a data da publicação/intimação da decisão? (Prazo: 15 dias úteis — art. 1.003, §5º CPC.)
- O ARE vai ao STF ou o AREsp vai ao STJ?

**Nota crítica:** Verificar o texto literal da decisão inadmissória antes de qualquer coisa. O fundamento da decisão determina o recurso cabível. Pedir o documento ao usuário se não estiver nos autos enviados.

**Estrutura da peça:**

```
AO EXCELENTÍSSIMO SENHOR MINISTRO PRESIDENTE DO
[SUPREMO TRIBUNAL FEDERAL / SUPERIOR TRIBUNAL DE JUSTIÇA]

Processo nº [...]
Agravante: [...]
Agravado(a): [...]

[NOME DO AGRAVANTE] vem interpor, com fundamento no art. 1.042 do Código de
Processo Civil, o presente

              AGRAVO EM RECURSO [EXTRAORDINÁRIO / ESPECIAL]

em face da decisão do Presidente/Vice-Presidente do [Tribunal de Origem] que
inadmitiu o Recurso [Extraordinário / Especial] interposto nestes autos.

I — DA TEMPESTIVIDADE

    [texto literal do art. 1.003, §5º via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[VERIFICAR: data-limite — 15 dias úteis a partir de [data+1].]

II — DO CABIMENTO — FUNDAMENTO DA DECISÃO AGRAVADA

A decisão agravada inadmitiu o Recurso [Extraordinário / Especial] com fundamento
no art. 1.030, inciso V, do Código de Processo Civil:

    [texto literal do art. 1.042 via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

    [texto literal do art. 1.030, V via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

III — DO ACÓRDÃO INADMISSOR

A decisão agravada tem o seguinte teor:

    [Citação literal da decisão do Presidente/VP que inadmitiu o recurso]
    Fonte: Decisão de inadmissão — [data/ID] — autos nº [número]

[Identificar o fundamento concreto da inadmissão e demonstrar que está errado.]

IV — DAS RAZÕES

[Demonstrar que o RE/REsp preenchia os requisitos de admissibilidade que o
Presidente/VP reputou ausentes. Remeter às razões do recurso inadmitido
ou reproduzir os argumentos de cabimento.]

V — DO PEDIDO

Requer o(a) Agravante:
  a) o provimento do presente Agravo para que o Recurso [Extraordinário / Especial]
     seja admitido e processado no [STF / STJ];
  b) subsidiariamente, que o [STF / STJ] julgue diretamente o mérito do
     Recurso [Extraordinário / Especial], nos termos do art. 1.042, §5º, do CPC.

Termos em que pede deferimento.
[Cidade], [data].
```

---

### 3.3.4 — Embargos de divergência (CPC arts. 1.043-1.044)

> ⚠️ **RECURSO INTERNO AO STJ OU AO STF — NÃO É RECURSO PARA OUTRO TRIBUNAL.** Os embargos de divergência são recurso interposto perante o próprio STJ ou STF para submeter ao órgão pleno ou à seção competente acórdão de turma que diverge de outro acórdão do mesmo tribunal. Destina-se à uniformização interna da jurisprudência do tribunal superior. O paradigma (acórdão divergente) é elemento de cabimento e deve ser identificado com precisão — por isso os dados do acórdão paradigma levam marcador `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP]`.

**Intake:**
- O acórdão embargado foi proferido em (a) RE/REsp/recurso ordinário ou (b) processo de competência originária do tribunal?
- Qual é o **acórdão paradigma** — outro acórdão do mesmo tribunal que diverge da tese adotada no acórdão embargado? Identificar: órgão julgador, número do processo, data, tese.
- A divergência é de **mérito** (ambos os acórdãos decidiram o mérito), de **admissibilidade** (ambos decidiram sobre admissibilidade), ou mista (um de mérito e outro que não conheceu mas apreciou a controvérsia — art. 1.043, III)?
- A divergência versa sobre direito **material** ou **processual** (ambos cabem — art. 1.043, §2º)?
- Qual é a data de publicação do acórdão embargado? (Prazo — ver nota crítica abaixo.)

**Nota crítica — cabimento (art. 1.043):**
Quatro hipóteses:

| Inciso | Hipótese | Detalhe |
|---|---|---|
| I | RE ou REsp: embargado e paradigma **ambos de mérito**, turmas divergentes | Hipótese mais frequente |
| II | RE ou REsp: embargado e paradigma **ambos de admissibilidade** | Ex.: uma turma admite recurso, outra não, pela mesma questão |
| III | RE ou REsp: um de mérito, outro que **não conheceu mas apreciou a controvérsia** | Hipótese mais restrita |
| IV | **Processos de competência originária**: turma diverge de outra turma ou seção | Ex.: divergência em habeas corpus originário |

**Nota crítica — prazo:**
O CPC não fixa prazo próprio para os embargos de divergência — remete ao regimento interno do respectivo tribunal (art. 1.044). No STJ (RISTJ art. 267) e no STF (RISTF art. 330), o prazo é de **15 dias** contados da publicação do acórdão embargado. `[VERIFICAR: confirmar o prazo atual no RISTJ/RISTF — regimento interno é [FORA DO CORPUS] desta skill.]`

**Nota crítica — interrupção do prazo para RE (art. 1.044, §1º):**
A interposição de embargos de divergência no STJ **interrompe o prazo** para interposição de recurso extraordinário por qualquer das partes. Isso significa que, ao optar pelos embargos de divergência no STJ, o prazo do RE recomeça do zero com a publicação do acórdão que julgar os embargos.

**Nota crítica — prova da divergência (art. 1.043, §4º):**
O embargante deve provar a divergência com certidão, cópia ou citação de repositório oficial ou credenciado (inclusive eletrônico), ou com reprodução de julgado disponível na internet com indicação da fonte. A divergência deve demonstrar identidade de situações e divergência de teses — não apenas de resultados.

**Nota crítica — jurisprudência:**
O acórdão paradigma (prova da divergência) é elemento estrutural de cabimento — não é "jurisprudência ilustrativa". Identificar com número, turma, data e tese, usando o marcador:
`[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, órgão, data e texto exato do acórdão paradigma antes do protocolo]`

**Estrutura da peça:**

```
AO EXCELENTÍSSIMO SENHOR MINISTRO PRESIDENTE DO
[SUPERIOR TRIBUNAL DE JUSTIÇA / SUPREMO TRIBUNAL FEDERAL]

Processo nº [...]
Embargante: [...]
Embargado(a): [...]

[NOME DO EMBARGANTE], já qualificado(a) nos autos, por seu(sua) advogado(a),
vem interpor, com fundamento no art. 1.043, inciso [I/II/III/IV], do Código de
Processo Civil, os presentes

              EMBARGOS DE DIVERGÊNCIA

em face do acórdão proferido pela [Nª Turma] em [data], pelos fundamentos
a seguir.

I — DA TEMPESTIVIDADE

O acórdão embargado foi publicado em [data]. Prazo de 15 dias (RISTJ art. 267 /
RISTF art. 330):
[VERIFICAR: confirmar o prazo vigente no regimento interno do tribunal — [FORA
DO CORPUS] desta skill. Data-limite estimada: [data].]

II — DO CABIMENTO — DA DIVERGÊNCIA (art. 1.043)

    [texto literal do art. 1.043, caput e inciso aplicável, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

O acórdão embargado diverge do acórdão paradigma nos seguintes termos:

**Acórdão embargado:**
[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, órgão, data e texto exato antes do protocolo]:
[Nª Turma do STJ/STF], [tipo de recurso] nº [N], Rel. Min. [...], j. [data],
DJe [data]. Tese adotada: "[resumo da tese do acórdão embargado]."
Fonte: pesquisa web — [URL ou "não localizado — verificar manualmente"]

**Acórdão paradigma:**
[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, órgão, data e texto exato antes do protocolo]:
[Nª Turma / Seção / Corte Especial do STJ/STF], [tipo de recurso] nº [N],
Rel. Min. [...], j. [data], DJe [data]. Tese adotada: "[resumo da tese divergente]."
Fonte: pesquisa web — [URL ou "não localizado — verificar manualmente"]

[Demonstrar a identidade dos casos (mesma questão jurídica, mesmo enquadramento
normativo) e a divergência de teses entre os dois acórdãos. 2-3 parágrafos.]

[Prova da divergência (art. 1.043, §4º): cópia do acórdão paradigma — doc. [X].]

III — DA TESE CORRETA

[Expor a tese jurídica que o embargante sustenta como correta — a do acórdão
paradigma ou uma síntese que harmonize os entendimentos. Buscar via MCP os
dispositivos legais/constitucionais pertinentes à questão de fundo.]

    [texto literal do dispositivo legal/constitucional pertinente via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[Aplicação: por que o acórdão paradigma acertou e o acórdão embargado errou.
2-4 parágrafos.]

IV — DA INTERRUPÇÃO DO PRAZO PARA RE (se interposto no STJ — art. 1.044, §1º)

    [texto literal do art. 1.044, §1º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

[Incluir este item apenas quando o embargante (ou a parte contrária) pretende
também interpor RE: registrar a interrupção para não perder o prazo do RE.]

V — DO PEDIDO

Requer o(a) Embargante:
  a) o recebimento e processamento dos presentes Embargos de Divergência;
  b) o julgamento pelos [Corte Especial / Seção / Órgão Pleno], com a uniformização
     da jurisprudência do tribunal;
  c) o provimento dos embargos para que o acórdão embargado seja reformado e
     prevaleça a tese de que [resumo da tese correta];
  d) a condenação do(a) embargado(a) nas custas e honorários recursais
     (art. 85, §11, do CPC).

Termos em que pede deferimento.
[Cidade], [data].
```

---

**Grupo 3.4 — Cumprimento de sentença**

### 3.4.1 — Cumprimento de sentença — quantia certa (CPC arts. 523-527)

**Intake:**
- A sentença transitou em julgado? Data do trânsito.
- O devedor foi intimado a pagar? Já passaram os 15 dias sem pagamento?
- Qual é o valor principal condenado? Há juros e correção fixados na sentença?
- O credor quer que o memorial de cálculo seja elaborado agora ou vai juntar separado?
- Há bens do devedor conhecidos para indicar à penhora?

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO [...]

Processo nº [...]

[NOME DO EXEQUENTE], já qualificado(a) nos autos, por seu(sua) advogado(a),
vem requerer o início do

                    CUMPRIMENTO DE SENTENÇA

em face de [NOME DO EXECUTADO], com fundamento nos arts. 523 e seguintes do
CPC, pelos seguintes fundamentos:

I — DO TÍTULO EXECUTIVO E DO TRÂNSITO EM JULGADO

A sentença transitou em julgado em [data] (certidão — doc. [X]).

Nos termos do art. 523 do CPC:

    [texto literal do art. 523 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

II — DO VALOR ATUALIZADO

[Memorial de cálculo:]
  - Valor principal condenado: R$ [...]
  - Correção monetária ([índice] — [VERIFICAR: índice fixado na sentença ou
    legislação aplicável]) desde [data]: R$ [...]
  - Juros de mora ([taxa] ao mês — [VERIFICAR: taxa fixada na sentença ou art.
    aplicável via MCP]) desde [data]: R$ [...]
  - Honorários sucumbenciais fixados em sentença: R$ [...]
  - **TOTAL: R$ [...]**

[VERIFICAR: todos os índices e taxas acima precisam ser conferidos com a
sentença e com a legislação vigente — confirmar com o(a) advogado(a).]

III — DA MULTA E DOS HONORÁRIOS DE CUMPRIMENTO

Não tendo ocorrido pagamento espontâneo no prazo de 15 dias:

    [texto literal do art. 523, §1º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

IV — DOS PEDIDOS

Requer o(a) exequente:
  a) a intimação do(a) executado(a) para pagar o valor total de R$ [...] no
     prazo de 15 dias, sob pena da multa de 10% e honorários de 10% (art. 523, §1º);
  b) não ocorrendo o pagamento, a expedição de mandado de penhora e avaliação;
  c) a penhora preferencial sobre [bens indicados — se conhecidos] (art. 835 do CPC:
     [texto literal via MCP]);
  d) a juntada do memorial de cálculo em anexo (doc. [X]).

Termos em que pede deferimento.
[Cidade], [data].
```

### 3.4.2 — Cumprimento de sentença — obrigação de fazer/não fazer (CPC art. 536)

**Intake:**
- Qual é a obrigação fixada na sentença?
- O devedor está inadimplente? Desde quando?
- A parte quer pedir astreintes (multa por período de descumprimento — art. 536, §1º)?
- Há urgência que justifique medida de apoio (art. 536, §1º, segunda parte)?

**Estrutura básica:**

```
[Cabeçalho padrão]

[NOME DO EXEQUENTE] vem requerer o

         CUMPRIMENTO DE SENTENÇA — OBRIGAÇÃO DE FAZER

com fundamento no art. 536 do CPC:

    [texto literal do art. 536 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

I — DA OBRIGAÇÃO E DO INADIMPLEMENTO

[A sentença de [data] fixou a obrigação de [descrever]. O(a) executado(a) não
cumpriu até a presente data, conforme comprovam os docs. [X].]

II — DAS ASTREINTES  (art. 536, §1º)

    [texto literal do art. 536, §1º, e art. 537 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Propor valor das astreintes com critério fundamentado.]

III — DOS PEDIDOS

  a) a intimação do(a) executado(a) para cumprir a obrigação de [descrever]
     no prazo de [N] dias;
  b) a fixação de multa periódica (astreintes) de R$ [...] por [dia/semana]
     de descumprimento;
  c) [se urgência] medidas de apoio nos termos do art. 536, §1º.
```

---

### 3.4.3 — Impugnação ao cumprimento de sentença (CPC art. 525)

> ⚠️ **DEFESA ENDOPROCESSUAL — NÃO É AÇÃO AUTÔNOMA, NÃO É RECURSO.** A impugnação é apresentada **nos próprios autos** do cumprimento de sentença, independentemente de penhora ou nova intimação. Não distribui processo novo. O prazo começa automaticamente após o escoamento dos 15 dias do art. 523 sem pagamento voluntário.

**Intake:**
- Houve intimação para pagamento (art. 523)? Em que data? Já se passaram os 15 dias sem pagamento?
- Qual(is) das matérias do art. 525, §1º (I a VII) o executado pretende alegar?
- Há excesso de execução (art. 525, §1º, V)? Se sim, o executado deve apresentar **demonstrativo discriminado do valor que entende correto** — obrigatório, sob pena de rejeição liminar (art. 525, §4º/§5º).
- O executado quer pedir **efeito suspensivo** (art. 525, §6º)? Há penhora, caução ou depósito suficiente para garantir o juízo?
- A execução se funda em lei ou ato normativo declarado inconstitucional pelo STF (art. 525, §12)?

**Nota crítica — prazo (art. 525, caput):**
O prazo de **15 dias** começa automaticamente após o escoamento dos 15 dias do art. 523 sem pagamento. Não há nova intimação. Verificar a data da intimação original para o pagamento e calcular o início e o fim do prazo da impugnação.

**Nota crítica — efeito suspensivo (art. 525, §6º):**
A impugnação **não suspende automaticamente** a execução. Para obter efeito suspensivo, exige-se: (i) requerimento do executado; (ii) juízo garantido com penhora, caução ou depósito suficientes; (iii) fundamentos relevantes; (iv) prosseguimento da execução manifestamente suscetível de causar grave dano de difícil ou incerta reparação.

**Nota crítica — matérias do art. 525, §1º:**
Rol taxativo de defesas cabíveis na impugnação. A matéria mais abrangente é o inciso VII: **causa modificativa ou extintiva superveniente à sentença** (pagamento, novação, compensação, transação, prescrição). Matérias anteriores à sentença que não foram alegadas na fase de conhecimento estão preclUSAS — não cabem na impugnação.

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO [...]

Processo nº [...]
Exequente: [...]
Executado(a): [...]

[NOME DO EXECUTADO], já qualificado(a) nos autos, por seu(sua) advogado(a),
vem apresentar, no prazo legal, a presente

                IMPUGNAÇÃO AO CUMPRIMENTO DE SENTENÇA

com fundamento no art. 525 do Código de Processo Civil:

    [texto literal do art. 525, caput, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

I — DA TEMPESTIVIDADE

A intimação para pagamento (art. 523) foi publicada em [data]. Transcorridos os
15 dias sem pagamento voluntário, o prazo de 15 dias para impugnar iniciou-se
em [data] e se encerra em [data].
[VERIFICAR: conferir as datas no sistema do tribunal — feriados forenses
são [FORA DO CORPUS].]

II — DAS MATÉRIAS DA IMPUGNAÇÃO (art. 525, §1º)

    [texto literal do art. 525, §1º, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

II.1 — [MATÉRIA DO INCISO X — ex.: Do excesso de execução (art. 525, §1º, V)]

[Desenvolver a tese. Se for excesso de execução, apresentar demonstrativo
discriminado e atualizado do valor que o executado entende correto (art. 525,
§4º — obrigatório sob pena de rejeição liminar):]

Declara o(a) executado(a) que o valor correto é R$ [...], conforme demonstrativo
discriminado anexo (doc. [X]), nos termos do art. 525, §4º do CPC.

II.2 — [MATÉRIA DO INCISO Y] — mesma estrutura.

[Se inciso VII — causa superveniente à sentença, ex.: pagamento:]
A obrigação restou extinta por [pagamento / novação / prescrição superveniente],
ocorrido(a) em [data], conforme comprovam os docs. [X] e [Y] (art. 525, §1º, VII).

    [texto literal do art. 525, §1º, VII via MCP]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

III — DO EFEITO SUSPENSIVO   (art. 525, §6º — omitir se não requerido)

    [texto literal do art. 525, §6º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

O juízo está garantido por [penhora / caução / depósito] suficiente (doc. [X]).
Os fundamentos da impugnação são relevantes e o prosseguimento da execução é
manifestamente suscetível de causar ao executado grave dano de difícil ou
incerta reparação, porque [razão concreta].

IV — DOS PEDIDOS

Requer o(a) executado(a):
  a) [se efeito suspensivo] a atribuição de efeito suspensivo à impugnação,
     na forma do art. 525, §6º, até o seu julgamento;
  b) o recebimento e julgamento da impugnação;
  c) a procedência, para [resultado específico conforme as matérias alegadas]:
     — [inciso I: reconhecimento da nulidade da citação e anulação do processo
        desde esse momento]
     — [inciso V: redução do valor exequendo ao montante correto de R$ ...]
     — [inciso VII: declaração de extinção da obrigação por pagamento / prescrição
        e extinção do cumprimento de sentença].

Termos em que pede deferimento.
[Cidade], [data].
```

---

### 3.4.4 — Embargos à execução de título extrajudicial (CPC arts. 914-917 e 919)

> ⚠️ **AÇÃO AUTÔNOMA — DISTRIBUÍDA EM APARTADO.** Os embargos à execução são ação autônoma de defesa, distribuídos por **dependência** e autuados em **autos separados** (art. 914, §1º). Distinguem-se da impugnação ao cumprimento de sentença (art. 525) porque se opõem a **título extrajudicial** (CPC arts. 771 e seguintes), não a decisão judicial. O executado pode embargar **independentemente de penhora, depósito ou caução** (art. 914, caput) — diferença relevante em relação ao regime anterior do CPC/73. Sem efeito suspensivo automático (art. 919).

**Intake:**
- Qual é o título executivo extrajudicial (cheque, nota promissória, contrato, CDA, etc.)?
- Data da citação do executado na execução? (Prazo: 15 dias contados conforme art. 231 — verificar data correta.)
- Qual(is) das matérias do art. 917 (I a VI) serão alegadas?
- Se excesso de execução (art. 917, III): o embargante deve declarar imediatamente o valor correto e apresentar demonstrativo discriminado (art. 917, §3º) — obrigatório, sob pena de rejeição (art. 917, §4º).
- O embargante quer pedir **efeito suspensivo** (art. 919, §1º)? A execução já está garantida por penhora, depósito ou caução suficiente?

**Nota crítica — prazo (art. 915):**
15 dias contados da citação do executado na execução, conforme o art. 231. **Não se aplica o prazo em dobro** do art. 229 para litisconsortes representados por advogados diferentes (art. 915, §3º — regra expressa de exceção). Verificar a data da juntada do comprovante de citação nos autos da execução.

**Nota crítica — sem efeito suspensivo automático (art. 919):**
Os embargos não suspendem a execução por si sós. O efeito suspensivo pode ser concedido pelo juiz mediante requerimento, desde que: (i) a execução já esteja garantida por penhora, depósito ou caução suficiente; (ii) presentes os requisitos da tutela provisória (probabilidade do direito + urgência ou evidência).

**Nota crítica — amplitude das matérias (art. 917, VI):**
O inciso VI admite **qualquer matéria que seria lícito deduzir como defesa em processo de conhecimento**. Isso inclui vícios do negócio jurídico, nulidade do título, prescrição, pagamento anterior ao ajuizamento — qualquer defesa de mérito. É a diferença central em relação à impugnação ao cumprimento de sentença, cujo rol é mais restrito.

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO [...]

Processo de execução nº [...] — Autos da execução em apenso
Exequente: [...]
Embargante/Executado(a): [...]

[NOME DO EMBARGANTE], já qualificado(a) nos autos da execução em epígrafe,
por seu(sua) advogado(a), vem, nos termos do art. 914 do Código de Processo Civil,
oferecer os presentes

                    EMBARGOS À EXECUÇÃO

com fundamento no art. 914 c/c arts. 915 e 917 do CPC:

    [texto literal do art. 914 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

I — DA TEMPESTIVIDADE (art. 915)

A citação do(a) executado(a) foi juntada aos autos em [data]. O prazo de 15 dias
para embargar tem início em [data+1] e vencimento em [data]:

    [texto literal do art. 915, caput, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

[VERIFICAR: data-limite exata — feriados forenses são [FORA DO CORPUS]. Confirmar
que não se aplica o prazo em dobro do art. 229 (art. 915, §3º veda expressamente).]

II — DO TÍTULO EXECUTIVO E DA EXECUÇÃO

O(a) exequente ajuizou execução com base em [identificar o título extrajudicial —
cheque nº / nota promissória / contrato de [data] / CDA nº...], no valor de
R$ [...]. [Resumir o que está sendo executado — 1-2 parágrafos.]

III — DAS MATÉRIAS DOS EMBARGOS (art. 917)

    [texto literal do art. 917, caput e incisos aplicáveis, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

III.1 — [MATÉRIA DO INCISO X — ex.: Da inexequibilidade do título (art. 917, I)]

[Desenvolver a tese — ex.: o título não preenche os requisitos legais de
certeza/liquidez/exigibilidade; ou vício formal que o torna inexequível; ou
pagamento anterior ao ajuizamento; ou prescrição. 2-4 parágrafos.]

[Se inciso III — excesso de execução (obrigatório o demonstrativo):]
Declara o(a) embargante que o valor correto da execução é R$ [...], nos termos
do art. 917, §3º do CPC — demonstrativo discriminado e atualizado em anexo
(doc. [X]).

III.2 — [MATÉRIA DO INCISO VI — qualquer defesa de conhecimento, se aplicável]

[Développer tese de mérito: vício do negócio jurídico / causa debendi não
provada / inadimplemento recíproco / nulidade / outra defesa substancial.
Buscar os dispositivos do CC ou lei especial aplicável via MCP.]

IV — DO PEDIDO DE EFEITO SUSPENSIVO   (art. 919, §1º — omitir se não requerido)

    [texto literal do art. 919, §1º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

A execução encontra-se garantida por [penhora / depósito / caução] nos termos
do doc. [X]. Os requisitos da tutela provisória estão presentes: probabilidade
do direito (demonstrada no item III) e [urgência concreta / evidência].
Requer o(a) embargante a atribuição de efeito suspensivo aos presentes embargos
até o seu julgamento.

V — DOS PEDIDOS

Requer o(a) embargante:
  a) o recebimento dos presentes embargos;
  b) [se efeito suspensivo] a atribuição de efeito suspensivo, suspendendo a
     execução até o julgamento;
  c) a procedência dos embargos para:
     — [inciso I] declarar inexequível o título e extinguir a execução;
     — [inciso III] reduzir o valor exequendo ao correto de R$ [...];
     — [inciso VI] [resultado específico da defesa de mérito — ex.: declarar
        extinta a obrigação pelo pagamento comprovado / pela prescrição / pelo
        vício do negócio];
  d) a condenação do(a) exequente nas custas e honorários advocatícios.

Dá-se à causa o valor de R$ [...] [em regra, o valor da execução].

Termos em que pede deferimento.
[Cidade], [data].
```

---

### 3.4.5 — Exceção de pré-executividade

> ⚠️ **CONSTRUÇÃO PRETORIANA — NÃO HÁ LEI ESPECÍFICA.** A exceção de pré-executividade não está prevista em artigo do CPC. É criação doutrinária e jurisprudencial admitida pelo STJ e pelo STF como mecanismo de defesa do executado **sem penhora prévia e sem prazo fixo**, voltada exclusivamente a **matérias de ordem pública conhecíveis de ofício** que **não exijam dilação probatória**. Toda referência ao seu cabimento, à Súmula 393 do STJ e à construção pretoriana leva **marcador obrigatório de jurisprudência** — aplicar a regra das peças ordinárias com adaptação: `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato antes do protocolo]`.

> A âncora normativa mais próxima no CPC é o **art. 803, parágrafo único**, que autoriza o juiz a reconhecer as nulidades da execução **de ofício ou a requerimento da parte, independentemente de embargos**. Esse dispositivo vem do MCP; o cabimento da exceção de pré-executividade em si — e seus limites — vem da jurisprudência.

**Intake:**
- O executado pretende alegar matéria de **ordem pública** (nulidade do título, ilegitimidade ativa/passiva, prescrição, decadência, inexigibilidade da obrigação, ausência de citação)?
- A matéria pode ser provada **sem dilação probatória** — apenas com documentos pré-constituídos? (Se precisar de testemunhas, perícia ou outra instrução, a via correta é os embargos à execução ou a impugnação, não a exceção.)
- Há penhora realizada? (Irrelevante para o cabimento — mas informar ao usuário que os embargos à execução também seriam cabíveis e podem ser mais amplos.)
- Qual é o título executivo (extrajudicial ou judicial)?

**Nota crítica — limite material: ordem pública + prova documental:**
O STJ consolidou que a exceção de pré-executividade cabe para matérias que (i) o juiz poderia reconhecer de ofício e (ii) não demandam dilação probatória.

Matérias típicas admitidas: nulidade absoluta da execução (art. 803 do CPC), prescrição do título, ilegitimidade de parte, inexistência ou nulidade do título executivo, inconstitucionalidade de norma que fundamenta a execução. Matérias que exigem instrução (pagamento não documentado, compensação, excesso de execução dependente de cálculo controverso) → NÃO cabem na exceção de pré-executividade; usar embargos ou impugnação.

[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato antes do protocolo]: STJ, Súmula 393: "A exceção de pré-executividade é admissível na execução fiscal relativamente às matérias conhecíveis de ofício que não demandem dilação probatória." Aplicada por analogia às execuções comuns pelos tribunais. Confirmar o texto atual da Súmula antes do protocolo.

**Nota crítica — âncora normativa (art. 803, parágrafo único do CPC):**
O parágrafo único do art. 803 é a base legal mais sólida para requerer o reconhecimento de nulidades da execução independentemente de embargos — e portanto independentemente de penhora:

    Art. 803. [...] Parágrafo único. A nulidade de que cuida este artigo será pronunciada pelo juiz, de ofício ou a requerimento da parte, independentemente de embargos à execução.
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

Para matérias além das nulidades do art. 803 (ex.: prescrição), a âncora é exclusivamente a construção pretoriana — marcador obrigatório.

**Nota crítica — diferença em relação aos embargos à execução (art. 914):**
- **Embargos:** ação autônoma, autuada em apartado, prazo de 15 dias da citação, matérias amplas (art. 917), admite dilação probatória.
- **Exceção de pré-executividade:** petição simples nos próprios autos, sem prazo fixo (enquanto a execução não estiver extinta), matérias restritas a ordem pública + prova documental.
Ambas podem ser usadas simultaneamente se a matéria couber nos dois veículos — avaliar com o(a) advogado(a).

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO [...]

Processo de execução nº [...]
Exequente: [...]
Executado(a)/Requerente: [...]

[NOME DO EXECUTADO], já qualificado(a) nos autos, por seu(sua) advogado(a),
vem apresentar, nos próprios autos, a presente

              EXCEÇÃO DE PRÉ-EXECUTIVIDADE

para requerer a extinção/nulidade da presente execução, pelos fundamentos a seguir.

I — DO CABIMENTO

A exceção de pré-executividade é instrumento de defesa endoprocessual admitido
pela jurisprudência consolidada do Superior Tribunal de Justiça:

[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato antes do protocolo]:
STJ, Súmula 393: "A exceção de pré-executividade é admissível na execução fiscal
relativamente às matérias conhecíveis de ofício que não demandem dilação probatória."
Aplicação analógica à execução comum — confirmar o texto e o alcance atual da Súmula.
Fonte: [pesquisa web — URL ou "não localizado — verificar manualmente"]

A matéria ora arguida é de **ordem pública**, conhecível de ofício pelo juízo
(art. 803, parágrafo único, do CPC), e demonstrável por **prova documental pré-constituída**
— sem necessidade de dilação probatória:

    [texto literal do art. 803, parágrafo único, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

II — DA [MATÉRIA DE ORDEM PÚBLICA ARGUIDA]

[Identificar com precisão o vício/matéria. Exemplos:]

[Se prescrição:]
A pretensão executiva está prescrita. O título data de [data]; o prazo prescricional
aplicável é de [N] anos (art. [X] do [CC/lei especial] — buscar via MCP). Transcorrido
o prazo sem interrupção:

    [texto literal do dispositivo de prescrição via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[Demonstrar: data do vencimento da obrigação + ausência de causa interruptiva
+ data do ajuizamento = prescrição consumada. Documentar com o próprio título.]

[Se nulidade do título — inexequibilidade (art. 803, I):]
O título apresentado não corresponde a obrigação certa, líquida e exigível
(art. 803, I, do CPC): [demonstrar o vício — ex.: obrigação ilíquida; condição
não implementada; ausência de data de vencimento.]

    [texto literal do art. 803, I, via MCP]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

[Se ilegitimidade passiva:]
O(a) executado(a) não é parte na relação obrigacional que deu origem ao título.
[Demonstrar com documentos pré-constituídos — certidão, escritura, contrato.]

III — DA PROVA DOCUMENTAL

Toda a arguição está amparada em prova documental pré-constituída, dispensando
dilação probatória:
- Doc. [X]: [descrever — ex.: cópia do título com data de emissão]
- Doc. [Y]: [descrever — ex.: certidão de distribuição sem interrupção do prazo]
- Doc. [Z]: [descrever]

IV — DO PEDIDO

Requer o(a) executado(a) que Vossa Excelência:
  a) conheça da presente exceção de pré-executividade e, reconhecendo a
     [prescrição / nulidade do título / ilegitimidade / ...]:
  b) declare extinta a execução nos termos do art. 924 do CPC:

    [texto literal do art. 924, inciso aplicável, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

  [ou, se nulidade sem extinção total:]
  b) declare a nulidade [parcial/total] da execução e determine [a medida adequada],
     nos termos do art. 803, parágrafo único, do CPC;

  c) condene o(a) exequente ao pagamento das custas e honorários advocatícios.

Termos em que pede deferimento.
[Cidade], [data].
```

---

**Grupo 3.5 — Ações autônomas de impugnação**

### 3.5.1 — Reclamação constitucional (CPC arts. 988-993)

> ⚠️ **A RECLAMAÇÃO NÃO É RECURSO — É AÇÃO ORIGINÁRIA.** Não há prazo recursal; há um limite negativo: é inadmissível após o **trânsito em julgado** da decisão reclamada (art. 988, §5º, I). A reclamação **não substitui o recurso cabível** e exige **aderência estrita** entre o ato reclamado e o paradigma invocado (competência usurpada, decisão desautorada, súmula vinculante, decisão do STF em controle concentrado, IRDR ou IAC). Usá-la como atalho recursal leva ao não conhecimento.

**Os quatro fundamentos do art. 988 — cada um com cabimento próprio:**

| Inciso | Fundamento | Competência para julgar |
|---|---|---|
| I | Preservar a **competência** do tribunal (ato usurpou competência que era do tribunal) | O tribunal cuja competência foi usurpada |
| II | Garantir a **autoridade das decisões** do tribunal (ato descumpriu decisão concreta proferida pelo tribunal naquele caso ou em caso vinculante) | O tribunal cuja decisão foi descumprida |
| III | Garantir a observância de **enunciado de súmula vinculante** e de **decisão do STF em controle concentrado** de constitucionalidade | STF |
| IV | Garantir a observância de **acórdão em IRDR** ou em **incidente de assunção de competência (IAC)** | O tribunal que julgou o IRDR/IAC |

**Intake:**
- Qual é o **ato reclamado** — decisão, ato administrativo ou judicial que se quer desconstituir? Pedir o documento.
- Qual é o **paradigma** invocado (qual dos quatro incisos)? Identificar com precisão: número da súmula vinculante, acórdão do STF em ADI/ADC/ADPF, acórdão do próprio tribunal, ou tese de IRDR/IAC.
- A decisão reclamada **já transitou em julgado**? (Se sim, a reclamação é inadmissível — art. 988, §5º, I.)
- [Se inciso III por RG/repetitivo] As **instâncias ordinárias foram esgotadas**? (Art. 988, §5º, II — sem esgotamento, é inadmissível.)
- Há urgência que justifique pedido de **suspensão** do ato/processo (art. 989, II)?

**Nota crítica — aderência estrita e §4º:**
A reclamação exige correspondência exata entre o caso concreto e o padrão decisório (art. 988, §4º — compreende tanto a **aplicação indevida** da tese quanto a **não aplicação** aos casos que a ela correspondam). Antes de redigir, demonstrar ponto a ponto a identidade entre a situação dos autos e o paradigma. Distinção fática relevante (distinguishing) entre o caso e o paradigma derruba a reclamação — sinalizar ao usuário se houver risco.

**Nota crítica — §5º (inadmissibilidades):**
- **§5º, I:** inadmissível após o trânsito em julgado da decisão reclamada. Verificar a data do trânsito antes de qualquer coisa.
- **§5º, II:** para garantir acórdão de RE com repercussão geral ou de RE/REsp repetitivos, é inadmissível **enquanto não esgotadas as instâncias ordinárias**. Confirmar o esgotamento.

**Nota crítica — jurisprudência e paradigma:**
O paradigma (súmula vinculante, acórdão do STF em controle concentrado, acórdão de IRDR/IAC, decisão do próprio tribunal) **é o fundamento de cabimento da reclamação — não é "jurisprudência ilustrativa"** e deve ser identificado com número, órgão e data. Como esses dados não vêm do MCP de legislação, marcar com `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, órgão julgador, data e texto exato do paradigma antes do protocolo]`. Buscar a ementa na web quando possível e registrar a fonte. As **leis** processuais (arts. 988-993) seguem a regra normal: texto literal via MCP.

**Nota crítica — endereçamento e instrução:**
A reclamação é **dirigida ao presidente do tribunal** competente e **instruída com prova documental** (art. 988, §2º). Sem a prova documental do ato reclamado e do paradigma, a inicial é inepta.

**Estrutura da peça:**

```
AO EXCELENTÍSSIMO SENHOR PRESIDENTE DO [TRIBUNAL COMPETENTE —
STF / STJ / TRF / TJ, conforme o paradigma]

Reclamante: [...]
Reclamado(a): [autoridade/órgão que praticou o ato reclamado]
Beneficiário(a): [parte beneficiada pela decisão reclamada — será citada]

[NOME DO RECLAMANTE], por seu(sua) advogado(a), vem, com fundamento no
art. 102, I, "l" / 105, I, "f" da Constituição Federal [conforme o tribunal]
e nos arts. 988 a 993 do Código de Processo Civil, propor

              RECLAMAÇÃO [CONSTITUCIONAL]

em face de [ato/decisão reclamada], pelos fundamentos a seguir.

I — DO CABIMENTO

A presente reclamação é cabível com fundamento no art. 988, inciso [I/II/III/IV],
do CPC:

    [texto literal do art. 988, caput e inciso aplicável, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Identificar com precisão o inciso e por que ele se aplica.]

II — DO PARADIGMA INVOCADO

[Identificar o paradigma — súmula vinculante nº / acórdão do STF em [ADI/ADC/ADPF] /
acórdão de IRDR/IAC / decisão do tribunal nos autos nº ...]

[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, órgão julgador, data e texto exato do paradigma antes do protocolo]:
[Identificação e tese do paradigma — ex.: "Súmula Vinculante nº [N]: '[texto]'" ou
"No julgamento da [ADI/ADC] nº [N], o STF firmou que [tese]".]
Fonte: pesquisa web — [URL se disponível, ou "não localizado — verificar manualmente"]

III — DO ATO RECLAMADO

[Descrever e citar literalmente o ato/decisão reclamada — como Fonte 3 (autos):]

    [Citação literal do ato reclamado]
    Fonte: [identificação do ato] — [data/ID] — [processo de origem, se houver]

IV — DA ADERÊNCIA ESTRITA (art. 988, §4º)

    [texto literal do art. 988, §4º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Demonstrar ponto a ponto a identidade entre o caso e o paradigma — por que o
ato reclamado [usurpou a competência / desautorou a decisão / contrariou a súmula
vinculante / aplicou indevidamente ou deixou de aplicar a tese]. 2-4 parágrafos.]

V — DA ADMISSIBILIDADE (art. 988, §5º)

A decisão reclamada NÃO transitou em julgado [VERIFICAR: confirmar — reclamação
após trânsito em julgado é inadmissível, art. 988, §5º, I].
[Se inciso III por RG/repetitivo:] As instâncias ordinárias foram esgotadas,
nos termos do art. 988, §5º, II.

VI — DO PEDIDO LIMINAR DE SUSPENSÃO   (art. 989, II — omitir se não houver urgência)

    [texto literal do art. 989, II via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Demonstrar o risco de dano irreparável que justifica a suspensão liminar do
ato/processo.]

VII — DOS PEDIDOS

Requer o(a) Reclamante:
  a) o recebimento e processamento da reclamação, com a requisição de informações
     à autoridade reclamada (art. 989, I) e a citação do(a) beneficiário(a)
     (art. 989, III);
  b) [se urgência] a concessão de liminar para suspender [o ato / o processo de
     origem] até o julgamento (art. 989, II);
  c) a procedência da reclamação para CASSAR a decisão reclamada e determinar
     [a medida adequada à observância do paradigma / preservação da competência]
     (art. 992):

    [texto literal do art. 992 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

Instrui esta reclamação a prova documental anexa (art. 988, §2º): [listar docs].

Termos em que pede deferimento.
[Cidade], [data].
```

### 3.5.2 — Ação Rescisória (CPC arts. 966-975)

> ⚠️ **AÇÃO AUTÔNOMA DE IMPUGNAÇÃO — NÃO É RECURSO.** Pressupõe **decisão de mérito transitada em julgado** (art. 966, caput) — ou decisão que, embora não de mérito, impeça nova propositura ou a admissibilidade do recurso (art. 966, §2º). Tem **prazo decadencial** (não prescricional) e estrutura **bifásica**: o *iudicium rescindens* (desconstituir a coisa julgada) e, quando for o caso, o *iudicium rescissorium* (rejulgar a causa). Exige **depósito de 5%** do valor da causa (art. 968, II), salvo isenções.

**As oito hipóteses do art. 966 — diagnosticar qual(is) se aplica(m):**

| Inciso | Hipótese | O que o autor precisa demonstrar |
|---|---|---|
| I | Prevaricação, concussão ou corrupção do juiz | Conduta criminosa do julgador que contaminou a decisão |
| II | Juiz impedido ou juízo absolutamente incompetente | Impedimento (art. 144) ou incompetência absoluta — não a relativa |
| III | Dolo/coação da parte vencedora, ou simulação/colusão das partes para fraudar a lei | Vício de conduta da parte que distorceu o resultado |
| IV | Ofensa à coisa julgada | A decisão rescindenda desrespeitou coisa julgada anterior |
| V | Violação manifesta de norma jurídica | Erro grave e evidente na aplicação do direito (não mera injustiça) — ver §§5º e 6º para súmula/repetitivo |
| VI | Prova falsa (apurada em processo criminal ou demonstrada na própria rescisória) | A decisão se fundou em prova cuja falsidade se comprova |
| VII | Prova nova, obtida após o trânsito, capaz por si só de assegurar pronunciamento favorável | Existência ignorada ou uso impossível à época + aptidão decisiva da prova |
| VIII | Erro de fato verificável do exame dos autos (art. 966, §1º) | Decisão admitiu fato inexistente ou negou fato ocorrido, sem ponto controvertido sobre ele |

**Nota crítica — inciso V (violação manifesta) + §§5º e 6º:**
O inciso V não serve para rediscutir a justiça da decisão — exige violação **manifesta** de norma. Quando a rescisória atacar decisão baseada em **súmula ou acórdão de casos repetitivos** que não considerou distinção (distinguishing), aplica-se o art. 966, §§5º e 6º: o autor deve, **sob pena de inépcia**, demonstrar fundamentadamente a situação particularizada (hipótese fática distinta ou questão jurídica não examinada). Buscar os §§5º e 6º via MCP e incluí-los expressamente quando for esse o fundamento.

**Intake:**
- Qual é a **decisão rescindenda**? Pedir o acórdão/sentença e a **certidão de trânsito em julgado** (data é essencial para o prazo decadencial).
- **Qual(is) hipótese(s) do art. 966** fundamenta(m) a rescisória? (Pode haver cumulação.)
- Qual a **data do trânsito em julgado da última decisão** proferida no processo? (Prazo: 2 anos — art. 975. Ver notas críticas sobre as exceções.)
- Quem é o autor da rescisória — parte vencida, terceiro juridicamente interessado, MP (art. 967)?
- O autor é **isento do depósito** de 5% (União, Estado, Município, autarquia/fundação de direito público, MP, Defensoria, beneficiário de gratuidade — art. 968, §1º)? Se não, calcular 5% do valor da causa (limite de 1.000 salários mínimos — §2º).
- Há **necessidade de novo julgamento** (iudicium rescissorium) ou apenas de desconstituir (ex.: rescisória por incompetência que só anula)?
- Há urgência para **tutela provisória** que suspenda o cumprimento da decisão rescindenda (art. 969)?

**Nota crítica — competência (escalonada):**
A ação rescisória é da competência do **tribunal que proferiu a decisão rescindenda**, ou do tribunal competente conforme a última decisão de mérito. Se o mérito foi decidido em 1º grau e a apelação não o alterou, a competência é do **TJ/TRF**. Se RE/REsp foi **conhecido e julgado no mérito**, a rescindenda é a decisão do **STF/STJ** e a competência é da respectiva corte; se o RE/REsp foi **inadmitido** (não conheceu do mérito), a rescindenda permanece sendo o acórdão do tribunal a quo. `[VERIFICAR: confirmar qual foi a última decisão de mérito e o tribunal competente — erro de competência leva à emenda forçada da inicial, art. 968, §5º.]`

**Nota crítica — prazo decadencial (art. 975 — regra e exceções):**
- **Regra geral:** 2 anos contados do **trânsito em julgado da última decisão** proferida no processo (art. 975, caput). Prorroga para o 1º dia útil seguinte se vencer em férias/recesso/feriado (§1º).
- **Prova nova (inciso VII):** termo inicial é a **data de descoberta da prova**, com **teto de 5 anos** do trânsito em julgado (§2º).
- **Simulação ou colusão:** para o terceiro prejudicado e o MP que não interveio, o prazo corre da **ciência** da simulação/colusão (§3º).
- Buscar o art. 975 via MCP e apresentar o texto ao usuário antes de afirmar qualquer data-limite. A contagem em dias/meses no sistema é `[FORA DO CORPUS]`.

**Nota crítica — depósito de 5% (art. 968, II):**
O depósito converte-se em **multa** em favor do réu se a rescisória for, **por unanimidade**, declarada inadmissível ou improcedente. Mencionar o depósito (ou a isenção) na inicial. O valor exato e a guia são `[FORA DO CORPUS — conferir tabela do tribunal]`.

**Nota crítica — jurisprudência:**
Aplicar a regra das peças ordinárias (Fonte 2): jurisprudência **vedada** no corpo, salvo o paradigma quando a rescisória for de inciso IV (coisa julgada anterior) ou inciso V com base em súmula/repetitivo — nesses casos o ato paradigma é elemento do cabimento e vai com `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, órgão e data antes do protocolo]`. Demais teses de apoio → `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`.

**Estrutura da peça:**

```
AO EXCELENTÍSSIMO SENHOR PRESIDENTE DO [TRIBUNAL COMPETENTE —
TJ / TRF / STJ / STF, conforme a decisão rescindenda]

Autor(a): [...]
Réu(é): [parte beneficiada pela decisão rescindenda]

[NOME DO AUTOR], por seu(sua) advogado(a), vem, com fundamento no art. 966,
inciso(s) [...], e nos arts. 967 a 975 do Código de Processo Civil, propor

              AÇÃO RESCISÓRIA

em face de [NOME DO RÉU], para rescindir [a sentença / o acórdão] proferido(a)
em [data], transitado(a) em julgado em [data], pelos fundamentos a seguir.

I — DA TEMPESTIVIDADE (PRAZO DECADENCIAL)

A decisão rescindenda transitou em julgado em [data] (certidão — doc. [X]).
O prazo decadencial é de 2 anos (art. 975 do CPC):

    [texto literal do art. 975 (caput e §§ aplicáveis) via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Se inciso VII — prova nova:] O termo inicial é a data da descoberta da prova
([data]), observado o teto de 5 anos (art. 975, §2º).
[Se simulação/colusão:] O prazo corre da ciência (art. 975, §3º).

[VERIFICAR: data-limite exata — contar no sistema do tribunal; férias/recesso
prorrogam (§1º). Contagem é [FORA DO CORPUS].]

II — DA COMPETÊNCIA

A competência para a rescisória é do [Tribunal], por ser o órgão que proferiu a
[última decisão de mérito]. [VERIFICAR: confirmar qual foi a última decisão de
mérito — ver nota de competência escalonada.]

III — DA LEGITIMIDADE (art. 967)

O(a) Autor(a) é [parte vencida / terceiro juridicamente interessado / Ministério
Público], com legitimidade nos termos do art. 967, inciso [...]:

    [texto literal do art. 967, inciso aplicável, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

IV — DO DEPÓSITO DE 5% (art. 968, II)   [ou: DA ISENÇÃO DE DEPÓSITO]

[Se devido:] O(a) Autor(a) efetua o depósito de 5% sobre o valor da causa
(art. 968, II), no valor de R$ [...] [FORA DO CORPUS — conferir guia e tabela
do tribunal; limite de 1.000 salários mínimos, art. 968, §2º].

    [texto literal do art. 968, II e §1º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Se isento:] O(a) Autor(a) é isento(a) do depósito, por ser [União/Estado/
Município/autarquia/MP/Defensoria/beneficiário de gratuidade] (art. 968, §1º).

V — DA DECISÃO RESCINDENDA

[Resumir o que a decisão rescindenda decidiu — 2-3 parágrafos factuais. Citar
literalmente o trecho relevante, como Fonte 3 (autos):]

    [Citação literal do trecho da decisão rescindenda]
    Fonte: [Sentença/Acórdão] ID [ID] — [data] — autos nº [número do processo]

VI — DO JUÍZO RESCINDENS — DO FUNDAMENTO DA RESCISÃO

VI.[A] — DA [HIPÓTESE DO ART. 966, INCISO X]

    [texto literal do art. 966, inciso aplicável (e §§ 1º/5º/6º se cabível) via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Demonstrar a configuração da hipótese:
 - inciso II → impedimento/incompetência absoluta concreta;
 - inciso V → qual norma foi manifestamente violada e como (+ §§5º/6º se súmula/repetitivo);
 - inciso VI → a prova falsa e a apuração de sua falsidade;
 - inciso VII → a prova nova, a ignorância/impossibilidade de uso à época e sua aptidão decisiva;
 - inciso VIII → o fato admitido/negado contra os autos (art. 966, §1º).
 2-5 parágrafos de subsunção rigorosa.]

[Se a hipótese for IV ou V com paradigma:]
[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, órgão e data antes do protocolo]:
[Identificação da coisa julgada anterior / súmula / acórdão repetitivo paradigma.]
Fonte: pesquisa web — [URL ou "não localizado — verificar manualmente"]

VII — DO JUÍZO RESCISSORIUM — DO NOVO JULGAMENTO   (art. 968, I — omitir se a
rescisão apenas desconstitui, sem rejulgamento)

Rescindida a decisão, requer o(a) Autor(a) o **novo julgamento** da causa, nos
termos do art. 968, I, do CPC, para que o Tribunal decida [o que deve ser
decidido no lugar da decisão rescindida].

    [texto literal do art. 968, I via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

VIII — DA TUTELA PROVISÓRIA   (art. 969 — omitir se não houver urgência)

    [texto literal do art. 969 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[A propositura não impede o cumprimento da decisão rescindenda; requerer tutela
provisória para suspendê-lo, demonstrando probabilidade do direito e perigo de dano.]

IX — DOS PEDIDOS

Requer o(a) Autor(a):
  a) o recebimento da ação e a citação do(a) réu(é) para responder no prazo
     fixado pelo relator (art. 970), entre 15 e 30 dias;
  b) [se urgência] a concessão de tutela provisória para suspender o cumprimento
     da decisão rescindenda (art. 969);
  c) no JUÍZO RESCINDENS, a procedência para RESCINDIR [a sentença/o acórdão]
     com fundamento no art. 966, [inciso(s)];
  d) [se cabível] no JUÍZO RESCISSORIUM, o novo julgamento da causa para
     [pedido específico];
  e) a condenação do(a) réu(é) nas custas e honorários advocatícios.

Dá-se à causa o valor de R$ [...].

Termos em que pede deferimento.
[Cidade], [data].
```

---

### 3.5.3 — Oposição (CPC arts. 682-686)

> ⚠️ **AÇÃO AUTÔNOMA INCIDENTAL — NÃO É RECURSO, NÃO É DEFESA.** A oposição é ação proposta por **terceiro** (o opoente) que pretende, no todo ou em parte, a coisa ou o direito sobre que controvertem autor e réu. Não é defesa do réu — é nova demanda de um terceiro que não é parte na ação originária. Distribuída por **dependência** e apensada aos autos, tramita simultaneamente à ação originária e é julgada pela **mesma sentença** (art. 685). O opoente é autor de uma ação nova; os opostos (autor e réu originários) são réus na oposição.

**Intake:**
- Quem é o opoente — terceiro que não é parte na ação originária?
- Qual é a coisa ou o direito disputado na ação originária que o opoente alega ser seu?
- A sentença na ação originária já foi proferida? (Oposição só pode ser oferecida **até a sentença** — art. 682. Após a sentença, o terceiro deve buscar outra via — embargos de terceiro, ação própria.)
- A oposição é oferecida antes ou depois do início da audiência de instrução? (Relevante para o §único do art. 685.)

**Nota crítica — prazo e limite temporal (art. 682):**
A oposição pode ser proposta **a qualquer tempo até a prolação da sentença** no processo originário. Não há prazo mínimo, mas quanto mais tarde for apresentada, maior o risco de o juiz ter já encerrado a instrução. Se a sentença já foi proferida, a oposição é inadmissível — o terceiro terá de buscar outra via (embargos de terceiro, se for o caso, ou ação própria de reivindicação).

**Nota crítica — estrutura de petição inicial completa (art. 683):**
O opoente deduz o pedido com **observância dos requisitos do art. 319** (petição inicial). Qualificação completa das partes (opoente e opostos), causa de pedir, pedido, valor da causa, documentos essenciais. Os opostos são citados **na pessoa de seus respectivos advogados** (não pessoalmente) para contestar em **prazo comum de 15 dias** (art. 683, parágrafo único).

**Nota crítica — julgamento (arts. 685-686):**
O juiz julga a oposição **em primeiro lugar** — antes da ação originária (art. 686). Se a oposição for procedente no todo, a ação originária perde o objeto. Se procedente em parte, o resultado influencia parcialmente. O julgamento é feito na **mesma sentença** que resolve a ação originária (art. 685).

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO [...]

Processo nº [...] — Ação originária entre [AUTOR] e [RÉU]

[NOME DO OPOENTE], [qualificação completa: nacionalidade, estado civil,
profissão, RG, CPF, endereço], por seu(sua) advogado(a) infra-assinado(a)
(procuração — doc. [X]), vem propor a presente

                         O P O S I Ç Ã O

em face de [NOME DO OPOSTO 1 — autor originário] e [NOME DO OPOSTO 2 —
réu originário], com fundamento nos arts. 682 a 686 do Código de Processo Civil:

    [texto literal do art. 682 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

pelos fundamentos a seguir.

I — DA ADMISSIBILIDADE

I.1 — Da legitimidade do opoente

O(a) opoente é terceiro(a) não integrante da relação processual originária,
que pretende a coisa/direito sobre que controvertem os opostos. A sentença
na ação originária ainda não foi proferida, razão pela qual a oposição é
tempestiva nos termos do art. 682 do CPC.

I.2 — Do processamento

Nos termos do art. 683 do CPC, a oposição será distribuída por dependência
e os opostos serão citados na pessoa de seus advogados para contestar em
prazo comum de 15 dias:

    [texto literal do art. 683 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

II — DOS FATOS

[Narrar os fatos que fundamentam a pretensão do opoente sobre a coisa ou
o direito disputado. Demonstrar por que o opoente é o titular do direito
ou a quem pertence a coisa, e não a nenhum dos opostos.
Referir documentos de prova — doc. [X], doc. [Y]. 3-6 parágrafos.]

III — DO DIREITO

[Fundamentar juridicamente a pretensão do opoente. Buscar via MCP os
dispositivos aplicáveis (ex.: CC arts. de propriedade, posse, contrato,
etc.). Estrutura padrão: texto literal via MCP + subsunção ao caso.]

    [texto literal do dispositivo legal aplicável via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[Aplicação ao caso: demonstrar que o opoente é o verdadeiro titular do
direito ou proprietário da coisa. 2-4 parágrafos.]

IV — DOS PEDIDOS

Requer o(a) opoente:
  a) o recebimento e processamento da presente oposição, com sua distribuição
     por dependência e apensamento aos autos da ação originária (art. 685 do CPC);
  b) a citação dos opostos [OPOSTO 1] e [OPOSTO 2] na pessoa de seus
     respectivos advogados, para contestarem no prazo comum de 15 dias
     (art. 683, parágrafo único);
  c) ao final, o julgamento da oposição em primeiro lugar (art. 686 do CPC):

    [texto literal do art. 686 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

  d) a procedência da oposição para declarar que a coisa/o direito disputado
     nos autos pertence ao(à) opoente, e não a nenhum dos opostos;
  e) a condenação dos opostos nas custas e honorários advocatícios.

Dá-se à causa o valor de R$ [...].

Termos em que pede deferimento.
[Cidade], [data].
```

---

### 3.5.4 — Embargos de terceiro (CPC arts. 674-681)

> ⚠️ **AÇÃO AUTÔNOMA INCIDENTAL — NÃO É RECURSO, NÃO É DEFESA DO EXECUTADO.** Os embargos de terceiro são ação proposta por **quem não é parte no processo** mas sofre constrição judicial (penhora, arresto, sequestro, apreensão) sobre bens seus ou sobre direito incompatível com o ato constritivo. Distribuídos por **dependência** ao juízo que ordenou a constrição e autuados em **autos separados** (art. 676). O embargante é autor de uma nova ação; os embargados são quem se aproveita da constrição e/ou quem indicou o bem.

**Intake:**
- Quem é o embargante — terceiro que não é parte no processo principal?
- Qual é o **ato constritivo** (penhora, arresto, sequestro, apreensão)? Pedir o auto ou documento que o identifica.
- O embargante é **proprietário** (tem domínio) ou **possuidor** do bem atingido?
- O bem está em fase de conhecimento ou de execução/cumprimento? (Relevante para o prazo — art. 675.)
- Já ocorreu adjudicação, alienação particular ou arrematação? Se sim, já se passaram mais de 5 dias? (Se sim, embargos intempestivos — prazo fatal.)
- Qual é o **fundamento específico** do embargante? (Ver rol do art. 674, §2º — cônjuge/meação, adquirente em fraude à execução, desconsideração de personalidade, credor com garantia real não intimado.)

**Nota crítica — prazo (art. 675):**
- **Processo de conhecimento:** até a sentença transitar em julgado (sem prazo mínimo).
- **Execução/cumprimento de sentença:** até **5 dias depois** da adjudicação, da alienação por iniciativa particular ou da arrematação — **mas sempre antes da assinatura da respectiva carta**. Após a assinatura da carta, os embargos são inadmissíveis; o terceiro terá de buscar outra via (ação reivindicatória própria).

**Nota crítica — quatro hipóteses especiais de "terceiro" (art. 674, §2º):**

| Inciso | Quem é considerado "terceiro" | Detalhe |
|---|---|---|
| I | Cônjuge/companheiro que defende bens próprios ou meação | Ressalvado art. 843 (bens comuns dos cônjuges em débito do casal) |
| II | Adquirente de bem em fraude à execução (art. 792) | Terá de demonstrar boa-fé — ônus invertido em bens não registráveis (art. 792, §2º) |
| III | Quem sofre constrição por desconsideração de personalidade da qual não participou | Útil quando a constrição atinge sócio não incluído no incidente |
| IV | Credor com garantia real (hipoteca, penhor) não intimado dos atos expropriatórios | Protege o credor hipotecário que não foi incluído no processo |

**Nota crítica — legitimidade passiva (art. 677, §4º):**
São legitimados passivos: (i) o sujeito a quem a constrição aproveita (normalmente o exequente/credor) e (ii) o adversário no processo principal que indicou o bem para a constrição. Ambos devem ser citados.

**Nota crítica — liminar de suspensão (art. 678):**
O juiz pode suspender a constrição desde que o embargante demonstre sumariamente o domínio ou a posse. Pode condicionar à prestação de caução, salvo hipossuficiência econômica (art. 678, parágrafo único). Requerer sempre — sem a liminar, o bem pode ser alienado durante o trâmite dos embargos.

**Nota crítica — jurisprudência:**
Aplicar a regra das peças ordinárias (Fonte 2): jurisprudência vedada → `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`.

**Estrutura da peça:**

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO [...]

Processo nº [...] — Ação originária / Processo de execução
Embargante: [NOME DO TERCEIRO — NÃO É PARTE NO PROCESSO PRINCIPAL]
Embargado(a) 1: [quem se aproveita da constrição — ex.: exequente/credor]
Embargado(a) 2: [quem indicou o bem, se diferente — ex.: réu/devedor]

[NOME DO EMBARGANTE], [qualificação completa: nacionalidade, estado civil,
profissão, RG, CPF, endereço], por seu(sua) advogado(a) infra-assinado(a)
(procuração — doc. [X]), vem propor os presentes

                   EMBARGOS DE TERCEIRO

com fundamento nos arts. 674 a 681 do Código de Processo Civil:

    [texto literal do art. 674, caput e §§1º-2º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

pelos fundamentos a seguir.

I — DA ADMISSIBILIDADE E DA TEMPESTIVIDADE

I.1 — Da qualidade de terceiro

O(a) embargante não é parte no processo principal nº [...]. É [proprietário(a)/
possuidor(a)] do bem objeto da constrição — doc. [X]. Nos termos do art. 674, §2º,
inciso [I/II/III/IV], é considerado(a) terceiro(a) para fins dos presentes embargos:
[Justificar o enquadramento no inciso específico.]

I.2 — Da tempestividade (art. 675)

    [texto literal do art. 675 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

[Fase de conhecimento:] A sentença no processo principal ainda não transitou em
julgado — embargos tempestivos.

[Fase de execução/cumprimento:] A [adjudicação / alienação / arrematação] ocorreu
em [data]. Os presentes embargos são oferecidos em [data], dentro do prazo de 5
dias e antes da assinatura da respectiva carta.
[VERIFICAR: confirmar que a carta ainda não foi assinada — após a assinatura os
embargos são inadmissíveis.]

II — DO DOMÍNIO / DA POSSE — PROVA SUMÁRIA (art. 677)

    [texto literal do art. 677, caput e §§ aplicáveis via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

O(a) embargante é [proprietário(a) / possuidor(a)] do bem descrito no auto de
[penhora / arresto / apreensão] (doc. [X]), conforme comprovam:
- Doc. [Y]: [ex.: escritura pública de compra e venda de [data] / certidão de
  matrícula atualizada nº ... / contrato de locação / nota fiscal de aquisição]
- Doc. [Z]: [outros documentos de prova sumária]

[Descrever o bem com precisão: matrícula, localização, características físicas.]

[Se cônjuge/companheiro — meação (art. 674, §2º, I):]
O bem constrito é bem [próprio / da meação], não sujeito à dívida do(a)
cônjuge/companheiro(a) devedor(a). O regime de bens é [comunhão parcial / separação]
desde [data do casamento/união], conforme certidão doc. [Z].

[Se adquirente em fraude à execução (art. 674, §2º, II):]
O(a) embargante adquiriu o bem em [data], de boa-fé, antes de qualquer averbação
de constrição ou de fraude à execução nos termos do art. 792 do CPC:

    [texto literal do art. 792 via MCP]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

[Demonstrar: (a) a averbação ou ciência da execução é posterior à aquisição; ou
(b) o bem não estava sujeito a registro e o embargante adotou as cautelas do art.
792, §2º — certidões no domicílio do vendedor.]

III — DO ATO CONSTRITIVO INDEVIDO

O auto de [penhora / arresto / sequestro] lavrado em [data] (doc. [X]) atingiu
indevidamente o bem do(a) embargante. A constrição é incompatível com o domínio/
posse do(a) embargante porque [demonstrar a incompatibilidade].

IV — DO PEDIDO LIMINAR DE SUSPENSÃO DA CONSTRIÇÃO (art. 678)

    [texto literal do art. 678 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

O domínio/a posse está suficientemente comprovado(a) pelos documentos acima.
Requer o(a) embargante a suspensão liminar da constrição sobre o bem [descrever],
evitando alienação ou qualquer ato de expropriação durante o trâmite dos embargos.

V — DOS PEDIDOS

Requer o(a) embargante:
  a) o recebimento dos presentes embargos, com sua distribuição por dependência
     ao processo nº [...] (art. 676 do CPC) e autuação em apartado;
  b) a citação dos embargados na forma do art. 677, §3º — pessoal, se o embargado
     não tiver procurador nos autos principais; ou na pessoa do advogado, se tiver;
  c) liminarmente, a suspensão da constrição sobre o bem [descrever], nos termos
     do art. 678 do CPC;
  d) ao final, o acolhimento dos embargos para, nos termos do art. 681 do CPC:

    [texto literal do art. 681 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

     cancelar o ato de constrição judicial indevida e reconhecer o [domínio /
     manutenção da posse / reintegração definitiva] do bem ao(à) embargante;

  e) a condenação dos embargados nas custas e honorários advocatícios.

Dá-se à causa o valor de R$ [...] [em regra, o valor do bem constrito].

Termos em que pede deferimento.
[Cidade], [data].
```

---

### 3.5.5 — Suspensão de segurança (Lei 12.016/2009 art. 15 + Lei 8.437/1992 art. 4)

> ⚠️ **MEDIDA AUTÔNOMA DO PODER PÚBLICO — NÃO É RECURSO.** A suspensão de segurança é requerimento formulado por **pessoa jurídica de direito público** ou pelo **Ministério Público** diretamente ao **presidente do tribunal** para suspender a execução de liminar ou sentença concessiva de mandado de segurança (Lei 12.016/2009 art. 15) ou de tutela de urgência/sentença em qualquer ação (Lei 8.437/1992 art. 4) que cause **grave lesão à ordem, à saúde, à segurança ou à economia públicas**. Não é recurso — não devolve o mérito ao tribunal. O presidente analisa exclusivamente o risco sistêmico à Administração Pública, não o mérito da decisão impugnada.

**Intake:**
- Quem é o requerente — qual pessoa jurídica de direito público (União, Estado, Município, autarquia) ou Ministério Público?
- Qual é a decisão a suspender — liminar ou sentença em mandado de segurança (→ Lei 12.016 art. 15) ou em outra ação (tutela de urgência, sentença em ação cautelar/civil pública) (→ Lei 8.437 art. 4)?
- Qual é o **tribunal competente** para conhecer do recurso na hipótese — TJ, TRF, STJ ou STF?
- Qual dos quatro fundamentos de grave lesão se aplica: **ordem**, **saúde**, **segurança** ou **economia** públicas? (Pode haver mais de um — demonstrar cada um.)
- Há urgência para pedir efeito suspensivo liminar ao presidente (art. 15, §4º)?
- Já houve pedido de suspensão anterior no tribunal de origem que foi indeferido? (Cabe então novo pedido ao presidente do tribunal superior — art. 15, §1º.)

**Nota crítica — duas bases legais com âmbito diferente:**

| Base legal | Hipótese de aplicação | Corpus MCP |
|---|---|---|
| **Lei 12.016/2009, art. 15** | Liminar ou sentença em **mandado de segurança** | ✅ No corpus |
| **Lei 8.437/1992, art. 4** | Liminar ou sentença em **qualquer outra ação** contra o Poder Público (ação cautelar, tutela de urgência, ACP, ação ordinária) | ❌ [FORA DO CORPUS] |

Usar sempre o artigo correto conforme a natureza da ação em que foi concedida a decisão a suspender. Em caso de dúvida, fundamentar nas duas bases.

**Nota crítica — presidente competente (escalonado):**
- Decisão de 1º grau (liminar de juiz de 1ª instância): pedido ao presidente do TJ/TRF competente para o recurso.
- Indeferido pelo TJ/TRF: novo pedido ao presidente do STJ (se Lei Federal) ou do STF (se questão constitucional) — art. 15, §1º.
- A escalada é automática: cada indeferimento abre a via para o tribunal superior.

**Nota crítica — análise restrita ao risco sistêmico:**
O presidente não reexamina o mérito da decisão impugnada — apenas avalia se a execução da decisão causa grave lesão sistêmica aos bens públicos protegidos. A demonstração do risco deve ser **concreta e documentada**, não genérica. Afirmações vagas como "haverá impacto orçamentário" são insuficientes.

**Nota crítica — jurisprudência:**
Aplicar regra das peças ordinárias (Fonte 2): jurisprudência vedada → `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`.

**Estrutura da peça:**

```
EXCELENTÍSSIMO SENHOR PRESIDENTE DO [TRIBUNAL — TJ / TRF / STJ / STF]

Requerente: [pessoa jurídica de direito público ou Ministério Público]
Processo de origem: [nº do MS ou da ação onde foi concedida a decisão]
Ação de origem: [Mandado de Segurança / Ação Ordinária / Tutela de Urgência / ACP]
Juízo/Órgão de origem: [juiz ou tribunal que concedeu a decisão]

[NOME DO REQUERENTE], por seus procuradores/advogados, vem requerer ao
Excelentíssimo Senhor Presidente a

        SUSPENSÃO DE [LIMINAR / SENTENÇA]

com fundamento no art. 15 da Lei nº 12.016/2009 [e/ou no art. 4º da Lei nº
8.437/1992 — se a ação não for mandado de segurança]:

    [texto literal do art. 15 da Lei 12.016/2009 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/lei/l12016.htm | situação: [situacao] | lei: Lei-12016-2009

[Se a decisão impugnada não é de MS:]
    [FORA DO CORPUS: art. 4º da Lei nº 8.437/1992 — verificar texto atual. Transcrever
    manualmente antes do protocolo. Fundamento: "Para evitar grave lesão à ordem, à saúde,
    à segurança e à economia públicas, o presidente do Tribunal ao qual couber o
    conhecimento do respectivo recurso poderá, a requerimento do Ministério Público ou
    da pessoa jurídica de direito público interessada, e sem prejuízo do disposto no
    art. 5º, nº II, desta Lei, suspender a execução da liminar nas ações movidas contra
    o Poder Público ou seus agentes a que se refere o art. 1º desta Lei" — confirmar
    redação atual.]

pelos fundamentos a seguir.

I — DO CABIMENTO E DA LEGITIMIDADE

O(a) Requerente é [pessoa jurídica de direito público — especificar] / [Ministério
Público], com legitimidade para formular o presente requerimento nos termos do
art. 15, caput, da Lei 12.016/2009 [/ art. 4º da Lei 8.437/1992].

A decisão impugnada é [liminar de [data] / sentença de [data]] proferida no
[Mandado de Segurança / Ação] nº [...], em trâmite perante [o juízo / a turma]
de [órgão de origem].

[Se escalada — art. 15, §1º:] O pedido de suspensão formulado ao presidente do
[tribunal de origem] foi indeferido em [data] (doc. [X]). Nos termos do art. 15,
§1º, da Lei 12.016/2009, cabe novo pedido ao presidente deste [STJ/STF]:

    [texto literal do art. 15, §1º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/lei/l12016.htm | situação: [situacao] | lei: Lei-12016-2009

II — DA DECISÃO IMPUGNADA

[Resumir o conteúdo da liminar/sentença e transcrever literalmente o dispositivo
que determina a obrigação do Poder Público — como Fonte 3 (autos):]

    [Citação literal do dispositivo da decisão impugnada]
    Fonte: [Liminar / Sentença] — [data/ID] — autos nº [número]

III — DA GRAVE LESÃO À [ORDEM / SAÚDE / SEGURANÇA / ECONOMIA] PÚBLICAS

[Este é o núcleo do pedido — demonstrar concretamente o risco sistêmico.
Não é análise do mérito da decisão, mas do impacto de sua execução.]

III.1 — Da grave lesão à ordem pública [omitir se não aplicável]

[Demonstrar que a execução da decisão cria precedente institucional que afeta
o funcionamento regular de serviços públicos, da administração ou da ordem jurídica.
Ex.: decisão que determina liberação de produto proibido pela ANVISA; que suspende
atos administrativos com efeitos sistêmicos. 2-3 parágrafos com dados concretos.]

III.2 — Da grave lesão à economia pública [omitir se não aplicável]

[Demonstrar o impacto financeiro concreto e mensurável. Ex.: valor do impacto
orçamentário, número de contribuintes afetados por extensão da decisão, precedente
que inviabiliza arrecadação. 2-3 parágrafos com dados e documentos — doc. [X].]

III.3 — Da grave lesão à saúde pública [omitir se não aplicável]

[Ex.: decisão que obriga o Estado a fornecer medicamento não aprovado / em
quantidade que excede a capacidade do sistema de saúde. 2-3 parágrafos concretos.]

III.4 — Da grave lesão à segurança pública [omitir se não aplicável]

[Ex.: decisão que interfere em operações policiais, que libera preso perigoso,
que impede ato de controle de fronteiras. 2-3 parágrafos concretos.]

IV — DO PEDIDO LIMINAR (art. 15, §4º — omitir se não houver urgência imediata)

    [texto literal do art. 15, §4º via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/lei/l12016.htm | situação: [situacao] | lei: Lei-12016-2009

A plausibilidade do direito invocado decorre da grave lesão demonstrada no item III.
A urgência reside em [demonstrar: quando a decisão começa a ser executada; qual
o dano irreversível que ocorrerá antes do julgamento do pedido em sessão].

V — DOS PEDIDOS

Requer o(a) [Requerente]:
  a) [se urgência] a concessão de efeito suspensivo liminar ao presente requerimento,
     nos termos do art. 15, §4º, da Lei 12.016/2009, suspendendo desde já a execução
     da [liminar / sentença] impugnada;
  b) o deferimento do pedido de suspensão para suspender, em caráter definitivo até
     o trânsito em julgado da ação de origem, a execução da [liminar / sentença]
     proferida nos autos nº [...];
  c) subsidiariamente, caso V. Exa. entenda insuficiente a documentação, a designação
     de prazo para complementação.

Termos em que pede deferimento.
[Cidade], [data].
```

---

### 3.6 — Módulo subsidiário — situação não coberta por módulo específico

Quando o diagnóstico do Passo 2 identificar a fase processual mas não houver módulo de minuta correspondente, a skill não recusa o trabalho — ela:

1. **Descreve a fase e a peça cabível** com clareza, indicando o fundamento legal (buscar via MCP o que for possível).
2. **Informa ao usuário** que não há módulo específico ainda disponível.
3. **Oferece produzir uma estrutura básica** com intake mínimo, usando os princípios gerais da skill (dispositivos via MCP, sem jurisprudência sem marcador, marcadores nos pontos incertos).
4. **Registra o gap** para que o usuário saiba que a peça gerada é menos estruturada que as produzidas por módulos dedicados.

Resposta padrão quando ativado:

> "Identifiquei que a fase processual é [fase] e que a peça cabível seria [peça], com fundamento no(s) art(s). [X] do [diploma]. Esta skill ainda não tem um módulo dedicado para esse tipo de peça. Posso produzir uma minuta estrutural básica — menos detalhada que as peças com módulo próprio — ou prefere que eu apenas oriente os próximos passos processuais sem redigir o documento?"

---

**Grupo 3.7 — Incidentes processuais**

### 3.7.1 — Suscitação de IRDR — Incidente de Resolução de Demandas Repetitivas (CPC arts. 976-987)

> ⚠️ **INCIDENTE PROCESSUAL — NÃO É RECURSO, NÃO É AÇÃO AUTÔNOMA.** O IRDR é um incidente suscitado perante o tribunal para fixação de tese jurídica vinculante sobre questão unicamente de direito, em contexto de múltiplos processos repetitivos. Não resolve o caso concreto de imediato — fixa a tese que será aplicada a todos os processos pendentes e futuros da área de jurisdição do tribunal. A suscitação é dirigida ao **presidente do tribunal**, não ao relator do processo.

**Intake:**
- Há **efetiva repetição de processos** que contenham controvérsia sobre **mesma questão unicamente de direito** (art. 976, I)? Identificar a questão jurídica com precisão.
- Há **risco de ofensa à isonomia e à segurança jurídica** (art. 976, II) — decisões divergentes sobre a mesma questão?
- **Algum tribunal superior já afetou recurso repetitivo sobre a mesma matéria** (art. 976, §4º)? Se sim, o IRDR é **incabível** — o mecanismo correto é aguardar o julgamento do repetitivo e depois aplicar a tese (ou pedir sobrestamento — ver módulos 3.3.1/3.3.2).
- O requerente é parte no processo, juiz/relator, MP ou Defensoria (art. 977)?
- Há processo específico de origem (caso-piloto) a partir do qual o incidente é suscitado?

**Nota crítica — pressupostos cumulativos (art. 976):**
Ambos os pressupostos são obrigatórios e simultâneos: (i) efetiva repetição (não basta risco potencial — precisa haver processos já em andamento com a mesma questão) e (ii) risco de ofensa à isonomia/segurança jurídica (decisões divergentes ou ausência de orientação uniforme). A inadmissão por falta de pressuposto não impede nova suscitação quando satisfeito (art. 976, §3º).

**Nota crítica — incabível quando tribunal superior já afetou (art. 976, §4º):**
Se o STJ ou o STF já afetou recurso para julgamento de tese repetitiva sobre a mesma matéria, o IRDR **não pode ser instaurado**. Verificar o sistema de consulta de recursos repetitivos do STJ/STF antes de suscitar o incidente. Se a tese já está no STJ/STF, requerer sobrestamento do processo (módulos 3.3.1 ou 3.3.2) em vez de suscitar IRDR.

**Nota crítica — sem custas (art. 976, §5º):**
O IRDR não exige preparo ou recolhimento de custas processuais.

**Nota crítica — efeitos após a admissão (arts. 980 e 982):**
Admitido o incidente pelo tribunal, o relator **suspende todos os processos** pendentes na área de jurisdição do tribunal (art. 982, I). O julgamento tem preferência e prazo de **1 ano** — superado esse prazo, cessa a suspensão, salvo decisão fundamentada do relator (art. 980, par. único). A parte pode pedir tutela de urgência ao juízo de origem durante a suspensão (art. 982, §2º).

**Nota crítica — eficácia vinculante da tese (art. 985):**
A tese fixada se aplica a todos os processos individuais ou coletivos da área de jurisdição do tribunal, inclusive futuros e nos juizados especiais. O descumprimento da tese admite **reclamação** (art. 985, §1º).

**Nota crítica — recurso do julgamento do IRDR (art. 987):**
Do julgamento do mérito do IRDR cabe RE ou REsp, conforme a natureza da questão. O recurso tem efeito suspensivo e a repercussão geral é presumida (art. 987, §1º). Se o STF/STJ apreciar o mérito, a tese se aplica no território nacional (art. 987, §2º).

**Nota crítica — jurisprudência:**
Aplicar regra das peças ordinárias (Fonte 2): vedada. Se houver divergência entre turmas do próprio tribunal (elemento do pressuposto II), citar as decisões com marcador:
`[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, órgão, data e tese antes do protocolo]`

**Estrutura da peça:**

```
EXCELENTÍSSIMO SENHOR PRESIDENTE DO
[TRIBUNAL DE JUSTIÇA DO ESTADO DE [UF] / TRIBUNAL REGIONAL FEDERAL DA [Nª] REGIÃO]

Processo de origem nº [...] — [Vara / Câmara / Turma de origem]
Requerente: [parte / Ministério Público / Defensoria Pública]

[NOME DO REQUERENTE], [qualificação], por seu(sua) advogado(a) / representante
legal, vem, nos termos do art. 977, inciso [II / III], do Código de Processo Civil,
requerer a instauração do

   INCIDENTE DE RESOLUÇÃO DE DEMANDAS REPETITIVAS — IRDR

com fundamento nos arts. 976 a 987 do CPC, pelos fundamentos a seguir.

I — DO CABIMENTO — DOS PRESSUPOSTOS (art. 976)

    [texto literal do art. 976, incisos I e II, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

I.1 — Da efetiva repetição de processos (art. 976, I)

A questão de direito objeto deste incidente é:

> [Formular a questão jurídica com precisão, em uma frase ou parágrafo curto.
> Ex.: "Se o prazo do art. X da Lei Y tem natureza decadencial ou prescricional
> para fins de [consequência]." — A formulação deve ser objetiva e replicável.]

Há efetiva repetição de processos que versam sobre essa questão nos seguintes
casos (amostra representativa):

- Processo nº [A] — [Vara/Câmara] — [breve descrição do ponto controvertido]
- Processo nº [B] — [Vara/Câmara] — idem
- Processo nº [C] — [Vara/Câmara] — idem
[VERIFICAR: juntar ao menos 3-5 processos identificados como doc. [X]. O pedido
deve ser instruído com os documentos necessários — art. 977, par. único.]

I.2 — Do risco de ofensa à isonomia e à segurança jurídica (art. 976, II)

Sobre a mesma questão, já se identificam decisões divergentes no âmbito deste
tribunal:

[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, órgão, data e tese antes do protocolo]:
- [Nª Câmara / Turma]: decidiu que [tese A]. [Processo nº / Acórdão].
- [Nª Câmara / Turma]: decidiu que [tese B, divergente]. [Processo nº / Acórdão].
Fonte: [pesquisa web / sistema do tribunal — URL ou "verificar manualmente"]

[Se não há divergência ainda, mas o risco é iminente:]
A questão é recorrente e está presente em [N] processos sem orientação uniforme,
gerando risco concreto de decisões contraditórias.

I.3 — Da inexistência de afetação em tribunal superior (art. 976, §4º)

[VERIFICAR: confirmar nos sistemas do STJ e STF que não há recurso afetado para
julgamento de tese repetitiva sobre a mesma questão. Se houver, o IRDR é incabível.]
Até a data desta suscitação, não foi identificada afetação de recurso repetitivo
sobre a questão nos tribunais superiores.

II — DA QUESTÃO DE DIREITO — FUNDAMENTO JURÍDICO

[Desenvolver a questão jurídica a ser fixada. Buscar via MCP os dispositivos
legais pertinentes:]

    [texto literal do dispositivo legal controverso via MCP]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[Explicar a controvérsia: quais interpretações divergentes estão em disputa;
qual é a tese que o requerente sustenta como correta; por que a tese correta
é a que o requerente defende. 3-5 parágrafos.]

III — DA LEGITIMIDADE (art. 977)

    [texto literal do art. 977 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

O(a) requerente é [parte no processo nº [...] / Ministério Público / Defensoria
Pública], com legitimidade para suscitar o IRDR nos termos do art. 977, inciso
[II / III], do CPC.

IV — DA SUSPENSÃO DOS PROCESSOS E DAS TUTELAS DE URGÊNCIA (arts. 980 e 982)

Admitido o incidente, requer o(a) requerente que o relator suspenda os processos
pendentes que versem sobre a mesma questão na área de jurisdição deste tribunal,
nos termos do art. 982, I, do CPC:

    [texto literal do art. 982, inciso I, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

O julgamento deverá ocorrer no prazo de 1 ano (art. 980):

    [texto literal do art. 980 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

V — DA TESE JURÍDICA A SER FIXADA

O(a) requerente propõe que o tribunal fixe a seguinte tese jurídica:

> "[Formular a tese em termos abstratos, aplicável a todos os casos futuros.
> Ex.: 'O prazo do art. X da Lei Y é decadencial, iniciando-se em [marco temporal],
> sendo inaplicável qualquer causa de interrupção ou suspensão.']"

A adoção dessa tese promoverá a isonomia e a segurança jurídica nos termos do
art. 985 do CPC:

    [texto literal do art. 985 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | situação: [situacao] | lei: Lei-13105-2015

VI — DOS PEDIDOS

Requer o(a) requerente:
  a) a instauração do Incidente de Resolução de Demandas Repetitivas, nos termos
     dos arts. 976-987 do CPC;
  b) admitido o incidente, a suspensão dos processos pendentes na área de jurisdição
     deste Tribunal que versem sobre a mesma questão (art. 982, I);
  c) o julgamento do mérito do incidente com a fixação da seguinte tese jurídica
     vinculante: "[tese proposta]";
  d) após o julgamento, a aplicação da tese a todos os processos individuais e
     coletivos na área de jurisdição deste tribunal, inclusive nos juizados especiais
     (art. 985, I e II).

Instrui este pedido com os documentos necessários à demonstração dos pressupostos
(art. 977, par. único): docs. [X] a [Z].

Termos em que pede deferimento.
[Cidade], [data].
```

## Passo 4 — Pesquisa legal (MCP)

Para cada dispositivo identificado no diagnóstico e na estrutura:

1. Identifique a norma (CPC, CLT, CC, lei especial).
2. Chame `buscar_artigos` com query precisa + `norma`.
3. Registre o bloco completo no formato padrão de citação.
4. Norma fora do corpus → `[FORA DO CORPUS]`.

**Prioridades de busca por tipo de peça:**

| Peça | Dispositivos essenciais | norma (sigla/slug) |
|---|---|---|
| Réplica | arts. 350, 351, 435 | Lei-13105-2015 |
| Tutela antecipada antecedente | arts. 303 (caput e §§1º-6º), 304 (estabilização) | Lei-13105-2015 |
| Tutela cautelar antecedente | arts. 305, 306, 307, 308, 309, 310 | Lei-13105-2015 |
| Apelação | arts. 1.009, 1.010, 1.012, 1.003 §5º, 85 §11 | Lei-13105-2015 |
| Agravo de instrumento | art. 1.015 (inciso específico), 1.016-1.020 | Lei-13105-2015 |
| Embargos de declaração | arts. 1.022, 1.023, 1.024 | Lei-13105-2015 |
| Cumprimento (quantia) | arts. 523, 523 §1º, 835 | Lei-13105-2015 |
| Cumprimento (obrigação) | arts. 536, 537 | Lei-13105-2015 |
| Impugnação ao cumprimento de sentença | arts. 525 (caput e §§1º, 4º, 5º, 6º, 12-14) | Lei-13105-2015 |
| Embargos à execução | arts. 914 (caput e §§1º-2º), 915 (caput e §§1º-3º), 917 (caput e §§1º-7º), 919 (caput e §§1º-5º) | Lei-13105-2015 |
| Exceção de pré-executividade | art. 803 (caput e par. único — base normativa mais próxima), art. 924 (extinção da execução); dispositivo de prescrição/decadência aplicável à obrigação via MCP; cabimento é pretoriano — marcador obrigatório | Lei-13105-2015 + lei especial da obrigação |
| Embargos de terceiro | arts. 674 (caput e §§1º-2º), 675 (caput e par. único), 676, 677 (caput e §§1º-4º), 678 (caput e par. único), 679, 681; art. 792 se fraude à execução | Lei-13105-2015 |
| Recurso ordinário trabalhista | CLT arts. 895, 899 | DL-5452-1943 |
| Recurso inominado JEC | Lei 9.099 arts. 41, 42 | [verificar norma — provável Lei-9099-1995] |
| Recurso Extraordinário | CF art. 102 III "a"; CPC arts. 1.029, 1.003 §5º, 1.035, 1.037; dispositivos constitucionais violados; art. 1.031 se simultâneo com REsp | CF-1988 + Lei-13105-2015 |
| Recurso Especial | CF art. 105 III; CPC arts. 1.029, 1.003 §5º, 1.032, 85 §11; dispositivos de lei federal violados; art. 1.031 se simultâneo com RE | CF-1988 + Lei-13105-2015 |
| Agravo em RE / Agravo em REsp | CPC arts. 1.042, 1.030 V, 1.003 §5º | Lei-13105-2015 |
| Embargos de divergência | CPC arts. 1.043 (caput e §§1º-5º), 1.044 (caput e §§1º-2º); dispositivo legal/constitucional da questão de fundo via MCP; acórdão paradigma com `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP]` | Lei-13105-2015 |
| Agravo Interno | CPC arts. 1.021, 1.021 §2º; se hipótese 2: também art. 1.030 §2º | Lei-13105-2015 |
| Recurso Ordinário Constitucional | CF art. 102 II ou 105 II; CPC arts. 1.027, 1.028; prazo: 15 dias úteis (art. 1.003 §5º) na regra geral, inclusive HC ao STF (102 II "a"); 5 dias (Lei 8.038 art. 30 — `[VERIFICAR/FORA DO CORPUS]`) só no HC ao STJ (105 II "a"); dispositivo legal violado | CF-1988 + Lei-13105-2015 |
| Reclamação constitucional | CPC arts. 988 (caput, inciso e §§4º/5º), 989, 992 | Lei-13105-2015 |
| Ação Rescisória | CPC arts. 966 (inciso e §§1º/5º/6º), 967, 968 (I, II, §§1º/2º), 969, 970, 975 (caput e §§1º/2º/3º) | Lei-13105-2015 |
| Oposição | CPC arts. 682, 683 (caput e par. único), 684, 685 (caput e par. único), 686 | Lei-13105-2015 |
| Suspensão de segurança | Lei 12.016/2009 art. 15 (caput e §§1º-5º) no corpus; Lei 8.437/1992 art. 4 [FORA DO CORPUS — transcrever manualmente] | Lei-12016-2009 |
| Suscitação de IRDR | CPC arts. 976 (caput e §§1º-5º), 977 (caput e par. único), 978, 980 (caput e par. único), 982 (caput e §§1º-5º), 985 (caput e §§1º-2º), 987 (caput e §§1º-2º); dispositivo legal controvertido via MCP | Lei-13105-2015 |

**Sem suplementação silenciosa.** MCP retornou pouco/nada → pergunte ao usuário antes de buscar em outro lugar.

## Passo 5 — Conferências obrigatórias antes da entrega

1. **Diagnóstico confirmado.** O tipo de peça foi confirmado pelo usuário antes de redigir?
2. **Prazo buscado via MCP.** O prazo aplicável foi verificado com o texto literal da lei (não de memória)? O texto está nas notas?
3. **Cabimento verificado.** Para agravo: o inciso do art. 1.015 está explícito? Para recurso ordinário trabalhista: o prazo é de 8 dias corridos (não úteis)?
4. **Auditoria de MCP — obrigatória.** Para cada dispositivo citado na peça, o bloco `citacao / source_url` está presente? Citação sem esses campos = foi de memória = **inválida**. Remova ou converta em `[CITAÇÃO PENDENTE]`.
5. **Auditoria de jurisprudência — obrigatória.** Há alguma súmula, acórdão, REsp, RE, OJ ou qualquer referência a decisão judicial na peça?
   - **Peças ordinárias:** Se sim, remova imediatamente e substitua por `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`.
   - **Recurso Extraordinário:** Toda jurisprudência deve estar marcada com `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]`. Se houver referência a precedente **sem esse marcador**, adicione imediatamente. Referências a Temas de Repercussão Geral sem marcador = falha grave.
6. **Marcadores remanescentes.** `[VERIFICAR]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS]`, `[JURISPRUDÊNCIA]`, `[DOC. A NUMERAR]` — todos listados no bloco de notas?
7. **Depósito recursal (trabalhista).** Se empregador recorrente, o depósito foi mencionado e o valor marcado como `[FORA DO CORPUS]`?

## Formatação padrão do documento

Todo o texto da peça — cabeçalho, qualificações, fatos, fundamentos, pedidos — deve estar em **alinhamento justificado**. Não há exceção para nenhuma seção. A citação de lei segue as regras próprias da seção "Regra absoluta" (recuada, justificada, fonte menor), mas o restante do documento também é justificado — não alinhado à esquerda.

No .docx, isso equivale a `AlignmentType.JUSTIFIED` (docx-js) em todos os parágrafos.

## Passo 6 — Output

Salve dois arquivos:

- `outputs/[tipo-peça]-[slug]-[YYYY-MM-DD].docx`
  - Tipos de prefixo: `replica`, `tutela-antecipada-antecedente`, `tutela-cautelar-antecedente`, `apelacao`, `agravo-instrumento`, `embargos-declaracao`, `cumprimento-sentenca`, `impugnacao-cumprimento`, `embargos-execucao`, `excecao-pre-executividade`, `embargos-terceiro`, `recurso-ordinario-trt`, `recurso-inominado-jec`, `recurso-extraordinario`, `recurso-especial`, `agravo-are`, `agravo-aresp`, `agravo-interno`, `recurso-ordinario-constitucional`, `embargos-divergencia`, `reclamacao`, `acao-rescisoria`, `oposicao`, `suspensao-seguranca`, `suscitacao-irdr`
- `outputs/[tipo-peça]-[slug]-NOTAS.md`

**Marcadores em vermelho — obrigatório.** Após gerar o `.docx`, execute o script `colorir_marcadores.py` para aplicar cor vermelha e negrito a todos os marcadores inline:

```bash
python scripts/colorir_marcadores.py outputs/[tipo-peça]-[slug]-[YYYY-MM-DD].docx
```

O script sobrescreve o arquivo no mesmo caminho. Se o script não estiver disponível, aplique manualmente cor `#FF0000` a cada ocorrência de `[VERIFICAR...]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS...]`, `[JURISPRUDÊNCIA...]`, `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP...]` e `[DOC. A NUMERAR]`.

**Aviso obrigatório ao usuário — incluir sempre após entregar a minuta:**

> ⚠️ **ITENS EM VERMELHO — VERIFICAÇÃO NECESSÁRIA ANTES DO PROTOCOLO**
> Os trechos marcados em vermelho no documento indicam pontos que precisam ser resolvidos pelo(a) advogado(a) antes de assinar e protocolar a peça. Revise cada marcador:
> - `[VERIFICAR: ...]` — dado não confirmado, presumido ou ausente
> - `[CITAÇÃO PENDENTE]` — artigo não localizado via MCP; incluir manualmente com fonte verificada
> - `[FORA DO CORPUS]` — norma estadual, municipal ou tabela do tribunal; verificar na fonte local
> - `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]` — espaço reservado para súmula ou julgado (peças ordinárias)
> - `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]` — precedente citado no corpo do RE que precisa ser conferido pelo(a) advogado(a) antes do protocolo
> - `[DOC. A NUMERAR]` — documento referenciado sem número; numerar ao juntar
>
> Nenhum desses marcadores pode permanecer na peça no momento do protocolo.

```
## Notas de revisão — [Tipo de Peça] — [data]

**Skill:** analise-processual-minuta (Letra da Lei)
**Fase diagnosticada:** [fase]
**Peça produzida:** [tipo]
**Fonte da legislação:** MCP Letra da Lei (texto verbatim do Planalto)

### Prazo
- Prazo legal: [N] dias [úteis/corridos] (art. [X] do [diploma])
  Fonte MCP: [citacao] | [source_url]
- Data de publicação/intimação: [data]
- Data-limite estimada: [VERIFICAR — confirmar no sistema do tribunal,
  considerando feriados forenses e suspensões locais — fora do corpus desta skill]

### Marcadores inline a resolver
- `[VERIFICAR: ...]` — N ocorrências
- `[CITAÇÃO PENDENTE]` — N
- `[FORA DO CORPUS]` — N (norma estadual/infralegal/tabela do tribunal)
- `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]` — N (peças ordinárias)
- `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]` — N (RE/reclamação/rescisória)
- `[DOC. A NUMERAR]` — N

### Dispositivos citados (todos verificados via MCP)
- [lei_slug]-[Art-N] — [source_url]
- ...

### Pontos abertos para a(o) advogado(a)
- [premissas assumidas que merecem confirmação]
- [decisões estratégicas que a skill não pode tomar]
- [depósito recursal, preparo, custas — verificar tabelas locais]

### O que esta skill NÃO fez
- Não calculou o prazo final no sistema do tribunal — feriados forenses locais
  são [FORA DO CORPUS].
- Não inseriu jurisprudência — espaços marcados `[JURISPRUDÊNCIA]` precisam
  ser preenchidos pelo(a) advogado(a).
- Não confirmou o valor do depósito recursal (trabalhista) — consultar tabela
  vigente do TST.
- Não protocolou nada.
```

## O que esta skill NÃO faz

- **Não protocola.** Nunca. Protocolar é ato privativo de advogado(a) habilitado(a).
- **Não calcula prazo final.** Devolve o texto legal do prazo (via MCP) e os marcos. A contagem exata no PJe/eSAJ — com feriados forenses locais, recesso (CPC art. 220), suspensões — é do(a) advogado(a).
- **Não confirma cabimento de agravo sem consultar o art. 1.015 via MCP.** O rol é taxativo; a skill verifica o inciso antes de afirmar que cabe agravo.
- **Não insere jurisprudência sem marcador.** Em peças ordinárias, jurisprudência é vedada e sai como `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`. No Recurso Extraordinário, precedentes do STF podem entrar no corpo da peça, mas sempre marcados com `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]`. Nenhum precedente entra limpo — sem marcador — em nenhuma peça.
- **Não cobre normas estaduais ou tabelamentos do tribunal.** Custas, depósito recursal, tabela de honorários periciais — `[FORA DO CORPUS]`.
- **Não decide estratégia.** "Apelar ou embargar primeiro?" é decisão profissional. A skill produz a peça que o(a) advogado(a) escolheu.
- **Não substitui o(a) advogado(a).** Produz rascunho — assinatura, responsabilidade e estratégia são da pessoa habilitada na OAB.
