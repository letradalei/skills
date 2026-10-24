Você é o competidor {CONTENDER} de um backtest. Revise uma política interna de prevenção a fraudes de
uma instituição de pagamento brasileira (fictícia) contra a regulação e a legislação vigentes e grave o
resultado em JSON.

Entradas (leia só estas):
- Política (texto extraído do .docx): {SANDBOX}/politica.txt
- Formato do resultado: {SANDBOX}/esquema-neutro.md

Parâmetros:
- data_base = a data de aprovação declarada na política.
- data_referencia = {DATA_REFERENCIA} (revise como a regra estava nesse dia; mudanças com efeitos
  posteriores ficam "a_vigorar").
- modo = "replay" se data_referencia for anterior a hoje, senão "atual". exemplo = true.

Proibido (invalida a rodada):
- Ler qualquer arquivo fora de {SANDBOX} e de {OUTDIR}; em especial nada em
  /Users/juliolins/letradalei/skills-worktrees, /Users/juliolins/letradalei/company-brain ou outros repositórios.
- Usar ferramentas fora da lista abaixo.

Ferramentas permitidas:
{TOOLS}

Tarefa:
1. Separe as cláusulas operativas e identifique as normas que as regem.
2. Descubra o que mudou nessas normas entre data_base e data_referencia (atos alteradores, datas de
   vigência/efeitos, prazos de implementação).
3. Para cada cláusula operativa, diga se há lacuna (achado com severidade) ou se está conforme. Cite em
   cada fonte o ato, o dispositivo, o ato alterador, a vigência e o link (source_url). Não invente: o que
   não conseguir confirmar vai em auditoria.nao_encontrado.
4. Preencha exposicao (precedentes dos tribunais) e tarefas se as ferramentas permitirem.

Registro (obrigatório):
- Primeiro comando: `date -u +%Y-%m-%dT%H:%M:%SZ > {OUTDIR}/inicio.txt`.
- Mantenha {OUTDIR}/log.txt com uma linha por chamada de ferramenta de pesquisa (ferramenta + consulta).
- Grave o resultado em {OUTDIR}/resultado.json e valide com `python3 -c "import json;json.load(open('{OUTDIR}/resultado.json'))"`.
- Último comando: `date -u +%Y-%m-%dT%H:%M:%SZ > {OUTDIR}/fim.txt`.

Resposta final: uma linha com o caminho do JSON, o número de achados por severidade e o número de
chamadas de ferramenta de pesquisa.
