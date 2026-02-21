import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification_email(config, transducers_to_notify):
    """
    Envia um e-mail de notificação sobre transdutores próximos do vencimento
    usando o método SMTPLib padrão do Python.
    
    Args:
        config (dict): Dicionário com as configurações de e-mail (SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD, RECIPIENTS).
        transducers_to_notify (list): Lista de dicionários de transdutores que precisam de notificação.
    """
    
    if not transducers_to_notify:
        return "Nenhum transdutor para notificar."

    # Cria o corpo do e-mail
    subject = f"ALERTA DE VENCIMENTO DE TRANSDUTORES - {len(transducers_to_notify)} Itens"
    
    # Cria a tabela HTML para o corpo do e-mail
    table_rows = "".join([
        f"<tr>"
        f"<td>{t['id']}</td>"
        f"<td>{t['descricao']}</td>"
        f"<td>{t['numero_serie']}</td>"
        f"<td>{t['localizacao']}</td>"
        f"<td>{t['validade_formatada']}</td>"
        f"<td style='color: {'#ED1C24' if t['dias_restantes'] <= 10 else '#ffc107'}; font-weight: bold;'>{t['dias_restantes']} dias</td>"
        f"</tr>"
        for t in transducers_to_notify
    ])
    
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .header {{ background-color: #4B1F68; color: white; padding: 10px; text-align: center; }}
                .container {{ margin: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Alerta de Vencimento de Transdutores</h2>
            </div>
            <div class="container">
                <p>Prezado(a) usuário(a),</p>
                <p>Os seguintes transdutores estão próximos da data de validade:</p>
                
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Descrição</th>
                            <th>Nº de Série</th>
                            <th>Localização</th>
                            <th>Validade (Dia/Mês/Ano)</th>
                            <th>Dias para Vencer</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                
                <p>Por favor, tome as medidas necessárias.</p>
                <p>Este é um e-mail automático. Por favor, não responda.</p>
            </div>
        </body>
    </html>
    """
    
    msg = MIMEMultipart('alternative')
    msg['From'] = config['EMAIL_USER']
    msg['To'] = ", ".join(config['RECIPIENTS'])
    msg['Subject'] = subject
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # Conecta ao servidor SMTP
        # Se a porta for 465, usa SMTP_SSL (SSL implícito)
        # Se a porta for 587 ou outra, usa SMTP padrão e starttls()
        if config['SMTP_PORT'] == 465:
            server = smtplib.SMTP_SSL(config['SMTP_SERVER'], config['SMTP_PORT'])
        else:
            server = smtplib.SMTP(config['SMTP_SERVER'], config['SMTP_PORT'])
            server.starttls() # Necessário para o Gmail na porta 587
            
        with server:
            server.login(config['EMAIL_USER'], config['EMAIL_PASSWORD'])
            server.sendmail(config['EMAIL_USER'], config['RECIPIENTS'], msg.as_string())
            
        return f"E-mail de notificação enviado com sucesso via SMTPLib para {len(config['RECIPIENTS'])} destinatários."
    except Exception as e:
        return f"Erro ao enviar e-mail de notificação via SMTPLib. Erro: {e}"

if __name__ == '__main__':
    print("Módulo de envio de e-mail pronto para usar SMTPLib.")