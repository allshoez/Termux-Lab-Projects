
from flask import Flask, render_template_string, request
import os, time
from threading import Thread

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Generator HTML → Flask</title>
<style>
body { font-family: Arial; background: #0a1530; color:#fff; padding:20px; }
h1 { text-align:center; color:#5eead4; }
textarea { width:100%; height:200px; padding:10px; font-family:monospace; font-size:14px; border-radius:8px; border:1px solid #5eead4; background:#0f1e4d; color:#fff; }
button { background:#5eead4; border:none; color:#000; padding:10px 16px; margin-top:10px; border-radius:8px; font-size:16px; cursor:pointer; }
button:hover { background:#4dd4be; }
pre { background:#0f1e4d; padding:15px; border-radius:8px; overflow-x:auto; white-space:pre-wrap; word-wrap:break-word; }
</style>
</head>
<body>
<h1>Generator HTML → Flask</h1>

<form method="POST">
<textarea name="html_input" placeholder="Tempel HTML di sini...">{{ html_input }}</textarea><br>
<button type="submit">Generate</button>
</form>

<h3>Hasil Kode Flask:</h3>
<pre id="flaskOutput">{{ flask_code }}</pre>
<button onclick="copyCode()">Salin Code</button>

<script>
function copyCode() {
  const code = document.getElementById('flaskOutput').textContent;
  navigator.clipboard.writeText(code).then(()=>{
    alert("Kode berhasil disalin!");
  }).catch(err=>{
    alert("Gagal menyalin kode: "+err);
  });
}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    html_input = ""
    flask_code = ""
    if request.method == "POST":
        html_input = request.form.get("html_input", "")
        flask_code = f'''from flask import Flask
import os, time
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return """{html_input}"""

if __name__ == "__main__":
    def run_flask():
        app.run(host="127.0.0.1", port=5000)

    t = Thread(target=run_flask)
    t.start()
    time.sleep(2)  # tunggu server siap
    # otomatis muncul pilihan browser di Android
    os.system('am start -a android.intent.action.VIEW -d "http://127.0.0.1:5000"')
    t.join()'''
    return render_template_string(HTML_TEMPLATE, html_input=html_input, flask_code=flask_code)

if __name__ == "__main__":
    def run_flask():
        app.run(host="127.0.0.1", port=5000)

    t = Thread(target=run_flask)
    t.start()
    time.sleep(2)  # tunggu server siap
    os.system('am start -a android.intent.action.VIEW -d "http://127.0.0.1:5000"')
    t.join()
