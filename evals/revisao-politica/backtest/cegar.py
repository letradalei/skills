"""Copy each run's resultado.json to <work>/grading/Rxx.json for the grader, without the fields that name
the tools used (auditoria.ferramentas, revisao.aviso_ferramentas, revisao.conformidade_disponivel), so the
grader scores blind. Usage: python3 -I cegar.py --work <dir>"""
import argparse
import json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--work", required=True)
work = Path(ap.parse_args().work)
(work / "grading").mkdir(exist_ok=True)
for run in sorted((work / "runs").iterdir()):
    try:
        d = json.loads((run / "resultado.json").read_text())
    except (OSError, ValueError) as e:
        print(f"{run.name}: sem resultado válido ({e})")
        continue
    d.get("auditoria", {}).pop("ferramentas", None)
    for k in ("aviso_ferramentas", "conformidade_disponivel"):
        d.get("revisao", {}).pop(k, None)
    (work / "grading" / f"{run.name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2))
    print(run.name, len(d.get("achados", [])), "achados")
