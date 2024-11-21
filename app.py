from flask import Flask, request, render_template, send_file, abort
import os
import secrets
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Dicionário para armazenar as informações dos arquivos
files_info = {}

# Assegura que o diretório de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def generate_secure_link():
    """Gera um link aleatório seguro"""
    return secrets.token_urlsafe(16)

def generate_password():
    """Gera uma senha aleatória"""
    return secrets.token_urlsafe(8)

def hash_password(password):
    """Cria um hash da senha"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'Nenhum arquivo selecionado', 400

    if file:
        # Gera nome seguro para o arquivo
        filename = secure_filename(file.filename)
        # Gera link e senha únicos
        secure_link = generate_secure_link()
        password = generate_password()
        password_hash = hash_password(password)
        
        # Salva o arquivo
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_link))
        
        # Armazena informações do arquivo
        files_info[secure_link] = {
            'original_name': filename,
            'password_hash': password_hash
        }
        
        return {
            'link': f'/download/{secure_link}',
            'password': password
        }

@app.route('/download/<link>', methods=['GET', 'POST'])
def download_file(link):
    if request.method == 'GET':
        return render_template('download.html')
    
    if link not in files_info:
        abort(404)
    
    password = request.form.get('password', '')
    if hash_password(password) != files_info[link]['password_hash']:
        return 'Senha incorreta', 403
    
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], link),
        download_name=files_info[link]['original_name']
    )

if __name__ == '__main__':
    app.run(debug=True)
