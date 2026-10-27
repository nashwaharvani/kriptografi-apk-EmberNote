"""EmberNote - Pesan dan foto rahasia sekali baca berbasis AES-256-GCM (Streamlit)."""
import gc
import os
import tempfile
import threading
import time
from datetime import datetime, timedelta, timezone

import streamlit as st

import tema
from modules import aes_gcm as cc
from modules import payload, selftest, storage, visual

st.set_page_config(page_title="EmberNote", page_icon="🔥", layout="centered")
tema.apply_theme()

MAX_CHARS = payload.MAX_TEXT_CHARS
DURATIONS = {"5 menit": 300, "1 jam": 3600, "24 jam": 86400, "7 hari": 604800}
PAGES = ["🏠 Beranda", "🎮 Main", "🛡️ Bukti Keamanan", "ℹ️ Tentang"]
WIB = timezone(timedelta(hours=7))
SELFTEST_LOCK = threading.Lock()


def fmt_time(ts: int) -> str:
    return datetime.fromtimestamp(ts, WIB).strftime("%d %b %Y %H:%M:%S WIB")


def go_to_main() -> None:
    st.session_state.page = PAGES[1]
    st.session_state.top_page = PAGES[1]


def sync_top_page() -> None:
    st.session_state.page = st.session_state.top_page


def run_security_tests():
    if os.name != "nt":
        return selftest.run_all()

    with SELFTEST_LOCK:
        temporary_directory = tempfile.TemporaryDirectory

        class RetryingTemporaryDirectory(temporary_directory):
            def cleanup(self):
                try:
                    super().cleanup()
                except PermissionError:
                    # Python 3.14 may release SQLite's temporary DB handle after collection.
                    gc.collect()
                    time.sleep(0.1)
                    super().cleanup()

        tempfile.TemporaryDirectory = RetryingTemporaryDirectory
        try:
            return selftest.run_all()
        finally:
            tempfile.TemporaryDirectory = temporary_directory


# ------------------------------------------------------------------- Beranda
def page_home():
    st.markdown(
        """
<section class="en-pixel-hero">
  <h1 class="en-pixel-title">LET'S PLAY EMBERNOTE</h1>
  <p class="en-pixel-subtitle">Pesan dan foto rahasia yang hangus setelah dibaca</p>
</section>
<section class="en-dialog">
  <h3>APA INI?</h3>
  <p>EmberNote adalah aplikasi untuk mengirim pesan dan foto rahasia yang hanya bisa dibuka satu kali. Isinya dikunci dengan AES-256-GCM, jadi server tidak bisa membacanya, dan setelah dibuka langsung hangus.</p>
</section>
<h2>CARA MAIN</h2>
<div class="en-pixel-grid">
  <article class="en-pixel-card"><h3>1. LEVEL 1, BUAT PESAN</h3><p>Tulis pesan atau pilih foto, tentukan masa berlaku, lalu klik enkripsi. Kamu mendapat ID dan Kunci.</p></article>
  <article class="en-pixel-card"><h3>2. BAGIKAN</h3><p>Kirim ID dan Kunci lewat jalur berbeda (misalnya ID lewat WhatsApp, Kunci lewat email).</p></article>
  <article class="en-pixel-card"><h3>3. LEVEL 2, BACA PESAN</h3><p>Penerima memasukkan ID dan Kunci. Pesan terbuka sekali, lalu hilang dari server.</p></article>
</div>
<h2>ATURAN MAIN</h2>
<div class="en-pixel-grid">
  <article class="en-pixel-card en-rule-card"><h3>🔑 Kunci salah</h3><p>Ditolak, pesan tetap aman.</p></article>
  <article class="en-pixel-card en-rule-card"><h3>🔥 Sekali baca</h3><p>Sudah dibuka atau kedaluwarsa: pesan tidak bisa dibuka lagi.</p></article>
  <article class="en-pixel-card en-rule-card"><h3>🖼️ Foto</h3><p>PNG, JPG, atau WEBP, maksimal 2 MB.</p></article>
</div>
<h2>POWER-UPS</h2>
<div class="en-stats">
  <div class="en-stat-card"><strong>🔐 AES-256-GCM</strong><span>Enkripsi terautentikasi</span></div>
  <div class="en-stat-card"><strong>🗝️ 256-bit</strong><span>Kunci rahasia</span></div>
  <div class="en-stat-card"><strong>🔥 Sekali baca</strong><span>Lalu hangus</span></div>
  <div class="en-stat-card"><strong>⭐ 13 pengujian</strong><span>Bukti keamanan</span></div>
</div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="home-actions"):
        left, right = st.columns(2)
        with left:
            st.button("▶ MULAI", type="primary", on_click=go_to_main, key="home_start")
        with right:
            st.button("📖 BACA PESAN", key="home_read", on_click=go_to_main)
    st.markdown('<div class="en-grass"></div>', unsafe_allow_html=True)


# ----------------------------------------------------------- Main: buat & baca
def page_main():
    with st.container(key="main-page"):
        st.title("🎮 Main")
        create_column, read_column = st.columns(2)

        with create_column:
            with st.container(key="main-create-panel", border=True):
                st.subheader("LEVEL 1: BUAT PESAN")

                with st.form("form_buat", clear_on_submit=True):
                    text = st.text_area(
                        "Pesan rahasia / deskripsi foto",
                        max_chars=MAX_CHARS,
                        height=80,
                    )
                    photo = st.file_uploader(
                        "Foto (opsional, PNG/JPG/WEBP, maks 2 MB)",
                        type=["png", "jpg", "jpeg", "webp"],
                    )
                    label = st.selectbox(
                        "Masa berlaku pesan",
                        list(DURATIONS),
                    )
                    create_submitted = st.form_submit_button(
                        "▶ ENKRIPSI & BUAT PESAN",
                        type="primary",
                    )

                if create_submitted:
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
                            "id": msg_id,
                            "key": cc.b64_encode(key),
                            "exp": expires_at,
                            "has_photo": photo is not None,
                        }

                created = st.session_state.get("created")
                if created:
                    what = "Pesan + foto" if created.get("has_photo") else "Pesan"
                    st.success(
                        f"{what} tersimpan; bagikan ID dan kunci terpisah."
                    )
                    st.caption("ID PESAN · kirim lewat chat biasa")
                    st.code(created["id"], language=None)
                    st.caption("KUNCI RAHASIA · kirim lewat jalur lain")
                    st.code(created["key"], language=None)
                    st.caption(
                        f"Sampai {fmt_time(created['exp'])} · `?id={created['id']}`"
                    )
                    if st.button(
                        "🧹 Bersihkan tampilan",
                        key="clear_created",
                    ):
                        st.session_state.pop("created", None)
                        st.rerun()

                with st.popover("🔍 Lihat isi server"):
                    if not created:
                        st.caption("Buat pesan terlebih dahulu untuk melihat data server.")
                    else:
                        row = storage.fetch_message(created["id"])
                        if row:
                            ciphertext = row["ciphertext"]
                            st.json({
                                "id": row["id"],
                                "nonce (hex)": row["nonce"].hex(),
                                "ukuran ciphertext + tag (byte)": len(ciphertext),
                                "expires_at": row["expires_at"],
                            })
                            st.image(
                                visual.ciphertext_to_image(ciphertext),
                                caption="Ciphertext berupa noise acak; bukan bentuk foto.",
                            )
                            st.markdown("Awal ciphertext sebagai teks (Base64):")
                            st.code(visual.base64_preview(ciphertext), language=None)
                            if len(ciphertext) >= 4096:
                                st.caption(
                                    f"Entropi ciphertext "
                                    f"{visual.byte_entropy(ciphertext):.3f} bit/byte "
                                    "(maksimum 8 = tidak berpola)."
                                )
                            st.caption(
                                "Server tidak menyimpan kunci, foto, maupun teks asli."
                            )

        with read_column:
            with st.container(key="main-read-panel", border=True):
                st.subheader("LEVEL 2: BACA PESAN")
                revealed = st.session_state.get("revealed")
                if revealed is not None:
                    st.markdown(
                        '<div class="st-key-game-over">GAME OVER: PESAN SUDAH HANGUS</div>',
                        unsafe_allow_html=True,
                    )
                    st.success("Pesan dibuka dan dihapus dari server.")
                    if revealed["image"]:
                        st.image(revealed["image"], caption="Foto rahasia")
                    if revealed["text"]:
                        st.text_area(
                            "Isi pesan / deskripsi",
                            value=revealed["text"],
                            height=80,
                            disabled=True,
                        )
                    if st.button("Tutup pesan", key="close_revealed"):
                        st.session_state.revealed = None
                        st.rerun()
                else:
                    with st.form("form_baca"):
                        msg_id = st.text_input(
                            "ID Pesan",
                            value=st.query_params.get("id", ""),
                        )
                        key_text = st.text_input("Kunci Rahasia", type="password")
                        read_submitted = st.form_submit_button(
                            "▶ BUKA PESAN (HANYA SEKALI)",
                            type="primary",
                        )

                    if read_submitted:
                        msg_id = msg_id.strip()
                        row = storage.fetch_message(msg_id)
                        if row is None:
                            st.error(
                                "Pesan tidak ditemukan, sudah dibaca, atau kedaluwarsa."
                            )
                        else:
                            try:
                                key = cc.parse_key(key_text)
                                aad = cc.build_aad(row["id"], row["expires_at"])
                                plain = cc.decrypt_bytes(
                                    row["nonce"],
                                    row["ciphertext"],
                                    key,
                                    aad,
                                )
                                text, image, _mime = payload.unpack(plain)
                            except (cc.DecryptionError, payload.PayloadError) as exc:
                                st.error(f"Gagal membuka pesan: {exc}")
                            else:
                                # Consume atomically so only one reader can see the message.
                                if storage.consume_message(msg_id):
                                    st.session_state.revealed = {
                                        "text": text,
                                        "image": image,
                                    }
                                    st.rerun()
                                else:
                                    st.error("Pesan ini baru saja dibuka oleh pihak lain.")


# ----------------------------------------------------------- Bukti keamanan
def page_proof():
    st.title("RULES!")
    st.subheader("Bukti Keamanan")
    st.write(
        "Halaman ini menjalankan pengujian langsung untuk menunjukkan bahwa **satu algoritma, "
        "AES-256-GCM, sudah mencukupi**: menjaga kerahasiaan teks dan foto, mendeteksi data yang "
        "diubah, dan melindungi metadata, tanpa hash atau cipher tambahan."
    )
    if st.button("▶ JALANKAN SEMUA PENGUJIAN", type="primary"):
        results = run_security_tests()
        passed = sum(r["Hasil"] == "LULUS" for r in results)
        (st.success if passed == len(results) else st.error)(
            f"SCORE: {passed}/{len(results)} · {passed} dari {len(results)} pengujian lulus."
        )
        for index in range(0, len(results), 2):
            columns = st.columns(2)
            for offset, (column, result) in enumerate(zip(columns, results[index:index + 2])):
                with column:
                    with st.container(border=True, key=f"proof-result-{index + offset}"):
                        passed_test = result["Hasil"] == "LULUS"
                        st.subheader(f"{'⭐' if passed_test else '⚠️'} {result['Pengujian']}")
                        (st.success if passed_test else st.error)(
                            "🏅 LULUS" if passed_test else "❌ GAGAL"
                        )
                        st.caption(result["Keterangan"])


# ------------------------------------------------------------------- Tentang
def page_about():
    st.title("ℹ️ Tentang EmberNote")
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
    st.subheader("⚠️ Batasan & ancaman yang tidak ditangani")
    st.markdown(
        """
<div class="en-pixel-grid">
  <div class="en-pixel-card"><h3>🖥️ Bukan E2EE murni</h3><p>Kunci dibuat dan dipakai di server saat pesan dibuat atau dibuka.</p></div>
  <div class="en-pixel-card"><h3>🗝️ Jaga kuncinya</h3><p>Siapa pun yang memegang ID dan kunci dapat membuka pesan. Kirim keduanya lewat jalur berbeda.</p></div>
  <div class="en-pixel-card"><h3>👀 Metadata terlihat</h3><p>Panjang pesan, ukuran foto, ID, dan waktu tidak tersembunyi.</p></div>
  <div class="en-pixel-card"><h3>📷 Metadata foto</h3><p>EXIF atau lokasi di foto tidak dibersihkan; hapus terlebih dahulu bila perlu.</p></div>
  <div class="en-pixel-card"><h3>🚦 Batas percobaan</h3><p>Belum ada pembatasan spam atau percobaan; menebak kunci 256-bit tetap tidak praktis.</p></div>
  <div class="en-pixel-card"><h3>☁️ Penyimpanan sementara</h3><p>Penyimpanan Streamlit Cloud bersifat sementara.</p></div>
  <div class="en-pixel-card"><h3>📱 Sesi browser</h3><p>Plaintext tetap ada di sesi browser sampai pesan ditutup.</p></div>
  <div class="en-pixel-card"><h3>🔎 Belum diaudit</h3><p>Aplikasi belum diaudit oleh pihak independen.</p></div>
</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="en-footer">THANK YOU<br>PRESS START TO PLAY AGAIN</div><div class="en-grass"></div>', unsafe_allow_html=True)


LEGACY_MAIN_PAGES = {"🔥 Buat Pesan", "📖 Baca Pesan"}
if st.session_state.get("page") in LEGACY_MAIN_PAGES:
    st.session_state.page = PAGES[1]
if st.session_state.get("top_page") in LEGACY_MAIN_PAGES:
    st.session_state.top_page = PAGES[1]
if "page" not in st.session_state:
    st.session_state.page = PAGES[1] if "id" in st.query_params else PAGES[0]
if st.session_state.get("page") not in PAGES:
    st.session_state.page = PAGES[0]
if st.session_state.get("top_page") not in PAGES:
    st.session_state.top_page = st.session_state.page

choice = st.radio(
    "MENU", PAGES, key="top_page", horizontal=True,
    label_visibility="collapsed", on_change=sync_top_page,
)

{
    PAGES[0]: page_home,
    PAGES[1]: page_main,
    PAGES[2]: page_proof,
    PAGES[3]: page_about,
}[choice]()
