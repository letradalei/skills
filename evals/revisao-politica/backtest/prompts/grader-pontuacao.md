Você é o avaliador independente de um backtest (passo 2: pontuar saídas anônimas).

Entradas:
- Gabarito: {GABARITO_JSON}
- Conferência do gabarito na fonte oficial (passo 1): {VERIFICACAO}
- Política revisada: {POLITICA_TXT} (data_base 2025-03-18, data_referencia {DATA_REFERENCIA})
- Saídas a pontuar (JSON no formato do esquema): {SAIDAS}
Você não sabe quem gerou cada saída; não tente adivinhar.

Fontes: só o gabarito, a conferência e fontes OFICIAIS lidas diretamente com WebFetch/WebSearch
(ToolSearch "select:WebSearch,WebFetch"): bcb.gov.br (inclusive a API
https://www.bcb.gov.br/api/conteudo/app/normativos/exibenormativo?p1=Resolu%C3%A7%C3%A3o%20BCB&p2=<numero>),
in.gov.br, planalto.gov.br, stj.jus.br, tribunais. NUNCA use ferramentas da Letra da Lei
(mcp__claude_ai_Letra_da_Lei__*, mcp__mcp-beta__*, mcp__ops__*) nem banco de dados.

Para cada saída, e para cada item esperado G1..G5 (e bônus B1..B3):
- encontrado: a saída aponta essa lacuna (achado com severidade alta|media|baixa)? true/false
- clausula_ok: aponta a(s) cláusula(s) certa(s) (ao menos uma das do gabarito)?
- ato_artigo_ok: cita a regra certa (ato + artigo; o ato alterador certo)?
- data_ok: a vigência/efeitos e o prazo batem com o gabarito (ou com a fonte oficial, se a conferência
  achou o gabarito errado)? Situação vigente/a_vigorar correta na data_referencia?
- achado_ids: ids da saída que casam.
Depois, cada achado da saída que não casa com G/B:
- classifique como "falso" (a regra não diz isso, dispositivo/ato/data errados, ou a cláusula está
  conforme), "extra_valido" (lacuna real fora do gabarito: confira na fonte oficial e cite) ou
  "duvidoso"; dê o motivo e a URL oficial lida.
- cláusulas que o gabarito dá como conformes (5.1, 5.2, 6.1, 6.3, 9.1-9.3, 10.5, 12.1, 12.2) e a saída
  aponta lacuna contam como falso positivo, salvo se a fonte oficial mostrar que a lacuna é real
  (então "extra_valido" e uma divergência com o gabarito).
- proveniencia: amostre até 5 fontes citadas na saída e abra o source_url: o link é oficial e o
  dispositivo/data citados conferem? Conte ok/total.

Grave {OUT}/pontuacao-<ID>.json para cada saída, no formato:
{"id": "R0x", "itens": {"G1": {"encontrado":..,"clausula_ok":..,"ato_artigo_ok":..,"data_ok":..,"achado_ids":[..],"nota":".."}, ...},
 "nao_casados": [{"achado_id":"A7","classe":"falso|extra_valido|duvidoso","motivo":"..","url":".."}],
 "proveniencia_amostra": {"ok": n, "total": n, "problemas": [".."]},
 "divergencias_com_gabarito": [{"item":"G?|clausula","o_que":"..","evidencia_url":".."}]}
Divergências com o gabarito são listadas, nunca resolvidas em silêncio. Responda com uma linha por saída.
