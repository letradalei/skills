"""Prepare a backtest round: sandbox inputs, the conformidade CLI, and one rendered prompt per run.

Usage:
  python3 -I preparar.py --work <dir> --data-referencia 2026-10-24 --runs 3 \
      --platform /path/to/platform-worktree --dburl-file <file holding the TEST branch URL>

Writes <work>/sandbox/{politica.txt,esquema-neutro.md}, <work>/bin/conformidade-local(.sh),
<work>/runs/<id>/ (one per contender run) and <work>/prompts/<id>.md. Run ids are anonymized
(R01..R09) so the grader does not know which contender wrote which output; the mapping goes to
<work>/mapa.json, which the grader never reads.
"""
import argparse
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POLICY = HERE.parents[2] / "plugins/letradalei/skills/revisao-politica/exemplos/politica-prevencao-fraudes-exemplo.docx"
CONTENDERS = {"a": "AI + busca na web", "b": "AI + ferramentas públicas da Letra da Lei", "c": "AI + grafo de conceitos (conformidade)"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--data-referencia", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--platform", required=True)
    ap.add_argument("--dburl-file", required=True)
    ap.add_argument("--seed", type=int, default=20261024)
    a = ap.parse_args()

    work = Path(a.work).resolve()
    sandbox = work / "sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)
    with open(sandbox / "politica.txt", "w") as f:
        subprocess.run([sys.executable, "-I", str(HERE / "extrair_politica.py"), str(POLICY)], stdout=f, check=True)
    shutil.copy(HERE / "esquema-neutro.md", sandbox / "esquema-neutro.md")

    (work / "bin").mkdir(exist_ok=True)
    cli = work / "bin" / "conformidade-local"
    subprocess.run([str(HERE / "conformidade-cli/build.sh"), a.platform, str(cli)], check=True)

    base = (HERE / "prompts/contender.md").read_text()
    runs = [(c, i) for c in CONTENDERS for i in range(1, a.runs + 1)]
    ids = [f"R{n:02d}" for n in range(1, len(runs) + 1)]
    random.Random(a.seed).shuffle(ids)
    mapa = {}
    (work / "prompts").mkdir(exist_ok=True)
    for (c, i), rid in zip(runs, ids):
        out = work / "runs" / rid
        out.mkdir(parents=True, exist_ok=True)
        tools = (HERE / f"prompts/tools-{c}.md").read_text()
        tools = tools.replace("{CLI}", f"{cli}.sh").replace("{DBURL_FILE}", str(Path(a.dburl_file).resolve()))
        p = (base.replace("{TOOLS}", tools).replace("{CONTENDER}", rid).replace("{SANDBOX}", str(sandbox))
             .replace("{OUTDIR}", str(out)).replace("{DATA_REFERENCIA}", a.data_referencia))
        (work / "prompts" / f"{rid}.md").write_text(p)
        mapa[rid] = {"contender": c, "descricao": CONTENDERS[c], "rodada": i}
    (work / "mapa.json").write_text(json.dumps(dict(sorted(mapa.items())), indent=2, ensure_ascii=False))
    print(json.dumps(dict(sorted(mapa.items())), ensure_ascii=False))


if __name__ == "__main__":
    main()
