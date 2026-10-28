import streamlit as st
import uuid
import base64
from src.pdf_loader import extract_pages
from src.chunker import chunk_pages
from src.vector_store import build_index
from src.rag import answer_question

st.set_page_config(
    page_title="Yapay Zekâ Öğrenci Asistanı",
    page_icon="🎓",
    layout="wide"
)

# İlk sohbeti oluştur
if "sohbetler" not in st.session_state:
    ilk_id = str(uuid.uuid4())

    st.session_state.sohbetler = {
        ilk_id: {
            "baslik": "Yeni Sohbet",
            "mesajlar": []
        }
    }

    st.session_state.aktif_sohbet = ilk_id


# Yeni sohbet oluşturma fonksiyonu
def yeni_sohbet():
    sohbet_id = str(uuid.uuid4())

    st.session_state.sohbetler[sohbet_id] = {
        "baslik": "Yeni Sohbet",
        "mesajlar": []
    }

    st.session_state.aktif_sohbet = sohbet_id


# Sol panel
with st.sidebar:

    st.title("🎓 Öğrenci Paneli")

    if st.button("➕ Yeni Sohbet", use_container_width=True):
        yeni_sohbet()
        st.rerun()

    st.divider()

    st.subheader("💬 Sohbetlerim")

    for sohbet_id in reversed(list(st.session_state.sohbetler.keys())):

        sohbet = st.session_state.sohbetler[sohbet_id]

        if st.button(
            "💬 " + sohbet["baslik"],
            key="sohbet_" + sohbet_id,
            use_container_width=True
        ):
            st.session_state.aktif_sohbet = sohbet_id
            st.rerun()

    st.divider()

    # PDF yükleme
    st.subheader("📄 PDF Dosyalarım")

    aktif_id = st.session_state.aktif_sohbet

    dosyalar = st.file_uploader(
        "Ders notlarını buraya yükle",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_" + aktif_id
    )

    if dosyalar:
        st.success(f"{len(dosyalar)} PDF yüklendi!")

        for dosya in dosyalar:
            st.write("📄 " + dosya.name)

        if st.button("📚 PDF'leri İşle", key="pdf_isle"):
            try:
                import tempfile
                import os
                import hashlib

                with st.spinner("PDF dosyaları işleniyor..."):
                    toplam_parca = 0

                    for dosya in dosyalar:
                        pdf_verisi = dosya.getvalue()

                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".pdf"
                        ) as gecici:
                            gecici.write(pdf_verisi)
                            gecici_yol = gecici.name

                        try:
                            sayfalar = extract_pages(gecici_yol)
                            parcalar = chunk_pages(sayfalar)

                            pdf_kimligi = hashlib.sha256(
                                pdf_verisi
                            ).hexdigest()[:16]

                            for parca in parcalar:
                                parca["id"] = (
                                    pdf_kimligi + "_" + parca["id"]
                                )

                            if parcalar:
                                build_index(parcalar)
                                toplam_parca += len(parcalar)

                        finally:
                            os.unlink(gecici_yol)

                st.success(
                    f"PDF'ler işlendi! "
                    f"{toplam_parca} metin parçası hazır."
                )

            except Exception as hata:
                st.error(f"PDF işleme hatası: {hata}")

        secilen_pdf = st.selectbox(
            "Önizlenecek PDF:",
            range(len(dosyalar)),
            format_func=lambda i: dosyalar[i].name
        )

        if st.checkbox("📖 PDF Önizleme"):
            pdf_verisi = dosyalar[secilen_pdf].getvalue()

            pdf_base64 = base64.b64encode(
                pdf_verisi
            ).decode("utf-8")

            pdf_html = f"""
            <iframe
                src="data:application/pdf;base64,{pdf_base64}"
                width="100%"
                height="500"
                type="application/pdf">
            </iframe>
            """

            st.components.v1.html(
                pdf_html,
                height=510
            )

    else:
        st.info("Henüz PDF yüklenmedi.")

    st.divider()
    # Çalışma araçları
    st.subheader("🧠 Çalışma Araçları")

    if st.button("📝 PDF Özeti", use_container_width=True):
        st.info("PDF özetleme özelliği yakında eklenecek.")

    if st.button("✅ Soru Oluştur", use_container_width=True):
        st.info("PDF'den soru oluşturma özelliği yakında eklenecek.")


# Ana sohbet ekranı
aktif_id = st.session_state.aktif_sohbet

aktif_sohbet = st.session_state.sohbetler[aktif_id]

st.title("🎓 Yapay Zekâ Öğrenci Asistanı")

st.caption(
    "PDF dosyalarını yükle, sorularını sor, derslerine hazırlan!"
)

if dosyalar:
    st.success(
        f"📚 {len(dosyalar)} PDF seçili. "
        "Belgeler üzerinden soru-cevap özelliği henüz geliştirilmedi."
    )
else:
    st.info("📄 Başlamak için sol panelden PDF yükleyebilirsin.")

st.divider()

# Sohbet mesajlarını göster
for mesaj in aktif_sohbet["mesajlar"]:

    with st.chat_message(mesaj["rol"]):
        st.write(mesaj["icerik"])


# Mesaj yazma alanı
soru = st.chat_input("PDF hakkında bir soru sor...")

if soru:

    # İlk sorudan sohbet başlığı oluştur
    if not aktif_sohbet["mesajlar"]:
        aktif_sohbet["baslik"] = (
            soru[:30] + "..."
            if len(soru) > 30
            else soru
        )

    aktif_sohbet["mesajlar"].append({
        "rol": "user",
        "icerik": soru
    })

        # Gerçek RAG sistemiyle cevap oluştur
    if dosyalar:
        try:
            with st.spinner("Yapay zekâ cevap hazırlıyor..."):
                sonuc = answer_question(soru)
                cevap = sonuc["answer"]

        except Exception as hata:
            cevap = f"Yapay zekâ hatası: {hata}"

    else:
        cevap = "Önce bir PDF yüklemelisin."
    aktif_sohbet["mesajlar"].append({
        "rol": "assistant",
        "icerik": cevap
    })

    st.rerun()