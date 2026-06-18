# Citação e formato (contrato compartilhado das peças)

Material de apoio das skills de redação (`peticao`, `contestacao`, `fundamentacao`, `analise`). Define **como uma fonte verificada entra na peça** e **como é formatada no `.docx`**. Para *localizar e verificar* lei e jurisprudência, siga a skill `letradalei:pesquisa` — ela é a autoridade sobre as ferramentas do MCP, os parâmetros e as verificações de vigência.

## Por que nada vem de memória

Toda lei e todo precedente da peça vêm do MCP da Letra da Lei. O modelo erra número de artigo, parágrafo e redação vigente — e as leis mudam (ex.: a Lei 14.905/2024 alterou os arts. 389 e 406 do Código Civil). Numa peça processual isso não é detalhe de estilo: citar dispositivo inexistente ou revogado é sancionável (CPC art. 80, II; art. 81) e compromete a credibilidade do(a) advogado(a) perante o juízo e a OAB. O MCP existe para eliminar essa classe de erro. Logo: pesquise, verifique, e só então cite.

Uma citação sem `citacao` + `source_url` retornados pela ferramenta não foi verificada — não entra na peça; vira `[CITAÇÃO PENDENTE]`. Isso vale também para dispositivos mencionados fora de um bloco de transcrição (em alertas, notas ou texto corrido): a referência precisa ser verificada via MCP.

## O que pode (e não pode) ser citado

- `situacao` ≠ `vigente` → `[VERIFICAR VIGÊNCIA, situação: <X>]`; não apresente como vigente.
- Norma estadual, municipal ou infralegal (decreto, portaria, resolução de agência) está fora do acervo → `[FORA DO CORPUS]`.
- Busca vazia, contraditória ou irrelevante → registre a lacuna via `acervo · reclame_aqui` antes de seguir. **Sem suplementação silenciosa:** se o MCP cobre pouco um instituto que a peça precisa, pare e pergunte ao usuário antes de buscar em outra fonte — a decisão é dele(a), não da skill.

## Bloco de citação — lei federal

```
    [texto literal retornado pelo MCP, recuado 1,25 cm à esquerda,
     justificado, fonte 1pt menor que o corpo]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[linha em branco; o texto principal retoma aqui, em formatação normal]
```

## Bloco de citação — jurisprudência

A força do precedente vem do campo `eficacia`:
- **vinculante** — observância obrigatória (art. 927 CPC); cite sem ressalva.
- **obrigatoria** — forte deferência (ex.: súmulas comuns); cite com o enunciado literal.
- **persuasiva** — subsídio argumentativo; marque `[JURISPRUDÊNCIA PERSUASIVA, revisar pertinência ao caso antes do protocolo]`.

```
    [enunciado literal do MCP, recuado 1,25 cm, justificado, fonte 1pt menor]
    Fonte: [autoridade] | [tipo] | search_id: [search_id] | eficacia: [eficacia]
```

Enunciado truncado (`is_truncated: true`) → busque o inteiro teor com `acervo · consultar` (`dominio: "jurisprudencia"`, `esfera`) antes de citar. Resultado zero ou não pertinente → `[JURISPRUDÊNCIA, a ser inserida pelo(a) advogado(a)]`; nunca transcreva enunciado de memória.

## Formatação no `.docx`

A transcrição **não leva aspas**: o recuo e a fonte menor já a distinguem visualmente do texto do(a) advogado(a), e aspas sobre texto recuado são redundantes e fogem ao padrão forense. Mantenha o mesmo formato em toda a peça.

- **Recuo:** margem esquerda deslocada 1,25 cm (720 DXA) em relação ao texto principal.
- **Alinhamento:** justificado — em todo o documento, não só na transcrição (`AlignmentType.JUSTIFIED`).
- **Fonte da transcrição:** 1pt menor que o corpo (corpo 12pt → transcrição 11pt).
- **Linha "Fonte:"** imediatamente após o texto transcrito, no mesmo recuo e tamanho menor.
- **Linha em branco** separando o bloco do parágrafo seguinte.

Se o bloco `Fonte:` não puder ser preenchido (faltam `citacao`/`source_url`), o dispositivo não foi buscado via MCP e não entra na peça.
