import os
import csv
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from calendar import monthrange
from email_sender import send_notification_email 

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'uma_chave_secreta_padrao_e_segura')

# Configurações do CSV
CSV_FILE = os.path.join(os.path.dirname(__file__), 'data.csv')
# ATUALIZADO: Adicionado 'psi'
CSV_HEADERS = ['id', 'descricao', 'validade_data_completa', 'numero_serie', 'localizacao', 'status_calibracao', 'psi']

# Configurações de E-mail (SMTPLib)
EMAIL_CONFIG = {
    'SMTP_SERVER': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'), # Servidor SMTP do Gmail
    'SMTP_PORT': int(os.environ.get('SMTP_PORT', 587)), # Porta 587 para TLS
    'EMAIL_USER': os.environ.get('EMAIL_USER', 'controletransdutores@gmail.com'),
    'EMAIL_PASSWORD': os.environ.get('EMAIL_PASSWORD', 'acesso2026@'), # Senha da conta do Gmail
    'RECIPIENTS': [r.strip() for r in os.environ.get('RECIPIENTS', 'julio.marcostavaresviana@technipfmc.com').split(',')]
}

# --- Lógica de Manipulação do CSV ---

def init_csv():
    "Garante que o arquivo CSV exista com os cabeçalhos corretos."
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)

def read_transducers():
    "Lê todos os transdutores do arquivo CSV."
    init_csv()
    transducers = []
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Garante que o ID seja um inteiro para ordenação e busca
            try:
                row['id'] = int(row['id'])
            except ValueError:
                continue
            
            # Garante que os novos campos existam, definindo um valor padrão
            row['status_calibracao'] = row.get('status_calibracao', 'OK')
            row['psi'] = row.get('psi', '') # Novo campo PSI
            
            # CORREÇÃO: Garante que a chave de data correta exista, para compatibilidade com dados antigos
            if 'validade_mes_ano' in row and 'validade_data_completa' not in row:
                try:
                    year, month = map(int, row['validade_mes_ano'].split('-'))
                    last_day = monthrange(year, month)[1]
                    row['validade_data_completa'] = f"{year:04d}-{month:02d}-{last_day:02d}"
                except:
                    row['validade_data_completa'] = row['validade_mes_ano']
                row.pop('validade_mes_ano', None)
            
            transducers.append(row)
    return transducers

def write_transducer(data):
    "Adiciona um novo transdutor ao arquivo CSV."
    init_csv()
    transducers = read_transducers()
    
    # Gera um novo ID
    if transducers:
        last_id = max(t['id'] for t in transducers)
        new_id = last_id + 1
    else:
        new_id = 1
        
    data['id'] = new_id
    # Define o status inicial como OK
    data['status_calibracao'] = 'OK'
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        # Converte o ID de volta para string para escrita no CSV
        data_to_write = {k: str(v) for k, v in data.items()}
        writer.writerow(data_to_write)
    
    return data

def delete_transducer(transducer_id):
    "Remove um transdutor do arquivo CSV pelo ID."
    transducers = read_transducers()
    initial_count = len(transducers)
    
    # Filtra a lista, mantendo apenas os transdutores com ID diferente do ID a ser excluído
    transducers = [t for t in transducers if t['id'] != transducer_id]
    
    if len(transducers) < initial_count:
        rewrite_csv(transducers)
        return True
    return False

def rewrite_csv(transducers):
    "Reescreve todo o arquivo CSV com a lista atualizada de transdutores."
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for t in transducers:
            # Converte o ID de volta para string para escrita no CSV
            data_to_write = {k: str(v) for k, v in t.items()}
            writer.writerow(data_to_write)

# --- Lógica de Validade (Sem Alteração) ---

def calculate_validity(transducer):
    """Calcula os dias restantes e define o status de validade."""
    
    # Se o transdutor estiver em calibração, ignora a validade
    if transducer.get('status_calibracao') == 'Em Calibração':
        transducer['dias_restantes'] = 'N/A'
        transducer['status_class'] = 'warning'
        transducer['status_text'] = 'EM CALIBRAÇÃO'
        transducer['validade_formatada'] = transducer.get('validade_data_completa', 'N/A')
        transducer['validade_date'] = None
        return transducer
        
    validade_str = transducer.get('validade_data_completa') 
    
    if not validade_str:
        transducer['dias_restantes'] = 'Erro de Data'
        transducer['status_class'] = 'danger'
        transducer['status_text'] = 'Data Ausente'
        transducer['validade_formatada'] = 'N/A'
        transducer['validade_date'] = None
        return transducer
        
    try:
        # Tenta parsear a data completa
        validade_date = datetime.strptime(validade_str, '%Y-%m-%d')
    except ValueError:
        # Caso a data esteja em formato inválido (ex: YYYY-MM)
        try:
            year, month = map(int, validade_str.split('-'))
            last_day = monthrange(year, month)[1]
            validade_date = datetime(year, month, last_day)
        except ValueError:
            # Caso a data esteja em formato inválido
            transducer['dias_restantes'] = 'Erro de Data'
            transducer['status_class'] = 'danger'
            transducer['status_text'] = 'Data Inválida'
            transducer['validade_formatada'] = validade_str
            transducer['validade_date'] = None
            return transducer

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Calcula a diferença em dias
    dias_restantes = (validade_date - today).days
    
    transducer['dias_restantes'] = dias_restantes
    transducer['validade_formatada'] = validade_date.strftime('%d/%m/%Y') # Formato de exibição
    transducer['validade_date'] = validade_date
    
    if dias_restantes < 0:
        transducer['status_class'] = 'danger'
        transducer['status_text'] = 'VENCIDO'
    elif dias_restantes <= 10: # Menos de 10 dias
        transducer['status_class'] = 'danger'
        transducer['status_text'] = f'Vence em {dias_restantes} dias'
    elif dias_restantes <= 30: # Menos de 30 dias
        transducer['status_class'] = 'warning'
        transducer['status_text'] = f'Atenção! {dias_restantes} dias'
    else:
        transducer['status_class'] = 'ok'
        transducer['status_text'] = 'OK'
        
    return transducer

# --- Lógica de Notificação (Sem Alteração) ---

def check_for_notifications():
    """Verifica quais transdutores precisam de notificação e envia o e-mail."""
    transducers = read_transducers()
    transducers_with_status = [calculate_validity(t) for t in transducers]
    
    transducers_to_notify = []
    
    for t in transducers_with_status:
        # Verifica se a data de validade é válida e se está próximo do vencimento
        # E se não estiver em calibração
        if t.get('status_calibracao') != 'Em Calibração' and isinstance(t['dias_restantes'], int) and t['dias_restantes'] >= 0:
            # Notifica com 10 ou 5 dias
            if t['dias_restantes'] <= 10 or t['dias_restantes'] == 5:
                transducers_to_notify.append(t)
    
    if transducers_to_notify:
        # Remove a chave 'validade_date' antes de enviar para o email_sender
        for t in transducers_to_notify:
            t.pop('validade_date', None)
            
        result = send_notification_email(EMAIL_CONFIG, transducers_to_notify)
        return result
    
    return "Nenhuma notificação de vencimento necessária hoje."

# --- Rotas Flask ---

@app.route('/')
def index():
    transducers = read_transducers()
    transducers_with_status = [calculate_validity(t) for t in transducers]
    
    # Ordena para mostrar os mais próximos do vencimento primeiro
    transducers_with_status.sort(key=lambda t: t['dias_restantes'] if isinstance(t['dias_restantes'], int) else float('inf'))
    
    return render_template('index.html', transducers=transducers_with_status)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Validação básica
        if not request.form.get('descricao') or not request.form.get('validade_data_completa'):
            flash('Descrição e Data de Validade são campos obrigatórios.', 'error')
            return redirect(url_for('register'))
            
        new_transducer = {
            'descricao': request.form['descricao'],
            'validade_data_completa': request.form['validade_data_completa'],
            'numero_serie': request.form.get('numero_serie', ''),
            'localizacao': request.form.get('localizacao', ''),
            'psi': request.form.get('psi', '') # Novo campo PSI
        }
        write_transducer(new_transducer)
        flash('Transdutor cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/edit/<int:transducer_id>', methods=['GET', 'POST'])
def edit(transducer_id):
    transducers = read_transducers()
    transducer = next((t for t in transducers if t['id'] == transducer_id), None)
    
    if transducer is None:
        flash('Transdutor não encontrado.', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        # Validação básica
        if not request.form.get('descricao') or not request.form.get('validade_data_completa'):
            flash('Descrição e Data de Validade são campos obrigatórios.', 'error')
            return redirect(url_for('edit', transducer_id=transducer_id))
            
        # Armazena a data antiga para comparação
        old_validade_date = transducer['validade_data_completa']
            
        # Atualiza os dados do transdutor
        transducer['descricao'] = request.form['descricao']
        transducer['validade_data_completa'] = request.form['validade_data_completa']
        transducer['numero_serie'] = request.form.get('numero_serie', '')
        transducer['localizacao'] = request.form.get('localizacao', '')
        transducer['psi'] = request.form.get('psi', '') # Novo campo PSI
        
        # Lógica de Calibração: Se a data de validade foi alterada, o status de calibração volta para OK
        if transducer['validade_data_completa'] != old_validade_date:
            transducer['status_calibracao'] = 'OK'
        
        # Reescreve o CSV com a lista atualizada
        rewrite_csv(transducers)
        
        flash(f'Transdutor #{transducer_id} atualizado com sucesso!', 'success')
        return redirect(url_for('index'))
        
    # GET request
    return render_template('edit.html', transducer=transducer)

@app.route('/calibrate/<int:transducer_id>')
def calibrate(transducer_id):
    transducers = read_transducers()
    transducer = next((t for t in transducers if t['id'] == transducer_id), None)
    
    if transducer is None:
        flash('Transdutor não encontrado.', 'error')
        return redirect(url_for('index'))
        
    # Altera o status para Em Calibração
    transducer['status_calibracao'] = 'Em Calibração'
    
    # Reescreve o CSV com a lista atualizada
    rewrite_csv(transducers)
    
    flash(f"Transdutor #{transducer_id} marcado como 'Em Calibração'.", 'warning')
    return redirect(url_for('index'))

@app.route('/delete/<int:transducer_id>', methods=['POST'])
def delete(transducer_id):
    if delete_transducer(transducer_id):
        flash(f'Transdutor #{transducer_id} excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir transdutor. ID não encontrado.', 'error')
    return redirect(url_for('index'))

@app.route('/check_notifications')
def check_notifications():
    """Rota para executar a checagem de notificações manualmente."""
    result = check_for_notifications()
    flash(result, 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)