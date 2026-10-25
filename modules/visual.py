"""Visualisasi ciphertext sebagai gambar noise (bukti visual bahwa isi foto tidak bocor)."""
import base64
import math
from collections import Counter

from PIL import Image

MAX_SIDE = 192


def ciphertext_to_image(ciphertext: bytes, target: int = 256) -> Image.Image:
    """Tampilkan byte ciphertext apa adanya sebagai piksel RGB (3 byte = 1 piksel)."""
    data = ciphertext[: MAX_SIDE * MAX_SIDE * 3]
    side = max(8, math.ceil(math.sqrt(math.ceil(len(data) / 3))))
    data = data.ljust(side * side * 3, b"\x00")
    img = Image.frombytes("RGB", (side, side), data)
    scale = max(1, target // side)
    return img.resize((side * scale, side * scale), Image.NEAREST) if scale > 1 else img


def byte_entropy(data: bytes) -> float:
    """Entropi Shannon dalam bit/byte (maksimum 8 = tidak berpola)."""
    if not data:
        return 0.0
    n = len(data)
    return -sum((c / n) * math.log2(c / n) for c in Counter(data).values())


def base64_preview(ciphertext: bytes, n: int = 240) -> str:
    text = base64.b64encode(ciphertext).decode()
    return text[:n] + ("…" if len(text) > n else "")
