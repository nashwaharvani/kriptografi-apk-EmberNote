"""EmberNote - Pesan dan foto rahasia sekali baca berbasis AES-256-GCM (Streamlit)."""
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import streamlit as st

import tema
from modules import aes_gcm as cc
from modules import payload, selftest, storage, visual

st.set_page_config(page_title="EmberNote", page_icon="🔥", layout="centered")
tema.apply_theme()

LOGO = Path(__file__).parent / "images" / "logo.png"
MAX_CHARS = payload.MAX_TEXT_CHARS
DURATIONS = {"5 menit": 300, "1 jam": 3600, "24 jam": 86400, "7 hari": 604800}
PAGES = ["🔥 Buat Pesan", "📖 Baca Pesan", "🛡️ Bukti Keamanan", "ℹ️ Tentang"]
WIB = timezone(timedelta(hours=7))


def fmt_time(ts: int) -> str:
    return datetime.fromtimestamp(ts, WIB).strftime("%d %b %Y %H:%M:%S WIB")


# ---------------------------------------------------------------- Buat pesan
def page_create():
    st.header("🔥 Buat Pesan Rahasia Sekali Baca")
    st.caption("Pesan dan/atau foto dienkripsi dengan AES-256-GCM, dibuka sekali, lalu hangus.")

    with st.form("form_buat", clear_on_submit=True):
        text = st.text_area("Pesan rahasia / deskripsi foto", max_chars=MAX_CHARS, height=150)
        photo = st.file_uploader("Foto (opsional, PNG/JPG/WEBP, maks 2 MB)",
                                 type=["png", "jpg", "jpeg", "webp"])
        label = st.selectbox("Masa berlaku pesan", list(DURATIONS))
        submitted = st.form_submit_button("🔒 Enkripsi & buat pesan", type="primary")

    if submitted:
        try:
            blob = payload.pack(text, photo.getvalue() if photo else None)
        except payload.PayloadError as exc:
            st.warning(str(exc))
        else:
            key = cc.generate_key()
            msg_id = cc.generate_id()
            expires_at = int(time.time()) + DURATIONS[label]
            aad = cc.build_aad(msg_id, expires_at)
            nonce, ciphertext = cc.encrypt_bytes(blob, key, aad)
            storage.save_message(msg_id, nonce, ciphertext, expires_at)
            st.session_state.created = {
                "id": msg_id, "key": cc.b64_encode(key), "exp": expires_at,
                "has_photo": photo is not None,
            }

    created = st.session_state.get("created")
    if not created:
        return

    what = "Pesan dan foto" if created.get("has_photo") else "Pesan"
    st.success(f"{what} terenkripsi dan tersimpan. Kirim ID dan kunci lewat jalur yang BERBEDA.")
    st.markdown("**ID Pesan** (boleh dikirim lewat chat biasa)")
    st.code(created["id"], language=None)
    st.markdown("**Kunci Rahasia** (kirim lewat jalur lain; hanya ditampilkan sekarang)")
    st.code(created["key"], language=None)
    st.info(
        f"Berlaku sampai {fmt_time(created['exp'])}. Tautan langsung ke halaman baca: "
        f"tambahkan `?id={created['id']}` di akhir alamat aplikasi."
    )

    with st.expander("🔍 Apa yang sebenarnya tersimpan di server?"):
        row = storage.fetch_message(created["id"])
        if row:
            ct = row["ciphertext"]
            st.json({
                "id": row["id"],
                "nonce (hex)": row["nonce"].hex(),
                "ukuran ciphertext + tag (byte)": len(ct),
                "expires_at": row["expires_at"],
            })
            st.image(visual.ciphertext_to_image(ct),
                     caption="Ciphertext ditampilkan sebagai piksel: noise acak tanpa pola, tidak ada bentuk foto.")
            st.markdown("Awal ciphertext sebagai teks (Base64):")
            st.code(visual.base64_preview(ct), language=None)
            if len(ct) >= 4096:
                st.caption(f"Entropi ciphertext {visual.byte_entropy(ct):.3f} bit/byte (maksimum 8 = tidak berpola).")
            st.caption("Server tidak menyimpan kunci, foto, maupun teks asli, hanya data acak di atas.")

    if st.button("🧹 Bersihkan tampilan (hapus kunci dari layar)"):
        st.session_state.pop("created", None)
        st.rerun()


# ---------------------------------------------------------------- Baca pesan
def page_read():
    st.header("📖 Baca Pesan Rahasia")

    revealed = st.session_state.get("revealed")
    if revealed is not None:
        st.success("Pesan berhasil dibuka dan SUDAH DIHAPUS dari server. Simpan jika perlu.")
        if revealed["image"]:
            st.image(revealed["image"], caption="Foto rahasia")
        if revealed["text"]:
            st.text_area("Isi pesan / deskripsi", value=revealed["text"], height=180)
        if st.button("Tutup pesan"):
            st.session_state.revealed = None
            st.rerun()
        return

    with st.form("form_baca"):
        msg_id = st.text_input("ID Pesan", value=st.query_params.get("id", ""))
        key_text = st.text_input("Kunci Rahasia", type="password")
        submitted = st.form_submit_button("🔓 Buka pesan (hanya bisa sekali)", type="primary")

    if not submitted:
        return

    msg_id = msg_id.strip()
    row = storage.fetch_message(msg_id)
    if row is None:
        st.error("Pesan tidak ditemukan, sudah dibaca, atau sudah kedaluwarsa.")
        return
    try:
        key = cc.parse_key(key_text)
        aad = cc.build_aad(row["id"], row["expires_at"])
        plain = cc.decrypt_bytes(row["nonce"], row["ciphertext"], key, aad)
        text, image, _mime = payload.unpack(plain)
    except (cc.DecryptionError, payload.PayloadError) as exc:
        st.error(f"Gagal membuka pesan: {exc}")
        return

    # Hapus dulu secara atomik; hanya satu pembaca yang boleh melihat isi pesan.
    if storage.consume_message(msg_id):
        st.session_state.revealed = {"text": text, "image": image}
        st.rerun()
    else:
        st.error("Pesan ini baru saja dibuka oleh pihak lain.")


# ----------------------------------------------------------- Bukti keamanan
def page_proof():
    st.header("🛡️ Bukti Keamanan")
    st.write(
        "Halaman ini menjalankan pengujian langsung untuk menunjukkan bahwa **satu algoritma, "
        "AES-256-GCM, sudah mencukupi**: menjaga kerahasiaan teks dan foto, mendeteksi data yang "
        "diubah, dan melindungi metadata, tanpa hash atau cipher tambahan."
    )
    if st.button("▶️ Jalankan semua pengujian", type="primary"):
        results = selftest.run_all()
        passed = sum(r["Hasil"] == "LULUS" for r in results)
        (st.success if passed == len(results) else st.error)(
            f"{passed} dari {len(results)} pengujian lulus."
        )
        st.table(results)


# ------------------------------------------------------------------- Tentang
def page_about():
    st.header("ℹ️ Tentang EmberNote")
    st.markdown(
        """
**EmberNote** adalah aplikasi pesan dan foto rahasia sekali baca (*burn-after-reading*).

**Algoritma tunggal: AES-256-GCM**
- Kunci 256-bit dibuat acak oleh CSPRNG sistem operasi (`os.urandom`), tidak diturunkan dari password.
- Nonce 96-bit baru dibuat untuk setiap enkripsi.
- Teks dan foto dibungkus jadi **satu paket** lalu dienkripsi sekaligus, sehingga satu tag GCM melindungi keduanya.
- **AAD** mengikat `ID pesan` dan `waktu kedaluwarsa` ke ciphertext, sehingga mengubah metadata membuat dekripsi gagal.
- Server hanya menyimpan nonce dan ciphertext+tag. Kunci tidak pernah disimpan.

**Alur**
1. Pengirim menulis pesan dan/atau memilih foto, aplikasi membuat kunci acak, mengenkripsi, dan menyimpan ciphertext.
2. Pengirim membagikan *ID* dan *kunci* lewat dua jalur berbeda.
3. Penerima memasukkan keduanya, foto dan teks didekripsi serta diverifikasi, lalu dihapus dari server.

*Proyek pembelajaran kriptografi, bukan alat keamanan untuk produksi.*
        """
    )
    with st.expander("⚠️ Batasan & ancaman yang tidak ditangani"):
        st.markdown(
            """
- **Bukan E2EE murni**: kunci dibuat dan dipakai di server saat pesan dibuat/dibuka.
- Siapa pun yang memegang **ID + kunci** dapat membuka pesan, jadi kirim keduanya lewat jalur berbeda.
- **Panjang pesan, ukuran foto, ID, dan waktu** tidak tersembunyi.
- Foto tidak dibersihkan dari metadata (EXIF/lokasi); hapus dulu bila perlu.
- Tidak ada pembatasan spam/percobaan (menebak kunci 256-bit tetap mustahil).
- Penyimpanan Streamlit Cloud bersifat sementara.
- Plaintext tetap ada di sesi browser sampai pesan ditutup.
- Belum diaudit pihak independen.
            """
        )


if "page" not in st.session_state:
    st.session_state.page = PAGES[1] if "id" in st.query_params else PAGES[0]

if LOGO.exists():
    st.sidebar.image(str(LOGO), width=96)
st.sidebar.title("EmberNote")
choice = st.sidebar.radio("Menu", PAGES, key="page")
st.sidebar.caption("AES-256-GCM • Teks & foto sekali baca")

tema.hero("EmberNote", "Pesan dan foto rahasia sekali baca, dilindungi satu algoritma.",
          ("AES-256-GCM", "Sekali baca", "AAD"))
{PAGES[0]: page_create, PAGES[1]: page_read, PAGES[2]: page_proof, PAGES[3]: page_about}[choice]()
