# Contrato do resultado (JSON de entrada do renderizador)

O agente grava o resultado da revisão neste formato e chama `${CLAUDE_PLUGIN_ROOT}/scripts/montar_pacote_conformidade.py`, que valida o JSON e gera o PDF (e o `.docx`). Exemplo completo e válido: `../exemplos/resultado-exemplo.json`.

```jsonc
{
  "versao_esquema": "1.0",
  "exemplo": false,                       // true só para a política de exemplo (põe o aviso no PDF)
  "politica": {
    "titulo": "...", "instituicao": "...", "arquivo": "nome.docx", "versao": "3.0",
    "data_revisao": "AAAA-MM-DD",         // data de aprovação/revisão extraída do documento
    "fonte_data_revisao": "trecho do documento de onde a data saiu"
  },
  "revisao": {
    "modo": "atual" | "replay",
    "data_base": "AAAA-MM-DD",            // normalmente = politica.data_revisao
    "data_referencia": "AAAA-MM-DD",      // hoje, ou a data do replay
    "gerado_em": "AAAA-MM-DD",
    "conformidade_disponivel": true | false,
    "aviso_ferramentas": "obrigatório quando false: o que foi usado no lugar e o risco"
  },
  "resumo": "3 a 5 frases, com os números e os prazos",
  "achados": [{
    "id": "A1",
    "conceito": "MED | Contas suspeitas | Registros e reporte | ...",
    "clausula": {"ref": "10.2", "trecho": "texto literal da política"},
    "exige_hoje": "o que a regra exige na data de referência, em linguagem direta",
    "fontes": [{
      "citacao": "Res. BCB 1/2020, Regulamento anexo, art. 41-D, § 1º, I e II",
      "ato_alterador": "Res. BCB 559/2026, de 23/4/2026" | null,
      "vigencia": "AAAA-MM-DD",           // data em que a redação passou a valer (efeitos)
      "source_url": "https://...",        // obrigatório; sem ele o PDF marca [CITAÇÃO PENDENTE]
      "search_id": "handle do MCP"
    }],
    "severidade": "alta" | "media" | "baixa" | "conforme",
    "situacao": "vigente" | "a_vigorar",
    "prazo": {"data": "AAAA-MM-DD", "base": "ato e dispositivo que fixam o prazo", "vencido": true} | null,
    "nova_redacao": "texto proposto para a cláusula" | null
  }],
  "alteracoes": [{                        // forma de conformidade · alteracoes
    "data": "AAAA-MM-DD", "tipo_data": "vigencia | efeitos | assinatura | publicacao | julgamento",
    "tipo": "alterado | incluido | revogado | ...", "alvo": "dispositivos atingidos",
    "ato_fonte": {"citacao": "...", "slug": "...", "source_url": "..."},
    "comentario": "o que mudou", "origem": "conformidade · alteracoes | notas do texto consolidado | leitura do ato",
    "achados": ["A1"]
  }],
  "exposicao": [{
    "achados": ["A3"], "tese": "como os tribunais tratam a lacuna",
    "precedentes": [{"citacao": "...", "autoridade": "STJ", "tipo": "tema_repetitivo", "eficacia": "vinculante",
                     "data": "AAAA-MM-DD", "trecho": "enunciado ou ementa literal", "source_url": "...", "search_id": "..."}]
  }],
  "tarefas": [{
    "responsavel": "ops" | "juridico" | "fraude_compliance",
    "tarefa": "verbo + entrega", "achados": ["A1"],
    "prazo": "AAAA-MM-DD" | null,         // só quando a regra fixa prazo; nunca inventar
    "base_prazo": "ato e dispositivo do prazo, ou 'sem prazo próprio'"
  }],
  "auditoria": {
    "verificacoes": ["o que foi lido, de onde, em que data"],
    "nao_encontrado": ["o que se procurou e não se achou, com [VERIFICAR] quando couber"],
    "ferramentas": ["acervo · consultar", "..."],
    "limitacoes": ["..."]
  }
}
```

Regras que o renderizador aplica:
- Falta de chave obrigatória, severidade fora da lista, responsável fora da lista, data fora de `AAAA-MM-DD` ou `conformidade_disponivel` ausente: o script recusa o JSON e lista os erros.
- Fonte sem `citacao` ou `source_url`: sai `[CITAÇÃO PENDENTE]` em vermelho no PDF (aviso no terminal).
- Prazo `vencido` ausente: calculado contra `data_referencia`.
- Alteração com data posterior à `data_referencia`: aparece como "a vigorar".
- Marcadores `[VERIFICAR ...]`, `[NÃO ENCONTRADO ...]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS]` saem em vermelho.
