# Ferramentas MCP da Letra da Lei

A superfície pública da MCP da Letra da Lei atualmente expõe duas ferramentas de pesquisa jurídica:

## `listar_legislacao_federal`

Use esta ferramenta quando o usuário perguntar:

- quais leis federais estão cobertas
- se uma determinada lei está disponível
- qual `law_key` deve ser usado antes de uma busca direcionada

Ela retorna uma lista de leis com:

- `law_key`
- `title`
- `corpus_group`
- `source_url`
- `source_indexed_at`

## `buscar_legislacao_federal`

Use esta ferramenta para busca semântica sobre a legislação federal brasileira.

Parâmetros mais comuns:

- `query`: pergunta em linguagem natural, em português ou inglês
- `corpus`: `law_key` opcional para restringir a busca a uma única lei
- `date`: data ISO 8601 opcional para consultar a versão da lei vigente naquela data

Formato esperado do resultado:

- número do artigo
- texto completo
- data de vigência
- link direto para a fonte autoritativa no Planalto

## Postura de pesquisa

- Pesquise primeiro, responda depois.
- Prefira citações em nível de artigo a resumos genéricos.
- Se faltar cobertura, diga isso em vez de adivinhar.
