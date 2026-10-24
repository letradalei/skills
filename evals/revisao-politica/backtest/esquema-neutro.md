# Esquema do resultado (backtest)

Mesma forma JSON do resultado da skill `revisao-politica` (`references/esquema-resultado.md`), com os
exemplos trocados por marcadores neutros para não dar pistas aos competidores. Grave UM arquivo JSON
válido (sem comentários) nesta forma.

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
    "conceito": "<tema da cláusula>",
    "clausula": {"ref": "10.2", "trecho": "texto literal da política"},
    "exige_hoje": "o que a regra exige na data de referência, em linguagem direta",
    "fontes": [{
      "citacao": "<ato>, <dispositivo: art., §, inciso>",
      "ato_alterador": "<ato alterador>, de <data>" | null,
      "vigencia": "AAAA-MM-DD",           // data em que a redação passou a valer (efeitos)
      "source_url": "https://...",        // obrigatório; sem ele o PDF marca [CITAÇÃO PENDENTE]
      "search_id": "identificador da ferramenta, se houver" | null
    }],
    "severidade": "alta" | "media" | "baixa" | "conforme",
    "situacao": "vigente" | "a_vigorar",
    "prazo": {"data": "AAAA-MM-DD", "base": "ato e dispositivo que fixam o prazo", "vencido": true} | null,
    "nova_redacao": "texto proposto para a cláusula" | null
  }],
  "alteracoes": [{                        
    "data": "AAAA-MM-DD", "tipo_data": "vigencia | efeitos | assinatura | publicacao | julgamento",
    "tipo": "alterado | incluido | revogado | ...", "alvo": "dispositivos atingidos",
    "ato_fonte": {"citacao": "...", "slug": "...", "source_url": "..."},
    "comentario": "o que mudou", "origem": "<de onde saiu a alteração>",
    "achados": ["A1"]
  }],
  "exposicao": [{
    "achados": ["A1"], "tese": "como os tribunais tratam a lacuna",
    "precedentes": [{"citacao": "...", "autoridade": "<tribunal>", "tipo": "<tipo>", "eficacia": "<eficácia>",
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
    "ferramentas": ["<ferramentas usadas>"],
    "limitacoes": ["..."]
  }
}
```

Regras:
- Datas em `AAAA-MM-DD`. `severidade` em alta|media|baixa|conforme; `situacao` em vigente|a_vigorar;
  `responsavel` em ops|juridico|fraude_compliance.
- Toda fonte traz `citacao` (ato + dispositivo), `vigencia` (data em que a redação passou a valer) e `source_url`.
- Prazo só quando a regra o fixa; não invente.
- Cláusula conferida sem lacuna entra como achado `conforme`.
