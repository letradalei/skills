---
name: peticao
description: Redige petição inicial brasileira (CPC art. 319) com fundamentação verificada. Use para "redige uma inicial", "vou ajuizar [ação]", "monta a inicial", "preciso entrar com [ação]", ou qualquer peça inaugural cível, trabalhista, do consumidor, juizado, família ou mandado de segurança. Não use para contestação, recurso ou defesa.
argument-hint: "[tipo de ação ou descrição curta, ex.: 'indenizatória por dano moral']"
compatibility: "Requer python-docx (pip install python-docx) para colorir os marcadores de revisão no .docx gerado."
metadata:
  version: "0.3.0"
---

# Petição Inicial

A inicial abre o processo, e tudo que vem depois é moldado por ela: fato não narrado não vira causa de pedir; pedido não formulado não pode ser concedido (CPC art. 141 e 492). Esta skill produz um **rascunho com fundamentação verificada dispositivo por dispositivo contra o texto vigente** — não uma peça pronta. Quem assina, decide a estratégia e protocola é a pessoa habilitada na OAB.

## Contratos compartilhados (leia antes de redigir)

Esta peça segue contratos comuns às skills de redação. Carregue-os conforme a etapa:
- **`letradalei:pesquisa`** — como buscar e verificar lei e jurisprudência no MCP (ferramentas, parâmetros, vigência, texto integral). Nenhuma citação vem de memória.
- **`../_shared/intake.md`** — disciplina de entrevista (em blocos de até 4 perguntas/rodada), o protocolo "Informar manualmente" e o fallback não-interativo. Não redija antes de completar o intake.
- **`../_shared/citacao-e-formato.md`** — como uma fonte verificada entra na peça e como o bloco de citação é formatado no `.docx`.
- **`../_shared/saida.md`** — arquivos de saída, marcadores em vermelho e bloco de notas.

Em uma frase: **pesquise no MCP, verifique a vigência, cite no formato padrão; o que não for verificável vira marcador**, nunca texto inventado.

## Fluxo

1. **Intake** (`../_shared/intake.md` + Passo 1): partes, fatos, pedido, juízo, rito.
2. **Pesquisa** (`letradalei:pesquisa`): busque no MCP cada dispositivo que entrará na peça. Memória do modelo não cita artigo.
3. **Precedentes vinculantes** (Passo 2.1): mapeie repercussão geral (STF) e repetitivos (STJ) que afetem as teses centrais.
4. **Estrutura** (Passo 3): monte na forma do CPC art. 319.
5. **Conferência** (Passo 4) e **saída** (`../_shared/saida.md`): `.docx` em `outputs/peticao-[slug]-[data].docx` + `NOTAS.md`.

## Passo 1, Intake (perguntas específicas da inicial)

Siga o protocolo de `../_shared/intake.md`. As perguntas próprias desta peça:

### 1.1 Partes
- **Autor(a/es):** nome, nacionalidade, estado civil, profissão, CPF/CNPJ, endereço, e-mail (CPC art. 319, II).
- **Réu(s):** mesmos dados; se desconhecidos, declarar (art. 319, § 1º) e indicar como serão buscados.
- Há litisconsórcio? Necessário ou facultativo? Ativo ou passivo?

### 1.2 Causa de pedir e fatos
- Narrativa cronológica (causa de pedir remota e próxima).
- Documento que comprova cada fato — peça ao usuário listar/anexar.
- Há prova testemunhal? Pericial? Documento eletrônico?

### 1.3 Pedido
- Principal, certo e determinado (CPC art. 322 e 324).
- Sucessivos, subsidiários, alternativos, cumulados?
- Tutela de urgência/evidência (art. 300 e ss.)? Se sim: probabilidade do direito + perigo de dano + reversibilidade.
- Pedido genérico (art. 324, § 1º) só nas hipóteses do artigo; justificar.

### 1.4 Juízo competente e rito
- Competência: territorial, matéria, pessoa, valor (busque arts. 42 a 53 do CPC se necessário).
- Rito: comum, JEC (Lei 9.099/1995), juizado da Fazenda Pública, procedimento especial.
- Valor da causa (art. 291 a 293).

### 1.5 Regime aplicável (conferência rápida)
- **Relação de consumo** → busque no CDC (`Lei-8078-1990`).
- **Trabalhista** → CLT (`DL-5452-1943`).
- **Família** → Código Civil (`Lei-10406-2002`) + Estatuto do Idoso/ECA/Lei Maria da Penha conforme o caso.
- Não decida o regime sem conferir a lei.

### 1.6 Dados obrigatórios por regime (Rodada 2)
- **Gratuidade de justiça:** se o(a) autor(a) é **pessoa física**, pergunte sempre (mesmo sem o usuário mencionar). Se sim → pedido expresso (CPC art. 99) + orientar declaração de hipossuficiência. Pessoa jurídica: só se houver indício de dificuldade declarado.
- **Se trabalhista:** **remuneração mensal bruta** (essencial para FGTS = 8% × remuneração × meses, férias, 13º, aviso prévio). Sem o valor, os pedidos pecuniários ficam `[VERIFICAR: calcular]`. Cabeçalho: `___ª VARA DO TRABALHO DE [COMARCA]` com o número em branco é lacuna normal na inicial (não marque em vermelho).
- **Se consumidor:** valor do dano material, se houver (compõe o valor da causa, art. 292, V).
- **Se família com menor:** confirmar filhos menores (define via judicial e intervenção do MP).

## Passo 2, Pesquisa legal

Para **cada tese** que sustenta um pedido, siga `letradalei:pesquisa`: identifique a norma matriz (CC, CDC, CLT, CPC, lei especial), busque o dispositivo, verifique `situacao`, e registre o bloco de citação no formato de `../_shared/citacao-e-formato.md`. Tese que depende de norma fora do acervo → `[FORA DO CORPUS]`.

## Passo 2.1, Precedentes vinculantes (repercussão geral e repetitivos)

Execute após o Passo 2, antes de redigir. Um tema vinculante pode determinar o desfecho — ou suspender o processo. Para cada tese central:

1. `jurisprudencia-federal · buscar_vinculantes` com a tese em linguagem natural; filtre por `autoridade: "STF"` (repercussão geral) ou `"STJ"` (repetitivos).
2. IRDRs estaduais relevantes: `jurisprudencia-estadual · buscar_vinculantes` com `localidade` = UF do juízo.
3. Insira o precedente pertinente na seção "Do Direito" (formato de jurisprudência do contrato de citação; `eficacia: vinculante` dispensa marcador).

Casos especiais:
- **Tema pendente:** `[ATENÇÃO, TEMA PENDENTE: processos sobre esta matéria podem estar suspensos ou sujeitos a modulação. Verificar impacto antes de ajuizar.]`
- **Sem resultado pertinente:** `[JURISPRUDÊNCIA, busca de vinculantes feita via MCP sem resultado direto para esta tese. Verificar manualmente.]` — não omita em silêncio: o(a) advogado(a) precisa saber que a busca foi feita.
- O MCP cobre STF/STJ/TST/CARF e IRDRs dos TJs. Precedentes de TRTs e outros tribunais → `[FORA DO CORPUS, verificar precedentes do tribunal local]`. A skill não avalia se o tema é favorável — isso é do(a) advogado(a).

## Passo 3, Estrutura da peça (CPC art. 319)

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [...] VARA [CÍVEL / DA
FAMÍLIA / DO JUIZADO ESPECIAL CÍVEL / DA FAZENDA PÚBLICA / DO TRABALHO] DA COMARCA
DE [...]

                                                          [Distribuição por dependência? Sim/Não]
                                                          [Valor da causa: R$ ...]

[NOME DO AUTOR], [qualificação completa, art. 319, II], por seu(sua) advogado(a)
infra-assinado(a) (procuração anexa, doc. 01), vem, respeitosamente, à presença
de Vossa Excelência propor a presente

                AÇÃO [denominação, ex.: DE INDENIZAÇÃO POR DANOS MORAIS]

em face de [NOME DO RÉU], [qualificação completa], pelos fatos e fundamentos a
seguir expostos.

I, DOS FATOS

[Narrativa cronológica, factual, sem argumentação jurídica aqui. Cada fato com
referência ao doc. que o comprova: "(doc. nº)", não inventar números de doc se
o usuário não forneceu; marcar `[DOC. A NUMERAR]`.]

II, DO DIREITO

[Fundamentos jurídicos do pedido, art. 319, III. CADA dispositivo citado abaixo
deve ter sido retornado pelo MCP. Estrutura sugerida:]

II.1, [Instituto / tese 1, ex.: Da responsabilidade civil do fornecedor]

Dispõe o art. 14 do Código de Defesa do Consumidor (Lei nº 8.078/1990):

    [bloco de citação — ver ../_shared/citacao-e-formato.md]

[Aplicação ao caso concreto, subsunção. 2-4 parágrafos.]

II.2, [tese 2], mesma estrutura

[...]

III, DA TUTELA DE URGÊNCIA  (se aplicável)

[Texto introdutório.]

    [bloco de citação do art. 300, via MCP]

[Demonstrar probabilidade do direito + perigo de dano + reversibilidade.]

IV, DOS PEDIDOS

Diante do exposto, requer:

  a) [pedido principal, certo e determinado, art. 322 do CPC];
  b) a citação do(s/a/as) réu(s/ré/és) para, querendo, oferecer contestação no
     prazo legal, sob pena de revelia;
  c) a produção de todas as provas em direito admitidas, especialmente
     [documental / testemunhal / pericial / depoimento pessoal] (art. 319, VI);
  d) [pedidos acessórios, honorários (art. 85), custas, juros, correção];
  e) [tutela / liminar, se houver, repetir o pedido específico].

V, DO VALOR DA CAUSA

Atribui-se à causa o valor de R$ [...] (art. 291 do CPC), [critério, ex.:
"correspondente ao pedido econômico nos termos do art. 292, V"].

VI, DA OPÇÃO PELA AUDIÊNCIA DE CONCILIAÇÃO  (art. 319, VII)

[X] Tem interesse na realização de audiência de conciliação/mediação.
[ ] Não tem interesse.

Termos em que,
Pede deferimento.

[Cidade], [data].

_______________________________________
[NOME DA(O) ADVOGADA(O)]
OAB/[UF] nº [...]
```

## Passo 4, Conferências antes da entrega

Rode esta checklist e reporte cada item (as auditorias de citação seguem `../_shared/citacao-e-formato.md`):

1. **CPC art. 319** — os 7 incisos atendidos? (sim/não/N/A para cada).
2. **Pedido certo e determinado** (art. 322 e 324); se genérico, justificado pelo art. 324, § 1º?
3. **Congruência** (art. 141 e 492): o fato narrado sustenta cada pedido?
4. **Valor da causa** calculado conforme art. 291 a 293?
5. **Documentos essenciais** (art. 320): procuração, comprovantes do fato constitutivo, título se executiva.
6. **Competência** verificada via MCP, não de memória?
7. **Tutela de urgência** (se houver): probabilidade + perigo + reversibilidade demonstrados?
8. **Pedido de citação** consta? (erro frequente.)
9. **Gratuidade** — se pessoa física, pedido feito ou ausência registrada como `[VERIFICAR]`?
10. **Auditoria de citação** — todo dispositivo tem `citacao` + `source_url`? Toda jurisprudência tem `search_id` + `eficacia`? Sem isso = de memória = inválida; remover ou converter em marcador.
11. **Prescrição trabalhista** (se CLT): regra do art. 11 (busque, `DL-5452-1943`) — 5 anos na vigência do contrato, **limite de 2 anos após a extinção**. Compare a data de término com hoje; se o biênio expirou ou está a < 30 dias, alerta em vermelho no topo + nas notas, com instrução de não protocolar sem análise. Exceção: anotação na CTPS para fins previdenciários não prescreve (art. 11, § 1º).
12. **Marcadores remanescentes** listados no `NOTAS.md`.

## Passo 5, Saída

Siga `../_shared/saida.md` com `<tipo> = peticao`: monte o `.docx` com os utilitários de `montar_docx.py`, salve `outputs/peticao-[slug]-[data].docx` + `outputs/peticao-[slug]-NOTAS.md`, rode `colorir_marcadores.py` e inclua o aviso de itens em vermelho.

## O que esta skill NÃO faz

- **Não protocola.** Ato privativo de advogado(a) habilitado(a) (Lei 8.906/1994), com assinatura digital no PJe/eSAJ/Projudi.
- **Não insere jurisprudência não verificada.** O que não vier do MCP fica `[JURISPRUDÊNCIA, a ser inserida pelo(a) advogado(a)]`.
- **Não pesquisa norma estadual, municipal ou infralegal** → `[FORA DO CORPUS]`.
- **Não inventa fatos.** Só o que o usuário forneceu; lacuna vira `[VERIFICAR]`.
- **Não substitui o(a) advogado(a).** Produz rascunho; estratégia, ajuste e assinatura são da pessoa habilitada.
