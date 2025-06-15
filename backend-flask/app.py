from flask import Flask, request, send_file, after_this_request
from flask_cors import CORS
from yt_dlp import YoutubeDL
import os
import uuid

app = Flask(__name__)
CORS(app)

# Caminho completo até a pasta 'bin' do ffmpeg
FFMPEG_PATH = r"C:\\ffmpeg\\bin"

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    format_ = data.get('format')

    if not url or format_ not in ['mp3', 'mp4']:
        return {'error': 'Parâmetros inválidos'}, 400

    out_dir = 'downloads'
    os.makedirs(out_dir, exist_ok=True)

    filename = str(uuid.uuid4())
    
    if format_ == 'mp3':
        raw_filepath = os.path.join(out_dir, filename)
        final_filepath = os.path.join(out_dir, filename + '.mp3')
        ydl_opts = {
            'outtmpl': raw_filepath,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': FFMPEG_PATH,
        }
    else:
        final_filepath = os.path.join(out_dir, filename + '.mp4')
        ydl_opts = {
            'outtmpl': final_filepath,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'ffmpeg_location': FFMPEG_PATH,
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(final_filepath):
                    os.remove(final_filepath)
            except Exception as e:
                print(f"Erro ao remover arquivo temporário: {e}")
            return response

        return send_file(final_filepath, as_attachment=True)

    except Exception as e:
        return {'error': f'Erro na conversão: {str(e)}'}, 500

if __name__ == '__main__':
    app.run(debug=True)
