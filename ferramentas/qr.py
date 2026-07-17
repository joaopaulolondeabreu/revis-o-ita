"""Geração e decodificação de QR Codes, sem serviço externo.

Gerar:      python qr.py gerar <url> <saida.png>
Decodificar: python qr.py decodificar <imagem.png>  (imprime a URL lida)
"""

import sys
from pathlib import Path

import cv2
import numpy as np
import qrcode
from PIL import Image


def gerar_qr(url: str, saida: Path) -> Path:
    """QR preto sobre branco, margem de silêncio de 4 módulos, correção de erro alta."""
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=12,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(saida)
    return saida


def decodificar_qr(imagem: Path) -> str | None:
    pil = Image.open(imagem).convert("RGB")
    arr = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    detector = cv2.QRCodeDetector()
    texto, pontos, _ = detector.detectAndDecode(arr)
    return texto or None


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "gerar":
        gerar_qr(sys.argv[2], Path(sys.argv[3]))
        print(f"QR gerado: {sys.argv[3]}")
    elif len(sys.argv) >= 3 and sys.argv[1] == "decodificar":
        texto = decodificar_qr(Path(sys.argv[2]))
        if texto is None:
            print("ERRO: QR não pôde ser lido", file=sys.stderr)
            sys.exit(1)
        print(texto)
    else:
        print(__doc__)
        sys.exit(2)
