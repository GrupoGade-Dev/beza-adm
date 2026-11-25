#!/usr/bin/env python3
"""Converte um HTML em PDF usando o Chrome ou o Edge já instalados (sem instalar nada).

Uso: python3 html2pdf.py entrada.html saida.pdf
"""
import os
import shutil
import subprocess
import sys

CANDIDATOS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def achar_navegador():
    for c in CANDIDATOS:
        if os.path.exists(c):
            return c
    for nome in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        achado = shutil.which(nome)
        if achado:
            return achado
    return None


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    entrada, saida = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    nav = achar_navegador()
    if not nav:
        sys.exit("Não encontrei Chrome nem Edge neste computador. Instale um deles ou abra o HTML e use Imprimir > Salvar como PDF.")
    cmd = [nav, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={saida}", "file://" + entrada.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not os.path.exists(saida):
        sys.exit(f"Falha ao gerar o PDF.\n{r.stderr[-500:]}")
    print(f"OK: {saida}")


if __name__ == "__main__":
    main()
