"""EmberNote - Pesan dan foto rahasia sekali baca berbasis AES-256-GCM (Streamlit)."""
import gc
import html
import os
import tempfile
import threading
import time
from datetime import datetime, timedelta, timezone

import streamlit as st

import tema
from modules import aes_gcm as cc
from modules import payload, selftest, storage, visual

st.set_page_config(page_title="EmberNote", page_icon="🔥", layout="wide")
tema.apply_theme()

MAX_CHARS = payload.MAX_TEXT_CHARS
DURATIONS = {"5 menit": 300, "1 jam": 3600, "24 jam": 86400, "7 hari": 604800}
TABS = ["Beranda", "Main", "Bukti Keamanan", "Tentang"]
PROOF_LABELS = [
    "Round-trip", "Kunci salah", "Ciphertext berubah", "Tag berubah",
    "AAD berubah", "Nonce unik", "Plaintext aman", "Sekali baca",
    "Kedaluwarsa", "Foto + teks", "Foto berubah", "Ciphertext acak",
    "File palsu",
]
WIB = timezone(timedelta(hours=7))
SELFTEST_LOCK = threading.Lock()


def fmt_time(ts: int) -> str:
    return datetime.fromtimestamp(ts, WIB).strftime("%d %b %Y %H:%M:%S WIB")


def go_to_main() -> None:
    st.session_state.navigation_tabs = TABS[1]


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
<div class="en-home-screen">
  <h1>EMBERNOTE</h1>
  <section class="en-home-intro">
    <h2>APA INI?</h2>
    <p>EmberNote mengirim pesan dan foto rahasia yang hanya bisa dibuka satu kali. Semua isi dilindungi AES-256-GCM dan dihapus setelah dibaca.</p>
  </section>
  <h2>CARA MAIN</h2>
  <div class="en-home-steps">
    <article><h3>1 · BUAT</h3><p>Tulis pesan atau pilih foto, atur masa berlaku, lalu enkripsi.</p></article>
    <article><h3>2 · BAGIKAN</h3><p>Kirim ID dan kunci melalui dua jalur yang berbeda.</p></article>
    <article><h3>3 · BACA</h3><p>Masukkan ID dan kunci. Isi terbuka sekali lalu hangus.</p></article>
  </div>
  <div class="en-home-stats">
    <div><strong>AES-256-GCM</strong><span>Terenkripsi</span></div>
    <div><strong>256-bit</strong><span>Kunci acak</span></div>
    <div><strong>SEKALI</strong><span>Baca lalu hangus</span></div>
    <div><strong>13/13</strong><span>Uji keamanan</span></div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(horizontal=True, horizontal_alignment="left", key="home-actions"):
        st.button("▶ MULAI", type="primary", on_click=go_to_main, key="home_start")
        st.button("📖 BACA PESAN", on_click=go_to_main, key="home_read")
        with st.popover("📜 Aturan main"):
            st.markdown(
                "- Kunci yang salah ditolak; pesan tetap aman.\n"
                "- Pesan hanya bisa dibaca sekali dan kedaluwarsa otomatis.\n"
                "- Foto PNG, JPG, atau WEBP, maksimal 2 MB."
            )


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
    st.title("BUKTI KEAMANAN")
    if "proof_results" not in st.session_state:
        with st.spinner("Menjalankan 13 pengujian keamanan..."):
            st.session_state.proof_results = run_security_tests()

    results = st.session_state.proof_results
    passed = sum(result["Hasil"] == "LULUS" for result in results)
    (st.success if passed == len(results) else st.error)(
        f"SCORE: {passed}/{len(results)} · AES-256-GCM"
    )
    if st.button("↻ UJI ULANG", type="primary", key="rerun_security_tests"):
        with st.spinner("Menjalankan 13 pengujian keamanan..."):
            st.session_state.proof_results = run_security_tests()
        st.rerun()

    cards = []
    for label, result in zip(PROOF_LABELS, results):
        passed_test = result["Hasil"] == "LULUS"
        detail = html.escape(result["Keterangan"], quote=True)
        name = html.escape(label)
        badge = "LULUS" if passed_test else "GAGAL"
        status = "pass" if passed_test else "fail"
        cards.append(
            f'<article class="en-proof-card {status}" title="{detail}" '
            f'aria-label="{name}: {badge}. {detail}">'
            f'<strong>{name}</strong><span>{badge}</span></article>'
        )
    st.markdown(
        f'<div class="en-proof-grid">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------- Tentang
def page_about():
    st.title("TENTANG EMBERNOTE")
    st.markdown(
        """
**AES-256-GCM** mengenkripsi satu paket teks dan foto. Kunci acak 256-bit tidak disimpan; server hanya menyimpan nonce dan ciphertext hingga pesan dibaca atau kedaluwarsa.

<h2>BATASAN & ANCAMAN</h2>
<div class="en-about-grid">
  <article><h3>🖥️ Bukan E2EE murni</h3><p>Kunci dibuat dan dipakai di server saat pesan dibuat atau dibuka.</p></article>
  <article><h3>🗝️ Jaga kunci</h3><p>Pemegang ID dan kunci dapat membuka pesan. Bagikan lewat jalur berbeda.</p></article>
  <article><h3>👀 Metadata terlihat</h3><p>Panjang, ukuran foto, ID, dan waktu tidak tersembunyi.</p></article>
  <article><h3>📷 Metadata foto</h3><p>EXIF atau lokasi tidak dibersihkan otomatis.</p></article>
  <article><h3>🚦 Batas percobaan</h3><p>Belum ada pembatasan spam atau percobaan.</p></article>
  <article><h3>☁️ Penyimpanan sementara</h3><p>Penyimpanan Streamlit Cloud hilang saat aplikasi dimulai ulang.</p></article>
  <article><h3>📱 Sesi browser</h3><p>Plaintext tetap ada sampai pesan ditutup.</p></article>
  <article><h3>🔎 Belum diaudit</h3><p>Proyek pembelajaran, bukan alat keamanan produksi.</p></article>
</div>
        """,
        unsafe_allow_html=True,
    )


default_tab = TABS[1] if "id" in st.query_params else TABS[0]
home_tab, main_tab, proof_tab, about_tab = st.tabs(
    TABS,
    key="navigation_tabs",
    default=default_tab,
    on_change="rerun",
)

if home_tab.open:
    with home_tab:
        with st.container(key="home-page"):
            page_home()
if main_tab.open:
    with main_tab:
        page_main()
if proof_tab.open:
    with proof_tab:
        with st.container(key="proof-page"):
            page_proof()
if about_tab.open:
    with about_tab:
        with st.container(key="about-page"):
            page_about()
