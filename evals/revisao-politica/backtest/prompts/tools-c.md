- As ferramentas públicas da Letra da Lei: mcp__claude_ai_Letra_da_Lei__* (acervo___consultar,
  acervo___listar, legislacao-infralegal___buscar_atos, legislacao-federal___buscar_artigos,
  legislacao-federal___explorar_contexto, jurisprudencia-federal___buscar_precedentes/buscar_vinculantes,
  jurisprudencia-estadual___buscar_precedentes/buscar_vinculantes). Carregue-as com ToolSearch
  ("+Letra_da_Lei").
- E as ferramentas de conformidade (grafo de conceitos + histórico de alterações), por um CLI local
  somente leitura. Chame pelo Bash, sempre com a variável de ambiente abaixo:
    export PRODCOPY_DATABASE_URL="$(cat {DBURL_FILE})"
    {CLI} conceito '{"query":"<tema>"}'             # busca conceito por tema (ou "nome":"MED", ou "id":"letradalei:...")
    {CLI} conceito '{"id":"<id>","desde":"<data_base>","data_referencia":"<data_referencia>"}'
        -> o conceito, ancestrais, subconceitos, vínculos (regulação, legislação, jurisprudência, com
           search_id e source_url) e o histórico de alterações de cada dispositivo vinculado desde data_base
    {CLI} alteracoes '{"conceito":"<id ou nome>","desde":"<data_base>","ate":"<data_referencia>"}'
    {CLI} alteracoes '{"norma":"BCB-Res-1-2020","desde":"<data_base>","ate":"<data_referencia>"}'
    {CLI} alteracoes '{"search_id":"<search_id de um artigo>","desde":"<data_base>"}'
  Comece pelos conceitos que a política toca e use os vínculos e as alterações como roteiro; leia o texto integral dos dispositivos com
  acervo___consultar.
- Bash/Read/Write só para ler as entradas, chamar o CLI e gravar as saídas.
- NÃO use busca na web (WebSearch, WebFetch, curl), nem mcp__mcp-beta__*, mcp__ops__*, psql ou outro acesso ao banco.
