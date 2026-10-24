"""Testes do renderizador do pacote da skill revisao-politica.

Rodar (da raiz do plugin, plugins/letradalei):
    python -m unittest discover -s scripts/tests -v

Requer reportlab e python-docx; pypdf é opcional (confere o texto do PDF).
"""
import copy
import json
import os
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(AQUI)
sys.path.insert(0, SCRIPTS)

import montar_pacote_conformidade as m  # noqa: E402

EXEMPLO = os.path.join(SCRIPTS, "..", "skills", "revisao-politica", "exemplos", "resultado-exemplo.json")


def carregar():
    with open(EXEMPLO, encoding="utf-8") as fh:
        return json.load(fh)


class TestRenderizador(unittest.TestCase):
    def setUp(self):
        self.res = carregar()
        self.tmp = tempfile.mkdtemp()

    def test_exemplo_valido(self):
        self.assertEqual(m.validar(self.res), [])

    def test_pdf_e_docx(self):
        pdf = m.gerar_pdf(self.res, os.path.join(self.tmp, "pacote.pdf"))
        with open(pdf, "rb") as fh:
            self.assertEqual(fh.read(4), b"%PDF")
        try:
            from pypdf import PdfReader
        except ImportError:
            PdfReader = None
        if PdfReader:
            texto = "\n".join(pg.extract_text() for pg in PdfReader(pdf).pages)
            for esperado in ("1. Resumo", "2. Achados", "3. O que mudou", "4. Exposição judicial",
                             "5. Tarefas por responsável", "6. Registro de auditoria",
                             "Res. BCB 142/2021, art. 2º-A", "Aviso sobre as fontes", "DOCUMENTO DE EXEMPLO"):
                self.assertIn(esperado, texto)
        docx_path = m.gerar_docx(self.res, os.path.join(self.tmp, "pacote.docx"))
        from docx import Document
        corpo = "\n".join(p.text for p in Document(docx_path).paragraphs)
        self.assertIn("Nova redação proposta", corpo)
        self.assertIn("Res. BCB 559/2026", corpo)

    def test_replay_e_conformidade_disponivel(self):
        r = copy.deepcopy(self.res)
        r["revisao"].update(modo="replay", data_referencia="2026-07-01", conformidade_disponivel=True)
        pdf = m.gerar_pdf(r, os.path.join(self.tmp, "replay.pdf"))
        try:
            from pypdf import PdfReader
        except ImportError:
            return
        texto = "\n".join(pg.extract_text() for pg in PdfReader(pdf).pages)
        self.assertIn("Replay", texto)
        self.assertNotIn("Aviso sobre as fontes", texto)
        self.assertIn("a vigorar", texto)  # alterações de 2026-09-18 e 2027-02-01 ficam depois da referência

    def test_fonte_ausente_vira_citacao_pendente(self):
        r = copy.deepcopy(self.res)
        r["achados"][0]["fontes"] = [{"citacao": "Res. BCB 142/2021, art. 2º-A"}]
        avisos = m.validar(r)
        self.assertTrue(any("CITAÇÃO PENDENTE" in a for a in avisos))
        self.assertTrue(m.fonte_txt(r["achados"][0]["fontes"][0]).startswith("[CITAÇÃO PENDENTE]"))

    def test_invalidos(self):
        r = copy.deepcopy(self.res)
        r["achados"][0]["severidade"] = "critica"
        with self.assertRaises(m.ResultadoInvalido):
            m.validar(r)
        r = copy.deepcopy(self.res)
        del r["revisao"]["conformidade_disponivel"]
        with self.assertRaises(m.ResultadoInvalido):
            m.validar(r)
        r = copy.deepcopy(self.res)
        r["tarefas"][0]["responsavel"] = "ti"
        with self.assertRaises(m.ResultadoInvalido):
            m.validar(r)


if __name__ == "__main__":
    unittest.main()
