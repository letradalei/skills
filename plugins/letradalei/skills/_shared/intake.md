# Intake antes de redigir (contrato compartilhado das peças)

Material de apoio das skills de redação. A peça é moldada pelos dados do caso; uma minuta redigida sobre dado inventado ou presumido se invalida. Por isso a entrevista vem antes do rascunho.

## Entreviste primeiro

Antes de escrever qualquer linha da peça, **entreviste o usuário** pelo mecanismo interativo do host — no Claude Code, a ferramenta `AskUserQuestion`; no Codex, `request_user_input`; em outros runtimes, o recurso equivalente de perguntas ao usuário — em blocos de **no máximo 4 perguntas por rodada** (mais que isso cansa e degrada as respostas). Se faltar dado essencial depois da 1ª rodada, faça uma 2ª antes de prosseguir. Cada skill traz o seu próprio roteiro de perguntas — siga-o.

**Regra de ouro:** se o usuário não informou, não invente. Marque `[VERIFICAR]` e liste o item no bloco de notas final. A única exceção é dado não-essencial que o juízo não exige (ex.: e-mail da parte, quando dispensável).

## Sem usuário para entrevistar (execução não-interativa)

Se não houver usuário disponível para responder — execução automatizada, headless ou em lote —, **não trave**: redija com os dados já fornecidos e marque cada campo essencial ausente com `[VERIFICAR: ...]`. A entrevista interativa é o caminho preferencial; este é o fallback quando ela é impossível. A regra de ouro continua valendo: nunca invente dado.

## Protocolo "Informar manualmente"

No Claude Code, o `AskUserQuestion` (no Codex, `request_user_input`) oferece ao usuário a opção de deixar um item para "Informar manualmente"; em outros runtimes, trate do mesmo modo qualquer item que o usuário deixe em aberto. Depois de cada rodada, verifique se alguma resposta foi essa. Se foi, **não avance** para a etapa seguinte: reúna todos esses itens em uma única mensagem e peça que o usuário os forneça antes de continuar —

> "Você marcou os seguintes itens para preenchimento manual. Por favor, informe cada um antes de prosseguirmos:
> - [item 1]
> - [item 2]
> - ..."

Só siga para a redação quando todos os itens "Informar manualmente" tiverem sido respondidos ou explicitamente descartados pelo usuário (um descarte vira `[VERIFICAR]`).
