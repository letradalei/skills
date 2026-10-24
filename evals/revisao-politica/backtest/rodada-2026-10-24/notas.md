## Leitura da rodada (2026-10-24)

**Configuração.** Política de exemplo, data_base 2025-03-18, data_referencia 2026-10-24 (modo atual), 3 rodadas por competidor, todas com o mesmo modelo (Opus 5.5) e o mesmo enunciado; só a lista de ferramentas muda (`prompts/tools-{a,b,c}.md`). Os competidores não viram o gabarito, a skill, `consultas.md` nem `resultado-exemplo.json`; o esquema foi neutralizado (`esquema-neutro.md`), porque o original traz o art. 41-D e a Res. 559/2026 como exemplo. Avaliação em dois passos: (1) um agente conferiu o gabarito na fonte oficial (API de normativos do BCB, planalto, STJ, e-SAJ); (2) três agentes pontuaram as 9 saídas anônimas, cada um com uma saída de cada competidor, sem saber quem era quem (`cegar.py` remove os campos que dizem as ferramentas).

**O que os números dizem.**
- **Descoberta empatou.** As 9 rodadas acharam as 5 lacunas plantadas (G1-G5), com a cláusula certa, e nenhuma teve achado falso. Esta política não separa os competidores na descoberta: as lacunas vêm de atos do BCB de 2025-2026 que a busca na web já indexa.
- **A diferença está na precisão e na proveniência:**
  - (a), busca na web: recall estrito 4,0/5. Uma rodada (R07) citou só reproduções não oficiais (legisweb, resumo de escritório): 0 de 27 links oficiais, 0 de 5 na amostra conferida, e a base de G3 estava errada (§§ 2º-3º revogados pela 559, que ela nem cita). Foi o mais lento (8,7 min) e o mais barato (US$ 0,62).
  - (b), ferramentas públicas: recall estrito 3,7/5 e o menos consistente (40%). Em 2 de 3 rodadas, G1 ficou sem a âncora certa (Res. 142, art. 2º-A, e o prazo de 13/10/2025). 100% dos links são oficiais.
  - (c), grafo de conceitos: recall estrito 4,0/5, o melhor em ato/artigo (4,7) e o que mais achou lacunas reais fora do gabarito (4,7 por rodada). Erro recorrente: em 2 de 3 rodadas atribuiu o dever de G4 (art. 56, § 3º) só à Res. 587/2026, sem a 506/2025. É plausível que venha do histórico de alterações, que mostra a redação mais recente; isso não foi investigado.
- **Ressalvas de tamanho.** Com n=3 e três avaliadores diferentes, 4,0 contra 3,7 é ruído. As diferenças estritas dependem de juízos do avaliador ("parcial" vale meio ponto e nunca conta como estrito).
- **Custo.** O custo é estimado como tokens × US$ 5,6 por milhão: preço de tabela do Opus 5.5 (US$ 4 de entrada, US$ 20 de saída por MTok), supondo 90% de entrada e 10% de saída, sem cache. Os tokens são o `subagent_tokens` do relatório do agente. É uma ordem de grandeza.
- **Tempo.** O tempo vem de `inicio.txt` e `fim.txt`, gravados pelo próprio competidor.

**Números que dependem dos dados BCB ainda não recarregados.** Em prod e no branch de teste br-round-cloud-aclltn4o ainda não estão duas correções: o texto das alterações cortado em 300 caracteres e os arts. 78-HA a 78-HD não consultáveis por número.
- Dependem disso (b) e (c), que leem esse acervo: (b) pelo MCP público em prod, (c) pelo CLI local sobre o branch de teste, que também tem os dados antigos.
- Os itens afetados são:
  - G5, que trata dos arts. 78-HA a 78-HD. Os competidores (b) e (c) os citaram a partir da própria Res. 587, porque o consolidado não os devolve por número.
  - A datação de G4 e de G5, que vem do histórico de alterações cujo texto está truncado.
  - Os campos de proveniência que vêm desse histórico.
- Não dependem disso (a) nem o avaliador, que leram bcb.gov.br diretamente.
- Recarregado o BCB, rodar de novo (b) e (c).

**Outras limitações.**
- No CLI local, `conceito` com `query` usou o fallback lexical: não há credencial AWS para o embedding Bedrock. A busca por nome, alias e id funciona como no deploy.
- As restrições de ferramenta foram impostas por enunciado e conferidas pelos `log.txt` que o próprio competidor escreveu, não por bloqueio técnico. Os logs não mostram violação.
- O avaliador leu as teses do STJ só por resumo do WebFetch, e as dos dois acórdãos do TJSP não foram lidas, porque a busca do e-SAJ tem reCAPTCHA.

**Como rodar de novo.**
```bash
W=<pasta de trabalho>; python3 -I preparar.py --work $W --data-referencia 2026-10-24 --runs 3 \
  --platform <platform-worktree yc-compliance-core> --dburl-file <arquivo com a URL do branch de TESTE>
# um agente por prompt em $W/prompts/Rxx.md (contenders); depois prompts/grader-gabarito.md
python3 -I cegar.py --work $W        # saídas anônimas em $W/grading/
# 3 agentes com prompts/grader-pontuacao.md, cada um com uma saída de cada competidor
# $W/custos.json: {"Rxx": {"tokens": n, "usd": x}} a partir do uso de cada agente
python3 -I pontuar.py --work $W --out <rodada> --notas <rodada>/notas.md --resumo-divergencias <rodada>/resumo-divergencias.md
```
