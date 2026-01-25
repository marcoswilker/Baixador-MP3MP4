import streamlit as st
import yt_dlp
import os
import tempfile

# Configuração da página para celular e PC
st.set_page_config(page_title="YouTube Downloader Pro", page_icon="🎥")

st.title("🎥 YouTube Downloader")
st.markdown("Baixe vídeos ou áudio diretamente para o seu dispositivo.")

# --- ENTRADA DE DADOS ---
url = st.text_input("Cole a URL do YouTube aqui:", placeholder="https://www.youtube.com/watch?v=...")

formato = st.radio("Escolha o formato de saída:", ("MP4 (Vídeo)", "MP3 (Áudio)"), horizontal=True)


# --- FUNÇÃO DE DOWNLOAD ---
def processar_download(url, choice):
    # Usamos uma pasta temporária do sistema para não encher o servidor
    temp_dir = tempfile.gettempdir()

    ydl_opts = {
        'restrictfilenames': True,
        'noplaylist': True,
        'compat_opts': ['force-ipv4'],
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }

    if "MP4" in choice:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
        })
        extensao = "mp4"
    else:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
        extensao = "mp3"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # O yt-dlp pode mudar o nome levemente, pegamos o caminho real:
        filename = ydl.prepare_filename(info)
        if "MP3" in choice:
            filename = filename.rsplit('.', 1)[0] + ".mp3"
        return filename


# --- BOTÃO DE AÇÃO ---
if url:
    if st.button("🚀 Preparar Download"):
        try:
            with st.spinner("Processando... Isso pode demorar dependendo do tamanho do vídeo."):
                caminho_arquivo = processar_download(url, formato)

                # Lê o arquivo para oferecer o download na web
                with open(caminho_arquivo, "rb") as f:
                    st.success("Pronto! Clique no botão abaixo para salvar no seu dispositivo.")
                    st.download_button(
                        label="💾 Baixar Arquivo agora",
                        data=f,
                        file_name=os.path.basename(caminho_arquivo),
                        mime="video/mp4" if "MP4" in formato else "audio/mpeg"
                    )
        except Exception as e:
            st.error(f"Erro ao processar: {e}")

st.info("Nota: O vídeo é processado no servidor e depois enviado para o seu navegador.")