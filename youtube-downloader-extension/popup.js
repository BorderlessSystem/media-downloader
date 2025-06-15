document.getElementById('mp3').addEventListener('click', () => download('mp3'));
document.getElementById('mp4').addEventListener('click', () => download('mp4'));

function download(format) {
  const url = document.getElementById('url').value.trim();
  const status = document.getElementById('status');
  if (!url) {
    status.textContent = 'Por favor, cole um link.';
    return;
  }

  status.textContent = 'Processando...';

  fetch('http://127.0.0.1:5000/download', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url, format })
  })
    .then(response => {
      if (!response.ok) throw new Error("Erro na conversão.");
      return response.blob();
    })
    .then(blob => {
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = `video.${format}`;
      a.click();
      status.textContent = 'Download iniciado.';
    })
    .catch(err => {
      status.textContent = 'Erro: ' + err.message;
    });
}
