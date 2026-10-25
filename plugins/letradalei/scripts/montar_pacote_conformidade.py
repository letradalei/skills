#!/usr/bin/env python3
"""Monta o pacote de aprovação da skill revisao-politica (PDF e, opcionalmente, .docx).

Recebe o resultado da revisão em JSON (contrato em
skills/revisao-politica/references/esquema-resultado.md) e gera um documento com:
(a) resumo, (b) achados, (c) alterações desde a última revisão, (d) exposição
judicial, (e) tarefas por responsável e (f) registro de auditoria.

Uso:
    python montar_pacote_conformidade.py resultado.json
    python montar_pacote_conformidade.py resultado.json --pdf saida.pdf --docx saida.docx

Sem --pdf/--docx, salva em outputs/revisao-politica-<slug>-<data>.pdf e .docx.
O .docx usa os utilitários de montar_docx.py (mesmo padrão das demais skills).

Dependências: reportlab (PDF) e python-docx (.docx):
    pip install reportlab python-docx
O reportlab gera PDF em Python puro, sem binários de sistema (ao contrário do
weasyprint, que exige Pango/Cairo), por isso foi o escolhido.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import date
from xml.sax.saxutils import escape

SEVERIDADES = ("alta", "media", "baixa", "conforme")
ROTULO_SEV = {"alta": "Alta", "media": "Média", "baixa": "Baixa", "conforme": "Conforme"}
COR_SEV = {"alta": "#B42318", "media": "#B54708", "baixa": "#175CD3", "conforme": "#067647"}
RESPONSAVEIS = {
    "ops": "Operações",
    "juridico": "Jurídico",
    "fraude_compliance": "Prevenção a Fraudes e Compliance",
}
TIPO_DATA = {"vigencia": "vigência", "efeitos": "efeitos", "assinatura": "assinatura",
             "publicacao": "publicação", "julgamento": "julgamento"}
# Critério de severidade (esquema 1.1): a regra da tabela de references/consultas.md, seção 5, que o agente
# aplicou. O prefixo do código é a severidade, para que os mesmos fatos deem sempre a mesma classificação.
CRITERIOS = {
    "A-PRAZO": "prazo de implementação fixado pela regra já vencido, sem a cláusula aderir",
    "A-RECURSOS": "obrigação vigente contrariada ou omitida que decide se o dinheiro do cliente circula ou volta",
    "M-PARCIAL": "obrigação vigente parcialmente coberta, sem efeito sobre recursos na parte que falta",
    "M-PROCEDIMENTO": "procedimento exigido (prazo de análise, registro, comunicação, chaves) sem efeito direto sobre recursos",
    "M-FUTURO": "obrigação publicada com efeitos posteriores à data de referência",
    "B-REFERENCIA": "referência desatualizada ou redação imprecisa sem efeito prático",
    "B-GOVERNANCA": "governança interna da política (revisão vencida, papéis)",
    "C-ADERENTE": "cláusula conferida contra o texto vigente na data de referência, aderente",
}
PREFIXO_SEV = {"A": "alta", "M": "media", "B": "baixa", "C": "conforme"}
MARCADOR = re.compile(r"\[(?:VERIFICAR|CITAÇÃO PENDENTE|NÃO ENCONTRADO|FORA DO CORPUS|A REVISAR|ATENÇÃO)[^\]]*\]")


class ResultadoInvalido(ValueError):
    pass


# ---------------------------------------------------------------- validação

def validar(res: dict) -> list:
    """Confere o contrato mínimo. Levanta ResultadoInvalido com todos os problemas;
    devolve avisos não bloqueantes (ex.: achado sem fonte vira [CITAÇÃO PENDENTE])."""
    erros, avisos = [], []
    for chave in ("politica", "revisao", "achados", "alteracoes", "exposicao", "tarefas", "auditoria"):
        if chave not in res:
            erros.append(f"falta a chave '{chave}'")
    if erros:
        raise ResultadoInvalido("; ".join(erros))
    pol, rev = res["politica"], res["revisao"]
    for c in ("titulo", "data_revisao"):
        if not pol.get(c):
            erros.append(f"politica.{c} vazio")
    for c in ("modo", "data_base", "data_referencia"):
        if not rev.get(c):
            erros.append(f"revisao.{c} vazio")
    if rev.get("modo") not in (None, "atual", "replay"):
        erros.append("revisao.modo deve ser 'atual' ou 'replay'")
    if "conformidade_disponivel" not in rev:
        erros.append("revisao.conformidade_disponivel ausente (diga se as ferramentas de conformidade foram usadas)")
    for c in ("data_base", "data_referencia"):
        try:
            date.fromisoformat(rev.get(c) or "")
        except ValueError:
            erros.append(f"revisao.{c} não é AAAA-MM-DD")
    v11 = str(res.get("versao_esquema", "1.0")) >= "1.1"
    ids = set()
    for i, a in enumerate(res["achados"]):
        onde = f"achados[{i}]"
        if a.get("id") in ids:
            erros.append(f"{onde}.id repetido: {a.get('id')}")
        ids.add(a.get("id"))
        if a.get("severidade") not in SEVERIDADES:
            erros.append(f"{onde}.severidade deve ser uma de {SEVERIDADES}")
        if not (a.get("clausula") or {}).get("ref"):
            erros.append(f"{onde}.clausula.ref vazio")
        crit = a.get("criterio")
        if v11 and crit not in CRITERIOS:
            erros.append(f"{onde}.criterio deve ser um de {list(CRITERIOS)}")
        elif crit and PREFIXO_SEV.get(crit[:1]) != a.get("severidade"):
            erros.append(f"{onde}.criterio {crit} não corresponde à severidade {a.get('severidade')}")
        fontes = a.get("fontes") or []
        if not fontes:
            avisos.append(f"{a.get('id')}: sem fonte, marcado [CITAÇÃO PENDENTE]")
        for f in fontes:
            if not f.get("citacao") or not f.get("source_url"):
                avisos.append(f"{a.get('id')}: fonte sem citacao/source_url, marcada [CITAÇÃO PENDENTE]")
    if v11:
        operativas = pol.get("clausulas_operativas") or []
        if not operativas:
            erros.append("politica.clausulas_operativas vazio (liste as cláusulas operativas da política)")
        cobertas = set()
        for a in res["achados"]:
            cobertas |= refs_clausula((a.get("clausula") or {}).get("ref", ""))
        faltam = [c for c in operativas if c not in cobertas]
        if faltam:
            erros.append(f"cláusulas operativas sem achado nem 'conforme': {faltam} (toda cláusula operativa termina num achado)")
    for t in res["tarefas"]:
        if t.get("responsavel") not in RESPONSAVEIS:
            erros.append(f"tarefa com responsavel inválido: {t.get('responsavel')} (use {list(RESPONSAVEIS)})")
    if erros:
        raise ResultadoInvalido("; ".join(erros))
    return avisos


# ---------------------------------------------------------------- auxiliares

def refs_clausula(ref: str) -> set:
    """Itens numerados que uma referência de cláusula cobre: "10.2" -> {10.2}; "10.1 e 10.3" -> {10.1, 10.3};
    "9.1 a 9.3" -> {9.1, 9.2, 9.3}; "12" -> {12}."""
    out = set()
    for ini, fim in re.findall(r"(\d+(?:\.\d+)*)(?:\s*a\s*(\d+(?:\.\d+)*))?", ref or ""):
        out.add(ini)
        if fim and "." in ini and "." in fim and ini.rsplit(".", 1)[0] == fim.rsplit(".", 1)[0]:
            base = ini.rsplit(".", 1)[0]
            for n in range(int(ini.rsplit(".", 1)[1]), int(fim.rsplit(".", 1)[1]) + 1):
                out.add(f"{base}.{n}")
    return out


def data_br(iso):
    if not iso:
        return "sem data"
    try:
        d = date.fromisoformat(iso)
    except ValueError:
        return iso
    return d.strftime("%d/%m/%Y")


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60] or "politica"


def contagem(res: dict) -> dict:
    c = {s: 0 for s in SEVERIDADES}
    for a in res["achados"]:
        c[a["severidade"]] += 1
    return c


def fonte_txt(f: dict) -> str:
    if not f.get("citacao") or not f.get("source_url"):
        return f"[CITAÇÃO PENDENTE] {f.get('citacao') or ''}".strip()
    partes = [f["citacao"]]
    if f.get("ato_alterador"):
        partes.append(f"alterado por {f['ato_alterador']}")
    partes.append(f"vigência {data_br(f.get('vigencia'))}")
    return " | ".join(partes)


def prazo_txt(p, ref_iso):
    if not p or not p.get("data"):
        return "sem prazo fixado pela regra"
    vencido = p.get("vencido")
    if vencido is None:
        vencido = p["data"] <= ref_iso
    estado = "vencido" if vencido else "a vencer"
    return f"{data_br(p['data'])} ({estado}; {p.get('base', 'base não informada')})"


def quando_txt(m, ref_iso):
    t = f"{data_br(m.get('data'))} ({TIPO_DATA.get(m.get('tipo_data'), m.get('tipo_data') or 'data')})"
    return t + (" a vigorar" if (m.get("data") or "") > ref_iso else "")


def ordenar_achados(achados):
    return sorted(achados, key=lambda a: (SEVERIDADES.index(a["severidade"]), a.get("id", "")))


def titulo_doc(res):
    return f"Revisão de política: {res['politica']['titulo']}"


def linha_modo(rev):
    if rev["modo"] == "replay":
        return (f"Replay: revisão como seria feita em {data_br(rev['data_referencia'])}, "
                f"considerando só alterações até essa data")
    return f"Revisão na data de {data_br(rev['data_referencia'])}"


def aviso_ferramentas(rev):
    if rev.get("conformidade_disponivel"):
        return None
    return rev.get("aviso_ferramentas") or (
        "As ferramentas de conformidade não estavam disponíveis. A revisão usou as ferramentas públicas "
        "da Letra da Lei; o histórico de alterações pode estar incompleto.")


# ---------------------------------------------------------------- PDF

def gerar_pdf(res: dict, caminho: str) -> str:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                    Table, TableStyle)

    pol, rev = res["politica"], res["revisao"]
    base = getSampleStyleSheet()
    st = {
        "corpo": ParagraphStyle("corpo", parent=base["BodyText"], fontName="Helvetica", fontSize=9.5,
                                leading=13, alignment=TA_JUSTIFY),
        "cel": ParagraphStyle("cel", parent=base["BodyText"], fontName="Helvetica", fontSize=8.3, leading=10.5),
        "celb": ParagraphStyle("celb", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.3,
                               leading=10.5),
        "h1": ParagraphStyle("h1", parent=base["Title"], fontName="Helvetica-Bold", fontSize=17, leading=21,
                             alignment=0, spaceAfter=4),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=12.5,
                             leading=16, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#101828")),
        "h3": ParagraphStyle("h3", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=10,
                             leading=13, spaceBefore=6, spaceAfter=3),
        "sub": ParagraphStyle("sub", parent=base["BodyText"], fontName="Helvetica", fontSize=9.5,
                              textColor=colors.HexColor("#475467")),
        "aviso": ParagraphStyle("aviso", parent=base["BodyText"], fontName="Helvetica", fontSize=9,
                                leading=12, textColor=colors.HexColor("#7A2E0E")),
    }

    def p(texto, estilo="corpo"):
        t = escape(texto or "").replace("\n", "<br/>")
        t = MARCADOR.sub(lambda m: f'<font color="#D92D20"><b>{m.group(0)}</b></font>', t)
        return Paragraph(t, st[estilo])

    def link(url, estilo="cel"):
        if not url:
            return p("[CITAÇÃO PENDENTE]", estilo)
        return Paragraph(f'<link href="{escape(url)}" color="#175CD3">{escape(url)}</link>', st[estilo])

    def sev(s):
        return Paragraph(f'<font color="{COR_SEV[s]}"><b>{ROTULO_SEV[s]}</b></font>', st["cel"])

    grade = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D0D5DD")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F4F7")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ])
    ficha = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D0D5DD")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F9FAFB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ])
    largura = A4[0] - 3.6 * cm
    ref_iso = rev["data_referencia"]
    h = []

    if res.get("exemplo"):
        h.append(p("DOCUMENTO DE EXEMPLO, SEM RELAÇÃO COM INSTITUIÇÃO REAL", "aviso"))
    h.append(p(titulo_doc(res), "h1"))
    h.append(p(f"{pol.get('instituicao', '')}  |  {linha_modo(rev)}", "sub"))
    h.append(Spacer(1, 6))
    aviso = aviso_ferramentas(rev)
    if aviso:
        t = Table([[p("Aviso sobre as fontes: " + aviso, "aviso")]], colWidths=[largura])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FEF6EE")),
                               ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#F79009"))]))
        h += [t, Spacer(1, 6)]

    # (a) resumo
    h.append(p("1. Resumo", "h2"))
    c = contagem(res)
    dados = [
        ["Política", f"{pol['titulo']} (versão {pol.get('versao', 'n/i')}), arquivo {pol.get('arquivo', 'n/i')}"],
        ["Data de revisão da política", f"{data_br(pol['data_revisao'])}. {pol.get('fonte_data_revisao', '')}"],
        ["Data-base da comparação", data_br(rev["data_base"])],
        ["Data de referência", f"{data_br(ref_iso)} ({'replay' if rev['modo'] == 'replay' else 'revisão atual'})"],
        ["Achados por severidade", "  ".join(f"{ROTULO_SEV[s]}: {c[s]}" for s in SEVERIDADES)],
    ]
    t = Table([[p(a, "celb"), p(b, "cel")] for a, b in dados], colWidths=[4.6 * cm, largura - 4.6 * cm])
    t.setStyle(ficha)
    h += [t, Spacer(1, 6), p(res.get("resumo", ""))]

    # (b) achados
    h.append(p("2. Achados", "h2"))
    achados = ordenar_achados(res["achados"])
    linhas = [[p(x, "celb") for x in ("Id", "Cláusula", "Fonte principal", "Severidade", "Prazo")]]
    for a in achados:
        f0 = (a.get("fontes") or [{}])[0]
        linhas.append([p(a["id"], "cel"), p(a["clausula"]["ref"], "cel"), p(fonte_txt(f0), "cel"),
                       sev(a["severidade"]), p(prazo_txt(a.get("prazo"), ref_iso), "cel")])
    t = Table(linhas, colWidths=[1.0 * cm, 2.0 * cm, 7.2 * cm, 2.0 * cm, largura - 12.2 * cm], repeatRows=1)
    t.setStyle(grade)
    h += [t, Spacer(1, 8)]
    for a in achados:
        fontes = a.get("fontes") or [{}]
        corpo = [
            [p("Cláusula atual", "celb"), p(f"{a['clausula']['ref']}: {a['clausula'].get('trecho', '')}", "cel")],
            [p("O que a regra exige hoje", "celb"), p(a.get("exige_hoje", ""), "cel")],
            [p("Fontes", "celb"), [x for f in fontes for x in (p(fonte_txt(f), "cel"), link(f.get("source_url")))]],
            [p("Severidade", "celb"), sev(a["severidade"])],
            *([[p("Critério", "celb"), p(f"{a['criterio']}: {CRITERIOS[a['criterio']]}", "cel")]]
              if a.get("criterio") in CRITERIOS else []),
            [p("Situação da regra", "celb"),
             p("a vigorar" if a.get("situacao") == "a_vigorar" else "vigente na data de referência", "cel")],
            [p("Prazo", "celb"), p(prazo_txt(a.get("prazo"), ref_iso), "cel")],
            [p("Nova redação proposta", "celb"),
             p(a.get("nova_redacao") or "Sem alteração proposta.", "cel")],
        ]
        t = Table(corpo, colWidths=[4.0 * cm, largura - 4.0 * cm])
        t.setStyle(ficha)
        titulo = f"{a['id']}  |  {a.get('conceito', '')}  |  cláusula {a['clausula']['ref']}"
        h.append(KeepTogether([p(titulo, "h3"), t]))
        h.append(Spacer(1, 4))

    # (c) alterações
    h.append(p("3. O que mudou desde a última revisão", "h2"))
    h.append(p(f"Alterações nos dispositivos tocados pela política entre {data_br(rev['data_base'])} e "
               f"{data_br(ref_iso)}. Datas posteriores à data de referência aparecem como 'a vigorar'."))
    h.append(Spacer(1, 4))
    linhas = [[p(x, "celb") for x in ("Data", "Ato", "Dispositivos", "O que mudou", "Achados")]]
    for m in sorted(res["alteracoes"], key=lambda m: m.get("data") or ""):
        ato = m.get("ato_fonte") or {}
        linhas.append([p(quando_txt(m, ref_iso), "cel"), p(ato.get("citacao", "[CITAÇÃO PENDENTE]"), "cel"),
                       p(m.get("alvo", ""), "cel"), p(f"{m.get('tipo', '')}: {m.get('comentario', '')}", "cel"),
                       p(", ".join(m.get("achados") or []), "cel")])
    t = Table(linhas, colWidths=[2.4 * cm, 2.8 * cm, 4.6 * cm, largura - 11.6 * cm, 1.8 * cm], repeatRows=1)
    t.setStyle(grade)
    h.append(t)

    # (d) exposição
    h.append(p("4. Exposição judicial", "h2"))
    if not res["exposicao"]:
        h.append(p("[NÃO ENCONTRADO] Nenhum precedente pertinente localizado no acervo."))
    for e in res["exposicao"]:
        h.append(p(f"Achados {', '.join(e.get('achados') or [])}: {e.get('tese', '')}", "h3"))
        for pr in e.get("precedentes") or []:
            efic = f", eficácia {pr['eficacia']}" if pr.get("eficacia") else ""
            h.append(p(f"{pr.get('citacao')} ({(pr.get('tipo') or '').replace('_', ' ')}{efic}, {data_br(pr.get('data'))}): "
                       f"{pr.get('trecho', '')}", "cel"))
            h.append(link(pr.get("source_url")))
            h.append(Spacer(1, 3))

    # (e) tarefas
    h.append(p("5. Tarefas por responsável", "h2"))
    for chave, nome in RESPONSAVEIS.items():
        ts = [t for t in res["tarefas"] if t["responsavel"] == chave]
        if not ts:
            continue
        h.append(p(nome, "h3"))
        linhas = [[p(x, "celb") for x in ("Tarefa", "Achados", "Prazo", "Base do prazo")]]
        for t_ in sorted(ts, key=lambda t_: t_.get("prazo") or "9999"):
            pr = data_br(t_.get("prazo")) if t_.get("prazo") else "sem prazo regulatório"
            if t_.get("prazo") and t_["prazo"] <= ref_iso:
                pr += " (vencido)"
            linhas.append([p(t_["tarefa"], "cel"), p(", ".join(t_.get("achados") or []), "cel"),
                           p(pr, "cel"), p(t_.get("base_prazo", ""), "cel")])
        tb = Table(linhas, colWidths=[largura - 10.4 * cm, 1.8 * cm, 3.4 * cm, 5.2 * cm], repeatRows=1)
        tb.setStyle(grade)
        h.append(tb)

    # (f) auditoria
    aud = res["auditoria"]
    h.append(p("6. Registro de auditoria", "h2"))
    dados = [
        ["Data de referência", f"{data_br(ref_iso)} ({linha_modo(rev)})"],
        ["Gerado em", data_br(rev.get("gerado_em"))],
        ["Ferramentas de conformidade", "usadas" if rev.get("conformidade_disponivel") else "indisponíveis (ver aviso)"],
        ["Ferramentas usadas", ", ".join(aud.get("ferramentas") or [])],
        ["O que foi verificado", "\n".join("- " + v for v in aud.get("verificacoes") or [])],
        ["Não encontrado", "\n".join("- " + v for v in aud.get("nao_encontrado") or []) or "nada"],
        ["Limitações", "\n".join("- " + v for v in aud.get("limitacoes") or [])],
    ]
    fontes = sorted({f["source_url"] for a in res["achados"] for f in a.get("fontes") or [] if f.get("source_url")})
    t = Table([[p(a, "celb"), p(b, "cel")] for a, b in dados] +
              [[p("Fontes consultadas", "celb"), [link(u) for u in fontes]]],
              colWidths=[4.6 * cm, largura - 4.6 * cm])
    t.setStyle(ficha)
    h.append(t)
    h.append(Spacer(1, 8))
    h.append(p("Rascunho para revisão e aprovação humanas. Não é aconselhamento jurídico. Cada afirmação "
               "remete ao ato, ao dispositivo e à data; o que não foi encontrado está marcado.", "sub"))

    rodape = (f"Letra da Lei | {pol['titulo']} | referência {data_br(ref_iso)}"
              + (" | DOCUMENTO DE EXEMPLO" if res.get("exemplo") else ""))

    def pagina(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#667085"))
        canvas.drawString(1.8 * cm, 1.1 * cm, rodape)
        canvas.drawRightString(A4[0] - 1.8 * cm, 1.1 * cm, f"página {doc.page}")
        canvas.restoreState()

    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    doc = SimpleDocTemplate(caminho, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm,
                            topMargin=1.6 * cm, bottomMargin=1.8 * cm, title=titulo_doc(res),
                            author="Letra da Lei, skill revisao-politica")
    doc.build(h, onFirstPage=pagina, onLaterPages=pagina)
    return caminho


# ---------------------------------------------------------------- DOCX

def gerar_docx(res: dict, caminho: str) -> str:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from montar_docx import bloco_citacao, nova_peca, paragrafo, salvar, titulo

    pol, rev = res["politica"], res["revisao"]
    ref_iso = rev["data_referencia"]
    doc = nova_peca(corpo_pt=11, fonte="Calibri")

    def tabela(cabecalho, linhas):
        t = doc.add_table(rows=1, cols=len(cabecalho))
        t.style = "Table Grid"
        for i, c in enumerate(cabecalho):
            t.rows[0].cells[i].text = c
            for r in t.rows[0].cells[i].paragraphs[0].runs:
                r.bold = True
        for linha in linhas:
            cel = t.add_row().cells
            for i, v in enumerate(linha):
                cel[i].text = v or ""
        doc.add_paragraph()

    if res.get("exemplo"):
        paragrafo(doc, "DOCUMENTO DE EXEMPLO, SEM RELAÇÃO COM INSTITUIÇÃO REAL", negrito=True, centralizado=True)
    titulo(doc, titulo_doc(res))
    paragrafo(doc, f"{pol.get('instituicao', '')} | {linha_modo(rev)}", centralizado=True)
    aviso = aviso_ferramentas(rev)
    if aviso:
        paragrafo(doc, "[ATENÇÃO] Aviso sobre as fontes: " + aviso)

    paragrafo(doc, "1. Resumo", negrito=True)
    c = contagem(res)
    tabela(["Campo", "Valor"], [
        ["Política", f"{pol['titulo']} (versão {pol.get('versao', 'n/i')}), arquivo {pol.get('arquivo', 'n/i')}"],
        ["Data de revisão da política", f"{data_br(pol['data_revisao'])}. {pol.get('fonte_data_revisao', '')}"],
        ["Data-base da comparação", data_br(rev["data_base"])],
        ["Data de referência", data_br(ref_iso)],
        ["Achados por severidade", "  ".join(f"{ROTULO_SEV[s]}: {c[s]}" for s in SEVERIDADES)],
    ])
    paragrafo(doc, res.get("resumo", ""))

    paragrafo(doc, "2. Achados", negrito=True)
    for a in ordenar_achados(res["achados"]):
        paragrafo(doc, f"{a['id']} | {a.get('conceito', '')} | cláusula {a['clausula']['ref']} | "
                       f"severidade {ROTULO_SEV[a['severidade']]}", negrito=True)
        bloco_citacao(doc, a["clausula"].get("trecho", ""), f"Fonte: política, cláusula {a['clausula']['ref']}",
                      corpo_pt=11)
        paragrafo(doc, "O que a regra exige hoje: " + a.get("exige_hoje", ""))
        for f in a.get("fontes") or [{}]:
            paragrafo(doc, "Fonte: " + fonte_txt(f) + (f" | {f['source_url']}" if f.get("source_url") else ""))
        if a.get("criterio") in CRITERIOS:
            paragrafo(doc, f"Critério: {a['criterio']}: {CRITERIOS[a['criterio']]}")
        paragrafo(doc, "Prazo: " + prazo_txt(a.get("prazo"), ref_iso))
        paragrafo(doc, "Nova redação proposta:", negrito=True)
        paragrafo(doc, a.get("nova_redacao") or "Sem alteração proposta.")

    paragrafo(doc, "3. O que mudou desde a última revisão", negrito=True)
    tabela(["Data", "Ato", "Dispositivos", "O que mudou", "Achados"], [
        [quando_txt(m, ref_iso),
         (m.get("ato_fonte") or {}).get("citacao", "[CITAÇÃO PENDENTE]"), m.get("alvo", ""),
         f"{m.get('tipo', '')}: {m.get('comentario', '')}", ", ".join(m.get("achados") or [])]
        for m in sorted(res["alteracoes"], key=lambda m: m.get("data") or "")])

    paragrafo(doc, "4. Exposição judicial", negrito=True)
    for e in res["exposicao"]:
        paragrafo(doc, f"Achados {', '.join(e.get('achados') or [])}: {e.get('tese', '')}", negrito=True)
        for pr in e.get("precedentes") or []:
            efic = f" | eficácia: {pr['eficacia']}" if pr.get("eficacia") else ""
            bloco_citacao(doc, pr.get("trecho", ""),
                          f"Fonte: {pr.get('citacao')} | {data_br(pr.get('data'))} | search_id: "
                          f"{pr.get('search_id', 'n/i')}{efic} | {pr.get('source_url', '')}", corpo_pt=11)

    paragrafo(doc, "5. Tarefas por responsável", negrito=True)
    for chave, nome in RESPONSAVEIS.items():
        ts = [t for t in res["tarefas"] if t["responsavel"] == chave]
        if ts:
            paragrafo(doc, nome, negrito=True)
            tabela(["Tarefa", "Achados", "Prazo", "Base do prazo"], [
                [t["tarefa"], ", ".join(t.get("achados") or []),
                 (data_br(t["prazo"]) + (" (vencido)" if t["prazo"] <= ref_iso else "")) if t.get("prazo")
                 else "sem prazo regulatório", t.get("base_prazo", "")]
                for t in sorted(ts, key=lambda t: t.get("prazo") or "9999")])

    aud = res["auditoria"]
    paragrafo(doc, "6. Registro de auditoria", negrito=True)
    paragrafo(doc, f"Data de referência: {data_br(ref_iso)}. Gerado em {data_br(rev.get('gerado_em'))}. "
                   f"Ferramentas de conformidade: {'usadas' if rev.get('conformidade_disponivel') else 'indisponíveis'}.")
    paragrafo(doc, "Ferramentas usadas: " + ", ".join(aud.get("ferramentas") or []))
    for rotulo, chave in (("Verificado", "verificacoes"), ("Não encontrado", "nao_encontrado"),
                          ("Limitações", "limitacoes")):
        for v in aud.get(chave) or []:
            paragrafo(doc, f"{rotulo}: {v}")
    return salvar(doc, caminho)


# ---------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("resultado", help="JSON do resultado da revisão")
    ap.add_argument("--pdf", help="caminho do PDF (padrão: outputs/...)")
    ap.add_argument("--docx", help="caminho do .docx (padrão: outputs/...)")
    ap.add_argument("--sem-docx", action="store_true", help="gera só o PDF")
    args = ap.parse_args(argv)

    with open(args.resultado, encoding="utf-8") as fh:
        res = json.load(fh)
    try:
        avisos = validar(res)
    except ResultadoInvalido as e:
        sys.exit(f"Resultado inválido: {e}")
    base = os.path.join("outputs", f"revisao-politica-{slug(res['politica']['titulo'])}-{res['revisao']['data_referencia']}")
    pdf = gerar_pdf(res, args.pdf or base + ".pdf")
    print(pdf)
    if not args.sem_docx:
        print(gerar_docx(res, args.docx or base + ".docx"))
    for a in avisos:
        print("aviso:", a, file=sys.stderr)


if __name__ == "__main__":
    main()
