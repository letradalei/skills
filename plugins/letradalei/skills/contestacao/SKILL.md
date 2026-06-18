---
name: contestacao
description: Redige contestação cível brasileira (CPC arts. 335–342), preliminares (art. 337), mérito com impugnação especificada e eventual reconvenção, fundamentada. Use para "redige uma contestação", "preciso contestar", "fui citado, monta a defesa", "resposta à inicial". Não use para recurso, embargos ou peças posteriores à fase postulatória.
argument-hint: "[descrição curta, ex.: 'contestação em ação de cobrança' ou caminho do PDF da inicial]"
compatibility: "Requer python-docx (pip install python-docx) para colorir os marcadores de revisão no .docx gerado."
metadata:
  version: "0.3.0"
---

# Contestação

A contestação concentra toda a defesa (princípio da eventualidade, CPC art. 336): o que não for alegado aqui está, em regra, precluso, e os fatos não impugnados especificamente presumem-se verdadeiros (art. 341). Daí uma assimetria perigosa em relação à inicial — a falha na inicial costuma ser sanável; a falha na contestação, em regra, não. Esta skill produz um **rascunho com fundamentação verificada artigo por artigo**; a estratégia (qual preliminar primeiro, qual fato silenciar, reconvenção vs. pedido contraposto) é do(a) advogado(a).

## Contratos compartilhados (leia antes de redigir)

Esta peça segue contratos comuns às skills de redação. Carregue-os conforme a etapa:
- **`letradalei:pesquisa`** — como buscar e verificar lei e jurisprudência no MCP (ferramentas, parâmetros, vigência, texto integral). Nenhuma citação vem de memória.
- **`../_shared/intake.md`** — disciplina de entrevista (em blocos de até 4 perguntas/rodada), o protocolo "Informar manualmente" e o fallback não-interativo. Não redija antes de completar o intake.
- **`../_shared/citacao-e-formato.md`** — como uma fonte verificada entra na peça e como o bloco de citação é formatado no `.docx`.
- **`../_shared/saida.md`** — arquivos de saída, montagem do `.docx`, marcadores em vermelho e bloco de notas.

Em uma frase: **pesquise no MCP, verifique a vigência, cite no formato padrão; o que não for verificável vira marcador**, nunca texto inventado. Contestação com dispositivo errado destrói a defesa: o juízo vê que o artigo não existe ou diz outra coisa, e a tese morre.

## Fluxo

1. **Leia a inicial** (Passo 1) — sem ela não há contestação útil, só formalismo.
2. **Intake defensivo** (`../_shared/intake.md` + Passo 2): versão do réu, documentos, preliminares, mérito, reconvenção, provas.
3. **Pesquisa** (`letradalei:pesquisa`): busque cada dispositivo invocado. As 13 preliminares do art. 337 exigem a redação literal do inciso.
4. **Estrutura** (Passo 4): preliminares → mérito → reconvenção → provas → pedidos.
5. **Conferência** (Passo 5) e **saída** (`../_shared/saida.md`): `.docx` em `outputs/contestacao-[slug]-[data].docx` + `NOTAS.md`.

## Passo 1, Ler a inicial

**Pré-requisito não-negociável.** Sem a inicial em mãos, peça:

> "Para redigir a contestação preciso da petição inicial. Você pode (a) colar o texto, (b) anexar o PDF/DOCX, ou (c) descrever os pedidos, a causa de pedir e os documentos mencionados. Sem isso, qualquer contestação que eu produzir será genérica e provavelmente inútil."

Da inicial, extraia (e devolva ao usuário para confirmação antes de prosseguir):

- **Partes**, autor(a), réu(s), litisconsórcio.
- **Pedidos**, listados por letra/numeração, com valor de cada um.
- **Causa de pedir**, fatos narrados + fundamentos invocados.
- **Documentos juntados**, lista pelos `(doc. nº)`.
- **Tutela de urgência**, pedida? deferida?
- **Audiência de conciliação**, designada? data?
- **Rito**, comum, juizado, especial?
- **Data da juntada do AR ou do mandado** (CPC art. 335, III), para conferir prazo.

## Passo 2, Intake defensivo

Siga o protocolo de `../_shared/intake.md`. As perguntas próprias da defesa:

### 2.1 Versão da(o) ré(u)
- O que de fato aconteceu, na visão do(a) ré(u)? Onde diverge da narrativa do autor?
- Que documentos comprovam a versão da(o) ré(u)? (Pedir a juntar.)
- Há comunicações (e-mails, mensagens, atas) entre as partes que mudem a interpretação?

### 2.2 Preliminares possíveis (CPC art. 337)

Pergunte direto, uma a uma; para cada "sim", peça a fundamentação fática:

| Inciso | Preliminar | Pergunta gatilho |
|---|---|---|
| I | Inexistência/nulidade de citação | A citação foi válida? Pessoal? Por hora certa? |
| II | Incompetência absoluta/relativa | O juízo é competente? Foro de eleição? Domicílio do consumidor? |
| III | Incorreção do valor da causa | O valor está coerente com o pedido? |
| IV | Inépcia da petição inicial | Pedido faltando elemento? Causa de pedir confusa? |
| V | Perempção | Mesma demanda já extinta 3x por abandono? |
| VI | Litispendência | Mesma ação correndo em outro lugar? |
| VII | Coisa julgada | Já houve decisão definitiva sobre o mesmo? |
| VIII | Conexão | Há processo conexo? |
| IX | Incapacidade da parte, defeito de representação, falta de autorização | Autor é capaz? Representado? |
| X | Convenção de arbitragem | Há cláusula compromissória? |
| XI | Ausência de legitimidade ou de interesse processual | A(o) autor(a) é parte legítima? Tem interesse? |
| XII | Falta de caução ou de outra prestação que a lei exige como preliminar | Caso de cautio judicatum solvi (autor no estrangeiro)? |
| XIII | Indevida concessão do benefício de gratuidade de justiça | A gratuidade do art. 98 do CPC foi concedida indevidamente? |

Para cada "sim", busque o texto literal do art. 337 inciso correspondente via MCP. Não escreva "art. 337, IV" sem o texto colado ao lado.

### 2.3 Mérito, impugnação especificada dos fatos (art. 341)

**Regra de ouro sobre confissão: nunca confesse fato explicitamente.** Fato verdadeiro que não tem como impugnar → silencie. Não mencione, não destaque, não use a palavra "confesso" em nenhuma hipótese. A única exceção é quando o fato desfavorável é indispensável para construir uma tese própria do réu (ex.: para alegar prescrição, é preciso mencionar a data da violação do direito, mas mesmo assim, use "suposta violação" de forma fluida na narrativa, nunca em destaque isolado como confissão).

Para cada fato narrado na inicial, classifique internamente (para fins de estratégia, não para colocar na peça):

- **Impugnado por divergência**, aconteceu, mas não como o autor narrou. Versão correta: [...]. → Narrar a versão do réu.
- **Impugnado por inexistência**, não aconteceu. → Afirmar diretamente.
- **Verdadeiro mas sem saída**, não impugnar; omitir da contestação. → Não mencionar.
- **Verdadeiro e necessário para tese do réu**, mencionar de forma fluida, com "suposta" ou "alegada", apenas na medida do necessário. → Nunca isolar como linha de confissão.
- **Desconhecido**, não temos como confirmar ou negar; aplicabilidade do art. 341, parágrafo único?

**Cuidado:** o art. 341 lista exceções (representante público sem ônus de impugnar, fatos que dependem de documento da própria parte autora, etc.). Buscar o texto via MCP.

### 2.4 Reconvenção (art. 343)? Pedido contraposto (Lei 9.099/1995 nos juizados)?
- Há pretensão própria do(a) ré(u) contra o(a) autor(a) conexa ao mesmo fato? Valor?
- Se sim, pedido contraposto (juizado) ou reconvenção (rito comum)?
- Buscar art. 343 do CPC via MCP para conferir requisitos.

### 2.5 Provas
- Quais provas o(a) ré(u) quer produzir? Documental (já junta), testemunhal (rol), pericial (área), depoimento pessoal do autor?

## Passo 3, Pesquisa legal

Para cada tese, preliminar ou mérito, siga `letradalei:pesquisa`: identifique a norma, busque o dispositivo, verifique `situacao` e registre o bloco de citação no formato de `../_shared/citacao-e-formato.md`. Norma fora do acervo → `[FORA DO CORPUS]`.

## Passo 4, Estrutura da peça

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [...] VARA [...]
DA COMARCA DE [...]

                                                  Processo nº [...]
                                                  [Classe processual]

[NOME DA(O) RÉ(U)], já qualificado(a) nos autos da ação que lhe move
[NOME DO AUTOR], por seu(sua) advogado(a) infra-assinado(a) (procuração doc. 01),
vem, respeitosamente, à presença de Vossa Excelência, com fundamento no art. 335
do Código de Processo Civil, apresentar

                                C O N T E S T A Ç Ã O

pelos fatos e fundamentos que passa a expor.

I, DAS PRELIMINARES                                   (omitir seção se não houver)

I.1, [Preliminar 1, ex.: Da incompetência relativa do juízo (art. 337, II,
       c/c art. 64 do CPC)]

Dispõe o art. 337, II, do CPC:

    [bloco de citação — ver ../_shared/citacao-e-formato.md]

[Aplicação ao caso. Doc. que comprova. Pedido específico, formatação normal.]

I.2, [Preliminar 2], mesma estrutura

II, DO MÉRITO

II.1, DA REALIDADE DOS FATOS  (versão da(o) ré(u))

[Contranarrativa cronológica. Cada divergência ancorada em documento.]

II.2, DA IMPUGNAÇÃO ESPECIFICADA  (art. 341 do CPC)

Nos termos do art. 341 do CPC:

    [bloco de citação do art. 341, via MCP]

Quanto aos fatos narrados na inicial, manifesta-se a(o) Ré(u) na forma seguinte:

  a) [fato 1]: IMPUGNADO. [Razão + doc.]
  b) [fato 2]: IMPUGNADO. [Versão do réu + doc. que sustenta.]
  c) [fato 3]: IMPUGNADO POR INEXISTÊNCIA. [Razão + doc.]
  d) [fato 4]: o(a) Ré(u) desconhece, pleiteia que o ônus probatório recaia
     sobre o autor (art. 373, I, do CPC). [Texto literal do art. 373, I.]

II.3, DO DIREITO

II.3.a, [Tese de mérito 1, ex.: Da inexistência de defeito do serviço]

Dispõe o art. 14, § 3º, do Código de Defesa do Consumidor:

    [bloco de citação, via MCP]

[Subsunção. 2-4 parágrafos. Formatação normal.]

II.3.b, [Tese 2], mesma estrutura.

II.4, DA INVERSÃO DO ÔNUS DA PROVA  (se aplicável, ou para refutar inversão
                                       pedida na inicial)

    [bloco de citação do art. 6º, VIII, do CDC, ou art. 373, §1º do CPC, via MCP]

III, DA RECONVENÇÃO                                   (omitir seção se não houver)

Com fundamento no art. 343 do CPC:

    [bloco de citação do art. 343, via MCP]

apresenta a(o) Ré(u) reconvenção em face do(a) Autor(a) Reconvindo(a), pelos fundamentos a seguir.

[Estrutura: fatos, direito, pedidos, valor da causa da reconvenção.]

IV, DAS PROVAS

Protesta a(o) Ré(u) pela produção de todas as provas em direito admitidas,
especialmente:

  a) documental, em juntada com esta peça (docs. nº [...]);
  b) testemunhal, rol em momento oportuno;
  c) pericial, [especificar área e quesitos serão apresentados na fase
     instrutória];
  d) depoimento pessoal do(a) Autor(a), sob pena de confissão.

V, DOS PEDIDOS

Diante do exposto, requer a(o) Ré(u):

  a) [pedidos preliminares, ex.: a remessa dos autos ao foro competente; a
     extinção sem resolução de mérito por inépcia; o reconhecimento da
     prescrição];
  b) caso superadas as preliminares, no mérito, a TOTAL IMPROCEDÊNCIA dos
     pedidos formulados na inicial;
  c) a condenação do(a) Autor(a) ao pagamento de custas processuais e
     honorários advocatícios (art. 85 do CPC), [texto literal via MCP];
  d) [se houver reconvenção] a procedência da reconvenção, com [pedidos
     específicos];
  e) a produção das provas indicadas no item IV.

Termos em que,
Pede deferimento.

[Cidade], [data].

_______________________________________
[NOME DA(O) ADVOGADA(O)]
OAB/[UF] nº [...]
```

## Passo 5, Conferências antes da entrega

1. **Prazo.** 15 dias úteis (art. 335 do CPC + art. 219), texto literal via MCP. Termo inicial verificado? (Audiência de conciliação? Carta com AR? Citação por hora certa?)
2. **Princípio da eventualidade** (art. 336). Todas as defesas levantadas em conjunto?
3. **Impugnação especificada** (art. 341). Cada fato da inicial classificado? Lacuna = confissão ficta, perigosíssimo.
4. **Pedido contraposto vs. reconvenção.** Se rito é juizado, é pedido contraposto (Lei 9.099), verificar.
5. **Documentos.** Procuração + comprovantes da versão da(o) ré(u), listados?
6. **Auditoria de citação** (segue `../_shared/citacao-e-formato.md`): todo dispositivo tem `citacao` + `source_url`? Toda jurisprudência tem `search_id` + `eficacia`? Sem isso = de memória = inválida; remover ou converter em marcador.
7. **Marcadores remanescentes:** `[VERIFICAR]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS]`, `[JURISPRUDÊNCIA]`, `[DOC. A NUMERAR]`, todos listados no `NOTAS.md`.

## Passo 6, Saída

Siga `../_shared/saida.md` com `<tipo> = contestacao`: monte o `.docx` com os utilitários de `montar_docx.py`, salve `outputs/contestacao-[slug]-[data].docx` + `outputs/contestacao-[slug]-NOTAS.md`, rode `colorir_marcadores.py` e inclua o aviso de itens em vermelho.

## O que esta skill NÃO faz

- **Não protocola.** Ato privativo do(a) advogado(a) habilitado(a).
- **Não calcula o prazo final.** Devolve o texto do art. 335 do CPC (via MCP) e os marcos legais; a contagem no PJe/eSAJ, com feriados forenses, suspensões e recesso (art. 220 do CPC), é sua.
- **Não insere jurisprudência não verificada.** O que não vier do MCP fica `[JURISPRUDÊNCIA, a ser inserida pelo(a) advogado(a)]`.
- **Não decide estratégia.** "Confessar este fato para fortalecer a defesa naquele" é decisão profissional; a skill estrutura, você decide.
- **Não substitui o(a) advogado(a).** Produz rascunho; assinatura, responsabilidade e estratégia são da pessoa habilitada na OAB.
