from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'betim_chamados'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')  

# Página de Login para o Inventário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'andre.manoelino' and password == 'Minas@1234':
            session['logged_in'] = True
            return redirect(url_for('inventario'))
        else:
            flash('Credenciais inválidas. Tente novamente.')
    return render_template('login.html')


@app.route('/adicionar_item', methods=['POST'])
def adicionar_item():
    # Captura os dados do formulário
    departamento = request.form.get('departamento')
    hostname = request.form.get('hostname')
    ip_rede = request.form.get('ip_rede')
    anydesk = request.form.get('anydesk')
    senha_anydesk = request.form.get('senha_anydesk')
    ip_impressora = request.form.get('ip_impressora')
    modelo_impressora = request.form.get('modelo_impressora')  
    numero_serie_desktop = request.form.get('numero_serie_desktop')  
    fila_impressao = request.form.get('fila_impressao')
    atendente = request.form.get('atendente')
    pontos_em_uso = request.form.get('pontos_em_uso')
    pontos_reserva = request.form.get('pontos_reserva')
    switch = request.form.get('switch')
    porta_switch = request.form.get('porta_switch')

    # Obtendo a data e hora atual
    data_hora = datetime.now()

    # Insere os dados na tabela do inventário
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO inventario (departamento, hostname, ip_rede, anydesk, senha_anydesk, 
                                ip_impressora, modelo_impressora, numero_serie_desktop, 
                                fila_impressao, atendente, pontos_em_uso, 
                                pontos_reserva, switch, porta_switch, data_hora)  -- Incluindo a coluna data_hora
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  -- Adicionando %s para data_hora
    """, (departamento, hostname, ip_rede, anydesk, senha_anydesk,
          ip_impressora, modelo_impressora, numero_serie_desktop,
          fila_impressao, atendente, pontos_em_uso,
          pontos_reserva, switch, porta_switch, data_hora))  
    mysql.connection.commit()  # Salva as alterações no banco

    return redirect(url_for('inventario'))  # Redireciona de volta para a página do inventário


# Página do Inventário
@app.route('/inventario')
def inventario():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM inventario")  # Seleciona todos os itens do inventário
    dados_inventario = cursor.fetchall()
    return render_template('inventario.html', inventario=dados_inventario)

# Função para excluir um item do inventário
@app.route('/excluir_item/<int:id>')
def excluir_item(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM inventario WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('inventario'))  # Redireciona para a página do inventário

# Dashboard dos Chamados
@app.route('/dashboard')
def dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM chamados")
    chamados = cursor.fetchall()
    return render_template('dashboard.html', chamados=chamados)

# Abrir um novo chamado
@app.route('/abrir_chamado', methods=['POST'])
def abrir_chamado():
    nome = request.form['nome']
    departamento = request.form['departamento']
    guiche = request.form['guiche']
    descricao = request.form['descricao']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO chamados (nome, departamento, guiche, descricao) VALUES (%s, %s, %s, %s)",
                   (nome, departamento, guiche, descricao))
    mysql.connection.commit()
    return redirect(url_for('dashboard'))

# Fechar um chamado
@app.route('/fechar_chamado/<int:id>')
def fechar_chamado(id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE chamados SET status='Fechado' WHERE id=%s", [id])
    mysql.connection.commit()
    return redirect(url_for('dashboard'))

# Função para excluir um chamado
@app.route('/excluir_chamado/<int:id>')
def excluir_chamado(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM chamados WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('dashboard'))  # Redireciona para a página do dashboard

@app.route('/quantitativo')
def quantitativo():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM equipamentos_unidade")
    quantitativo_data = cursor.fetchall()   
    return render_template('quantitativo.html', quantitativo=quantitativo_data) 


# Função para adicionar novo item quantitativo
@app.route('/adicionar_quantitativo', methods=['POST'])
def adicionar_quantitativo():
    item = request.form['item']
    monitor_quantidade = request.form.get('monitor_quantidade')
    modelo_monitor = request.form.get('modelo_monitor')
    cabos_quantidade = request.form.get('cabos_quantidade')
    modelo_cabos = request.form.get('modelo_cabos')
    mouse_quantidade = request.form.get('mouse_quantidade')
    modelo_mouse = request.form.get('modelo_mouse')
    teclado_quantidade = request.form.get('teclado_quantidade')
    modelo_teclado = request.form.get('modelo_teclado')
    desktop_quantidade = request.form.get('desktop_quantidade')
    modelo_desktop = request.form.get('modelo_desktop')
    telefone_quantidade = request.form.get('telefone_quantidade')
    modelo_fone = request.form.get('modelo_fone')
    extensao_quantidade = request.form.get('extensao_quantidade')
    modelo_extensao = request.form.get('modelo_extensao')
    tablet_quantidade = request.form.get('tablet_quantidade')
    modelo_tablet = request.form.get('modelo_tablet')
    pendrive_quantidade = request.form.get('pendrive_quantidade')
    modelo_pendrive = request.form.get('modelo_pendrive')
    flashbio_quantidade = request.form.get('flashbio_quantidade')
    modelo_flashbio = request.form.get('modelo_flashbio')
    pad_quantidade = request.form.get('pad_quantidade')
    modelo_pad = request.form.get('modelo_pad')
    leitor_quantidade = request.form.get('leitor_quantidade')
    modelo_leitor = request.form.get('modelo_leitor')
    
  
    data_insercao = datetime.now()
    data_modificacao = datetime.now()

    # Inserindo dados no banco
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO quantitativo (
            item, monitor_quantidade, modelo_monitor, cabos_quantidade, modelo_cabos, 
            mouse_quantidade, modelo_mouse, teclado_quantidade, modelo_teclado, 
            desktop_quantidade, modelo_desktop, telefone_quantidade, modelo_fone, 
            extensao_quantidade, modelo_extensao, tablet_quantidade, modelo_tablet, 
            pendrive_quantidade, modelo_pendrive, flashbio_quantidade, modelo_flashbio, 
            pad_quantidade, modelo_pad, leitor_quantidade, modelo_leitor, 
            data_insercao, data_modificacao
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        item, monitor_quantidade, modelo_monitor, cabos_quantidade, modelo_cabos, 
        mouse_quantidade, modelo_mouse, teclado_quantidade, modelo_teclado, 
        desktop_quantidade, modelo_desktop, telefone_quantidade, modelo_fone, 
        extensao_quantidade, modelo_extensao, tablet_quantidade, modelo_tablet, 
        pendrive_quantidade, modelo_pendrive, flashbio_quantidade, modelo_flashbio, 
        pad_quantidade, modelo_pad, leitor_quantidade, modelo_leitor, 
        data_insercao, data_modificacao
    ))
    
    mysql.connection.commit()
    cursor.close()
    
    return redirect(url_for('quantitativo'))  # Redireciona para a página quantitativo após a adição


# Logout do inventário
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
