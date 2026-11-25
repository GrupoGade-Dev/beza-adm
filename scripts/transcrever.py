#!/usr/bin/env python3
"""Transcreve uma gravação (áudio/vídeo) para texto, localmente, com o Whisper.

Uso: python3 transcrever.py gravacao.mp4 saida.txt [modelo]
Modelo padrão: small (bom equilíbrio entre velocidade e qualidade em português).
Requer: ffmpeg e `pip install openai-whisper`. Nada é enviado para a internet; só o
modelo é baixado na primeira execução.
"""
import shutil
import sys


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    if not shutil.which("ffmpeg"):
        sys.exit("Falta o ffmpeg. Mac: brew install ffmpeg · Windows: winget install ffmpeg")
    try:
        import whisper
    except ImportError:
        sys.exit("Falta o Whisper. Instale com:  python3 -m pip install openai-whisper")
    modelo = sys.argv[3] if len(sys.argv) > 3 else "small"
    m = whisper.load_model(modelo)
    r = m.transcribe(sys.argv[1], language="pt", verbose=False)
    linhas = []
    for seg in r["segments"]:
        t = int(seg["start"])
        linhas.append(f"[{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}] {seg['text'].strip()}")
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"OK: {sys.argv[2]} ({len(linhas)} trechos). Atenção: nomes próprios costumam sair errados; revise.")


if __name__ == "__main__":
    main()
