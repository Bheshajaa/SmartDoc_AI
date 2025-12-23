import streamlit as st
import io
import time
from word_to_pdf import word_to_pdf
from pdf_to_word import pdf_to_word

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SmartDoc AI", layout="centered")

# ---------------- CSS ANIMATIONS ----------------
st.markdown("""
<style>
.download-btn {
    animation: fadeIn 0.8s ease-in;
}

.status-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 60px;
    font-weight: bold;
    margin: 20px auto;
    animation: popIn 0.6s ease-out;
}

.success {
    background-color: #2ecc71;
    color: white;
}

.failure {
    background-color: #e74c3c;
    color: white;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

@keyframes popIn {
    0% {transform: scale(0.5); opacity: 0;}
    100% {transform: scale(1); opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.title("📄 SmartDoc AI")
st.caption("High-Fidelity Conversion | Smooth UX | Privacy-First")

mode = st.radio(
    "Choose conversion type",
    ["Word → PDF", "PDF → Word"],
    horizontal=True
)

uploaded_file = st.file_uploader(
    "Upload your document",
    type=["docx", "pdf"]
)

# ---------------- MAIN LOGIC ----------------
if uploaded_file:
    file_bytes = uploaded_file.read()
    file_stream = io.BytesIO(file_bytes)

    if st.button("🔄 Convert"):

        # ✅ DEFINE widgets FIRST
        progress = st.progress(0)
        status = st.empty()

        # ✅ UX progress animation (INSIDE button)
        for i in range(0, 80, 10):
            progress.progress(i)
            status.text("Processing document...")
            time.sleep(0.15)

        try:
            with st.spinner("🔄 Finalizing conversion..."):
                if mode == "Word → PDF":
                    result = word_to_pdf(file_stream)
                    filename = "SmartDoc_Output.pdf"
                    mime = "application/pdf"
                else:
                    result = pdf_to_word(file_stream)
                    filename = "SmartDoc_Output.docx"
                    mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

            progress.progress(100)
            status.text("Conversion completed ✅")

            # ✅ SUCCESS CIRCLE
            st.markdown(
                '<div class="status-circle success">✓</div>',
                unsafe_allow_html=True
            )

            st.success("Conversion completed successfully!")

            # ✅ FADE-IN DOWNLOAD BUTTON
            st.markdown('<div class="download-btn">', unsafe_allow_html=True)
            st.download_button(
                label="⬇ Download File",
                data=result.getvalue(),
                file_name=filename,
                mime=mime
            )
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            progress.progress(100)
            status.text("Conversion failed ❌")

            # ❌ FAILURE CIRCLE
            st.markdown(
                '<div class="status-circle failure">✕</div>',
                unsafe_allow_html=True
            )

            st.error("Conversion failed. Please try again.")