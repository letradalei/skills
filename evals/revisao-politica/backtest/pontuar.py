"""Aggregate a backtest round into results.md and divergencias.md.

Usage: python3 -I pontuar.py --work <dir> --out <dir>

Reads <work>/mapa.json (anonymized run id -> contender), <work>/runs/Rxx/{resultado.json,inicio.txt,
fim.txt,log.txt}, the grader's <work>/grader/{verificacao-gabarito.json,pontuacao-Rxx.json} and
<work>/custos.json ({"Rxx": {"tokens": n, "usd": x}} from the agent runs). Mechanical checks
(provenance fields, official domains, time) are computed here; recall and false findings come from
the grader's judgments.
"""
import argparse
import itertools
import json
import statistics
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

G = ["G1", "G2", "G3", "G4", "G5"]
BONUS = ["B1", "B2", "B3"]
OFFICIAL = ("bcb.gov.br", "planalto.gov.br", "in.gov.br", "stj.jus.br", "stf.jus.br", "jus.br", "leg.br", "gov.br")
NAMES = {"a": "(a) AI + busca na web", "b": "(b) AI + ferramentas públicas (vetorial)", "c": "(c) AI + grafo de conceitos"}


def load(p: Path, default=None):
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return default


def minutes(run: Path):
    try:
        a = datetime.fromisoformat((run / "inicio.txt").read_text().strip().replace("Z", "+00:00"))
        b = datetime.fromisoformat((run / "fim.txt").read_text().strip().replace("Z", "+00:00"))
        return (b - a).total_seconds() / 60
    except (OSError, ValueError):
        return None


def provenance(res: dict):
    fontes = [f for a in res.get("achados", []) for f in a.get("fontes", [])]
    sem_fonte = sum(1 for a in res.get("achados", []) if not a.get("fontes"))
    completas = sum(1 for f in fontes if f.get("citacao") and f.get("vigencia") and f.get("source_url"))
    oficiais = sum(1 for f in fontes if any(urlparse(f.get("source_url") or "").netloc.endswith(d) for d in OFFICIAL))
    return {"fontes": len(fontes), "completas": completas, "oficiais": oficiais, "achados_sem_fonte": sem_fonte}


def val(x):
    """grader verdicts: true = 1, "parcial" = 0.5, anything else = 0."""
    if x is True:
        return 1.0
    if isinstance(x, str) and x.lower().startswith("parc"):
        return 0.5
    return 0.0


def mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def fmt(x, pct=False, nd=1):
    if x is None:
        return "n/d"
    return f"{100 * x:.0f}%" if pct else f"{x:.{nd}f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--notas", help="markdown appended to results.md (reading of the round, written by hand)")
    ap.add_argument("--resumo-divergencias", help="markdown put at the top of divergencias.md (consolidated, by hand)")
    a = ap.parse_args()
    work, out = Path(a.work), Path(a.out)
    mapa = load(work / "mapa.json")
    custos = load(work / "custos.json", {})
    verif = load(work / "grader/verificacao-gabarito.json", {})

    per_run = {}
    for rid, m in mapa.items():
        run = work / "runs" / rid
        res = load(run / "resultado.json", {})
        sc = load(work / "grader" / f"pontuacao-{rid}.json", {})
        itens = sc.get("itens", {})
        found = {g for g in G if val(itens.get(g, {}).get("encontrado")) == 1}
        strict = {g for g in G if all(itens.get(g, {}).get(k) is True for k in ("encontrado", "clausula_ok", "ato_artigo_ok", "data_ok"))}
        nc = sc.get("nao_casados", [])
        sev = {}
        for ach in res.get("achados", []):
            sev[ach.get("severidade")] = sev.get(ach.get("severidade"), 0) + 1
        try:
            calls = sum(1 for line in (run / "log.txt").read_text().splitlines() if line.strip())
        except OSError:
            calls = None
        pa = sc.get("proveniencia_amostra", {})
        per_run[rid] = {
            "contender": m["contender"], "rodada": m["rodada"], "valido": bool(res),
            "found": found, "strict": strict,
            "clausula": sum(val(itens[g].get("clausula_ok")) for g in found),
            "ato": sum(val(itens[g].get("ato_artigo_ok")) for g in found),
            "data": sum(val(itens[g].get("data_ok")) for g in found),
            "bonus": {b for b in BONUS if val(itens.get(b, {}).get("encontrado")) == 1},
            "falsos": sum(1 for x in nc if x.get("classe") == "falso"),
            "extras": sum(1 for x in nc if x.get("classe") == "extra_valido"),
            "duvidosos": sum(1 for x in nc if x.get("classe") == "duvidoso"),
            "sev": sev, "prov": provenance(res), "prov_amostra": (pa.get("ok"), pa.get("total")),
            "min": minutes(run), "calls": calls,
            "tokens": custos.get(rid, {}).get("tokens"), "usd": custos.get(rid, {}).get("usd"),
            "div": sc.get("divergencias_com_gabarito", []),
        }

    L = []
    L.append("# Backtest, revisão da política de exemplo: resultados\n")
    L.append("Política fictícia (Exemplo Pagamentos IP S.A., aprovada em 2025-03-18), revista na data de referência "
             "indicada abaixo; 3 rodadas por competidor; saídas anônimas (R01..R09) pontuadas por um avaliador "
             "independente que leu só o gabarito e fontes oficiais (bcb.gov.br, planalto.gov.br, stj.jus.br).\n")
    L.append("## Resumo por competidor (média das 3 rodadas)\n")
    L.append("| Competidor | Recall G1-G5 (achou) | Recall estrito (cláusula+ato+data) | Cláusula ok | Ato/artigo ok | Data ok | Bônus B1-B3 | Falsos | Extras válidos | Consistência: achou (itens com as 3 rodadas de acordo) | Consistência: estrito | Jaccard médio entre rodadas | Fontes completas | Links oficiais | Amostra de links conferida | Tempo (min) | Chamadas | Tokens | Custo aprox. (USD) |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for c in "abc":
        rs = [r for r in per_run.values() if r["contender"] == c]
        if not rs:
            continue
        agree = sum(1 for g in G if len({g in r["found"] for r in rs}) == 1) / len(G)
        agree_s = sum(1 for g in G if len({g in r["strict"] for r in rs}) == 1) / len(G)
        pairs = list(itertools.combinations(rs, 2))
        jac = mean([len(x["found"] & y["found"]) / len(x["found"] | y["found"]) if (x["found"] | y["found"]) else 1.0 for x, y in pairs])
        fontes = sum(r["prov"]["fontes"] for r in rs)
        comp = sum(r["prov"]["completas"] for r in rs) / fontes if fontes else None
        ofi = sum(r["prov"]["oficiais"] for r in rs) / fontes if fontes else None
        aok = sum(r["prov_amostra"][0] or 0 for r in rs)
        atot = sum(r["prov_amostra"][1] or 0 for r in rs)
        L.append("| " + " | ".join([
            NAMES[c],
            fmt(mean([len(r["found"]) for r in rs])) + "/5",
            fmt(mean([len(r["strict"]) for r in rs])) + "/5",
            fmt(mean([r["clausula"] for r in rs])), fmt(mean([r["ato"] for r in rs])), fmt(mean([r["data"] for r in rs])),
            fmt(mean([len(r["bonus"]) for r in rs])) + "/3",
            fmt(mean([r["falsos"] for r in rs])), fmt(mean([r["extras"] for r in rs])),
            fmt(agree, pct=True), fmt(agree_s, pct=True), fmt(jac, nd=2), fmt(comp, pct=True), fmt(ofi, pct=True),
            f"{aok}/{atot}" if atot else "n/d",
            fmt(mean([r["min"] for r in rs])), fmt(mean([r["calls"] for r in rs]), nd=0),
            fmt(mean([r["tokens"] for r in rs]), nd=0), fmt(mean([r["usd"] for r in rs]), nd=2),
        ]) + " |")
    L.append("\n## Por rodada\n")
    L.append("| Rodada | Competidor | G achados | Estritos | Bônus | Falsos | Extras | Duvidosos | Achados por severidade | Fontes (completas/oficiais/total) | Tempo (min) | Tokens | USD |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for rid, r in sorted(per_run.items(), key=lambda kv: (kv[1]["contender"], kv[1]["rodada"])):
        p = r["prov"]
        L.append(f"| {rid} | {r['contender']}{r['rodada']} | {','.join(sorted(r['found'])) or '-'} | {','.join(sorted(r['strict'])) or '-'} | "
                 f"{','.join(sorted(r['bonus'])) or '-'} | {r['falsos']} | {r['extras']} | {r['duvidosos']} | "
                 f"{', '.join(f'{k}:{v}' for k, v in sorted(r['sev'].items(), key=lambda kv: str(kv[0])))} | "
                 f"{p['completas']}/{p['oficiais']}/{p['fontes']} | {fmt(r['min'])} | {r['tokens'] or 'n/d'} | {fmt(r['usd'], nd=2)} |")
    L.append("\n## Recall por item do gabarito (rodadas que acharam, de 3)\n")
    L.append("| Item | " + " | ".join(NAMES[c] for c in "abc") + " |")
    L.append("|---|---|---|---|")
    for g in G + BONUS:
        cells = []
        for c in "abc":
            rs = [r for r in per_run.values() if r["contender"] == c]
            key = "bonus" if g in BONUS else "found"
            n = sum(1 for r in rs if g in r[key])
            s = "" if g in BONUS else f" (estrito {sum(1 for r in rs if g in r['strict'])})"
            cells.append(f"{n}/{len(rs)}{s}")
        L.append(f"| {g} | " + " | ".join(cells) + " |")
    if a.notas:
        L.append("\n" + Path(a.notas).read_text())
    (out / "results.md").write_text("\n".join(L) + "\n")

    D = ["# Divergências entre o avaliador e o gabarito (para o Julio)\n",
         "Listadas, não resolvidas. Fonte: conferência do gabarito na fonte oficial (passo 1) e as divergências "
         "que o avaliador registrou ao pontuar cada saída (passo 2).\n"]
    if a.resumo_divergencias:
        D.append(Path(a.resumo_divergencias).read_text())
    D.append("## Passo 1, conferência do gabarito (bruto)\n")
    for it in verif.get("itens", []):
        if it.get("confere") is not True or it.get("divergencia"):
            ev = "; ".join(e.get("url", "") for e in it.get("evidencia", [])[:3])
            D.append(f"- **{it.get('id')}** (confere: {it.get('confere')}): {it.get('divergencia')} [{ev}]")
    for x in verif.get("nao_conferido", []):
        D.append(f"- Não conferido: {x}")
    D.append("\n## Passo 2, ao pontuar as saídas (bruto, por rodada)\n")
    for rid, r in sorted(per_run.items()):
        for d in r["div"]:
            D.append(f"- {rid}, {d.get('item')}: {d.get('o_que')} [{d.get('evidencia_url')}]")
    (out / "divergencias.md").write_text("\n".join(D) + "\n")
    print((out / "results.md").read_text())


if __name__ == "__main__":
    main()
