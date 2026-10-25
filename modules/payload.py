"""Pembungkus isi pesan: teks (+ foto opsional) menjadi satu blok byte sebelum dienkripsi.

Foto dan teks dienkripsi SEKALIGUS dalam satu paket AES-256-GCM, jadi satu tag
melindungi keduanya: mengubah satu byte foto atau teks membuat dekripsi gagal.
Format: MAGIC(4) | panjang header(4) | header JSON | byte foto
"""
import io
import json
import struct
from typing import Optional, Tuple

from PIL import Image

MAGIC = b"EMB1"
MAX_IMAGE_BYTES = 2 * 1024 * 1024
MAX_PIXELS = 25_000_000
MAX_TEXT_CHARS = 5000
ALLOWED = {"PNG": "image/png", "JPEG": "image/jpeg", "WEBP": "image/webp"}


class PayloadError(ValueError):
    """Isi pesan tidak valid (bukan gambar, terlalu besar, atau format rusak)."""


def inspect_image(data: bytes) -> str:
    """Pastikan data benar-benar gambar PNG/JPEG/WEBP yang wajar; kembalikan MIME-nya."""
    if len(data) > MAX_IMAGE_BYTES:
        raise PayloadError("Ukuran foto maksimal 2 MB.")
    try:
        with Image.open(io.BytesIO(data)) as im:
            fmt, size = im.format, im.size
            im.verify()
    except Exception as exc:
        raise PayloadError("File bukan gambar yang valid.") from exc
    if fmt not in ALLOWED:
        raise PayloadError("Format foto harus PNG, JPG, atau WEBP.")
    if size[0] * size[1] > MAX_PIXELS:
        raise PayloadError("Resolusi foto terlalu besar.")
    return ALLOWED[fmt]


def pack(text: str, image: Optional[bytes] = None) -> bytes:
    if len(text) > MAX_TEXT_CHARS:
        raise PayloadError(f"Teks maksimal {MAX_TEXT_CHARS} karakter.")
    if not text.strip() and not image:
        raise PayloadError("Tulis pesan atau pilih foto terlebih dahulu.")
    mime = inspect_image(image) if image else None
    header = json.dumps(
        {"text": text, "mime": mime, "image_len": len(image) if image else 0},
        ensure_ascii=False, separators=(",", ":"),
    ).encode("utf-8")
    return MAGIC + struct.pack(">I", len(header)) + header + (image or b"")


def unpack(blob: bytes) -> Tuple[str, Optional[bytes], Optional[str]]:
    """Return (teks, byte_foto_atau_None, mime_atau_None). Teks polos lama tetap didukung."""
    if not blob.startswith(MAGIC):
        return blob.decode("utf-8", errors="replace"), None, None
    try:
        (hlen,) = struct.unpack(">I", blob[4:8])
        header = json.loads(blob[8:8 + hlen].decode("utf-8"))
        body = blob[8 + hlen:]
        n = int(header["image_len"])
        if n != len(body):
            raise ValueError("panjang foto tidak cocok")
        return header["text"], (body if n else None), header["mime"]
    except Exception as exc:
        raise PayloadError("Format isi pesan rusak.") from exc
