# Roteiro de consultas (conformidade e fallback público)

## 1. Ferramentas de conformidade (preferidas)

Servidas pelo gateway de produto da Letra da Lei (acesso de planos `team`/`partner`). Detecte pela lista de ferramentas: nomes terminados em `conformidade___conceito` e `conformidade___alteracoes`.

### `conformidade · conceito`
- **Args:** `id` | `nome` | `query` (um dos três), `data_referencia?` (AAAA-MM-DD), `desde?` (AAAA-MM-DD).
- **Retorna:** `conceito`, `ancestrais`, `descendentes`, `vinculos` agrupados em `regulacao`, `legislacao`, `jurisprudencia`, `doutrina` (cada item com `citacao`, `search_id`, `source_url`, `evidencia`) e `alteracoes` (rollup das mudanças nos dispositivos vinculados desde `desde`).
- **Como usar:** uma chamada por conceito da política, com `desde = data_base` e, no replay, `data_referencia = data do replay`. Comece por `query` com o tema da cláusula ("Mecanismo Especial de Devolução", "contas com fundada suspeita de fraude", "registros de fraude e relatório mensal"); depois use o `id` devolvido. Desça em `descendentes` quando a cláusula for mais específica que o conceito.
- `vinculos` é a lista de dispositivos a conferir. Não substitui a leitura do texto: leia cada dispositivo citado num achado com `acervo · consultar`.

### `conformidade · alteracoes`
- **Args:** `norma` | `search_id` | `conceito` (um dos três), `desde` (AAAA-MM-DD), `ate?` (AAAA-MM-DD).
- **Itens:** `data`, `tipo_data`, `tipo`, `alvo`, `ato_fonte {citacao, slug, source_url}`, `dispositivos`, `comentario`, `origem`.
- **Como usar:** `conceito = <id>` e `desde = data_base` para o histórico do conceito; `search_id` para o histórico de um artigo específico. No replay, `ate = data do replay`. Copie os itens para `alteracoes[]` do resultado, marcando `achados`.

## 2. Fallback público (sem as ferramentas de conformidade)

Diga no resultado (`conformidade_disponivel: false` + `aviso_ferramentas`) e no chat que a revisão usou as ferramentas públicas e que o histórico pode estar incompleto.

1. **Localizar a regra.** `legislacao-infralegal · buscar_atos` com `autoridade: "BCB,CMN"` (ou o regulador do tema) e `query` com o tema da cláusula; para um ato conhecido, `acervo · consultar` com `dominio: "legislacao-infralegal"`, `norma` ("BCB Resolução 1/2020") e `numeros` (até 5). Lei federal: `legislacao-federal · buscar_artigos` e `acervo · consultar` com `dominio: "legislacao"`.
2. **Reconstruir o histórico.** O texto consolidado infralegal anota cada mudança: "(Redação dada pela Resolução BCB nº 559, de 23/4/2026, produzindo efeitos a partir de 1º/7/2026.)", "(Incluído pela ...)", "(Revogado pela ...)". Toda nota com data posterior à `data_base` é uma alteração candidata. A data da nota é a do ato; a data de efeitos vem de "produzindo efeitos a partir de" ou da cláusula de vigência do ato alterador.
3. **Ler o ato alterador.** `acervo · consultar` no ato (`norma: "BCB Resolução 559/2026"`, `numeros: ["1","2","3"]`): o art. 1º/2º traz o texto novo, os seguintes trazem revogações e a vigência (às vezes escalonada por dispositivo). Prazos de implementação costumam estar no próprio dispositivo ("até o dia 13 de outubro de 2025") ou na cláusula de vigência.
4. **Lei federal no tempo.** `acervo · consultar` com `data_referencia` devolve a redação daquele dia (`vigente_desde`, `versao`); `legislacao-federal · explorar_contexto` mostra `alterado_por` com `data_vigencia`.
5. **Alcance do fallback.** Mudança sem nota no consolidado e dispositivo novo em artigo que a política não cita podem escapar. Registre em `auditoria.limitacoes`.

Quando um artigo não vier por número (aparece em `omitidos`), procure-o com `buscar_atos` (`norma` + `query`) ou dentro do registro do artigo anterior; registre em `auditoria.nao_encontrado` e, se for falha do acervo, em `acervo · reclame_aqui`.

## 3. Aplicação pelos tribunais

- Vinculantes primeiro: `jurisprudencia-federal · buscar_vinculantes` (temas, súmulas vinculantes), depois `buscar_precedentes` com `autoridade: "STJ"` para súmulas e acórdãos.
- Estadual: `jurisprudencia-estadual · buscar_precedentes` com `localidade` (UF da sede da instituição, ou "SP" como maior volume) e termos de ementa ("Mecanismo Especial de Devolução", "bloqueio cautelar Pix", "conta recebedora fraude").
- Leia a ementa inteira (`acervo · consultar`, `dominio: "jurisprudencia"`) antes de usar um trecho. Copie o trecho literal, com `eficacia` e `data`. Acórdão é `persuasiva`: diga isso.
- Precedente não encontrado para um achado: escreva "[NÃO ENCONTRADO] nenhum precedente pertinente no acervo" na tese, não preencha com memória.

## 4. Replay ("como em AAAA-MM-DD")

- `data_referencia` = data pedida; `modo: "replay"`.
- Considere só alterações cujo ato foi publicado até essa data (`ate` nas ferramentas de conformidade; no fallback, descarte notas de atos posteriores).
- Alteração publicada até a data mas com efeitos depois: achado com `situacao: "a_vigorar"` e o prazo de efeitos.
- Texto vigente: lei federal com `data_referencia`; infralegal, reconstruído a partir das notas (o consolidado traz só a redação atual): diga isso na auditoria.
- Jurisprudência: só decisões com data de julgamento até a data do replay.

## 5. Severidade

| Severidade | Quando |
|---|---|
| `alta` | Obrigação vigente que a política contraria ou omite e que atinge o consumidor ou o fluxo de recursos (bloqueio, devolução, recusa de transação), ou prazo regulatório já vencido. Exposição a responsabilidade objetiva. |
| `media` | Obrigação vigente parcialmente coberta, ou procedimento interno exigido (prazo de análise, registro, comunicação) sem efeito direto sobre recursos; ou obrigação com prazo futuro já publicado. |
| `baixa` | Referência desatualizada, redação imprecisa sem efeito prático, governança interna (revisão vencida). |
| `conforme` | Cláusula conferida contra o texto vigente, sem alteração desde a data-base, ou já aderente. Inclua as conformes relevantes: mostram o que foi checado. |
