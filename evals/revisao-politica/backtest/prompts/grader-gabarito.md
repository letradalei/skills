Você é o avaliador independente de um backtest (passo 1: conferir o gabarito na fonte oficial).

Leia o gabarito: {GABARITO_JSON} (e {GABARITO_MD}). Ele lista os achados esperados (G1..G5), os bônus
(B1..B3), as cláusulas que devem sair conformes e a exposição judicial, numa revisão da política
{POLITICA_TXT} com data_base 2025-03-18 e data_referencia {DATA_REFERENCIA}.

Regra central: confira cada fato SOMENTE em fontes oficiais, lidas diretamente com WebFetch/WebSearch
(carregue com ToolSearch "select:WebSearch,WebFetch"): bcb.gov.br (exibenormativo, inclusive a API
https://www.bcb.gov.br/api/conteudo/app/normativos/exibenormativo?p1=Resolu%C3%A7%C3%A3o%20BCB&p2=<numero>
que devolve o texto em JSON), in.gov.br (DOU), planalto.gov.br, stj.jus.br / scon.stj.jus.br,
tjsp.jus.br. NUNCA use ferramentas da Letra da Lei (mcp__claude_ai_Letra_da_Lei__*, mcp__mcp-beta__*,
mcp__ops__*), bancos de dados, nem arquivos fora de {GABARITO_JSON}, {GABARITO_MD} e {POLITICA_TXT}.

Para cada item G1..G5, B1..B3 e cada precedente da exposição, confira: (1) a regra/dispositivo existe
com esse conteúdo na data_referencia; (2) o ato alterador e a data do ato; (3) a data de
vigência/efeitos e o prazo; (4) se a cláusula da política apontada de fato tem a lacuna. Confira também
as cláusulas "conformes" por amostra (ao menos 5.2, 9.1 e 10.5).

Grave {OUT}/verificacao-gabarito.json:
{"itens": [{"id": "G1", "confere": true|false|"parcial", "regra_ok": bool, "ato_alterador_ok": bool,
  "vigencia_ok": bool, "prazo_ok": bool|null, "lacuna_ok": bool, "evidencia": [{"url": "...",
  "trecho": "trecho literal lido"}], "divergencia": "o que difere do gabarito, ou null"}],
 "nao_conferido": ["o que não conseguiu ler na fonte oficial e por quê"]}
Não corrija o gabarito: só registre divergências com a evidência. Responda com uma linha por item.
