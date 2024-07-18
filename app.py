import os
import uuid
from flask import Flask, request, redirect, url_for, render_template, flash

app = Flask(__name__)

# Configuração da aplicação via arquivo externo (config.py)
app.config.from_object('config')

# Conjunto de extensões de arquivo permitidas
TIPOS_DISPONIVEIS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

# Função para verificar se a extensão do arquivo é permitida
def arquivos_permitidos(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in TIPOS_DISPONIVEIS

# Rota principal: exibe o formulário de upload e a imagem enviada, se houver
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo foi selecionado', 'error')
            return redirect(request.url)

        if not arquivos_permitidos(file.filename):
            flash('Utilize apenas arquivos de imagem (png, jpg, jpeg, gif)', 'error')
            return redirect(request.url)

        # Gera um nome de arquivo único com UUID para evitar colisões
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        flash('Imagem enviada com sucesso!', 'success')
        return render_template("index.html", filename=filename)
    else:
        return render_template('index.html')

# Rota para exibir a imagem enviada, recebe o nome do arquivo como argumento
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)