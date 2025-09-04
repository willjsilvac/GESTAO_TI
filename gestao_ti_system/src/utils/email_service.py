import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailService:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'smtp.json')
        self.config = self._load_config()
    
    def _load_config(self):
        """Carrega configurações SMTP do arquivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Erro ao carregar configurações SMTP: {e}")
            return None
    
    def is_configured(self):
        """Verifica se o SMTP está configurado"""
        if not self.config:
            return False
        
        required_fields = ['servidor', 'porta', 'usuario', 'senha']
        return all(self.config.get(field) for field in required_fields)
    
    def test_connection(self):
        """Testa a conexão SMTP"""
        if not self.is_configured():
            return False, "SMTP não configurado"
        
        try:
            server = smtplib.SMTP(self.config['servidor'], int(self.config['porta']))
            
            if self.config.get('ssl', True):
                server.starttls()
            
            server.login(self.config['usuario'], self.config['senha'])
            server.quit()
            
            return True, "Conexão SMTP bem-sucedida"
        except Exception as e:
            return False, f"Erro na conexão SMTP: {str(e)}"
    
    def send_password_recovery_email(self, email, token, user_name=""):
        """Envia email de recuperação de senha"""
        if not self.is_configured():
            return False, "SMTP não configurado"
        
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = f"{self.config.get('remetente_nome', 'Sistema de Gestão TI')} <{self.config.get('remetente_email', self.config['usuario'])}>"
            msg['To'] = email
            msg['Subject'] = "Recuperação de Senha - Sistema de Gestão TI"
            
            # Corpo do email
            recovery_link = f"http://18.219.145.132/redefinir-senha?token={token}"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Recuperação de Senha</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .button {{ display: inline-block; padding: 12px 24px; background-color: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Sistema de Gestão TI</h1>
                    </div>
                    <div class="content">
                        <h2>Recuperação de Senha</h2>
                        <p>Olá{f", {user_name}" if user_name else ""},</p>
                        <p>Você solicitou a recuperação de senha para sua conta no Sistema de Gestão TI.</p>
                        <p>Clique no botão abaixo para redefinir sua senha:</p>
                        <p style="text-align: center;">
                            <a href="{recovery_link}" class="button">Redefinir Senha</a>
                        </p>
                        <p>Ou copie e cole o link abaixo no seu navegador:</p>
                        <p style="word-break: break-all; background-color: #e5e7eb; padding: 10px; border-radius: 5px;">
                            {recovery_link}
                        </p>
                        <p><strong>Este link é válido por 1 hora.</strong></p>
                        <p>Se você não solicitou esta recuperação, ignore este email.</p>
                    </div>
                    <div class="footer">
                        <p>Sistema de Gestão TI - {datetime.now().strftime("%Y")}</p>
                        <p>Este é um email automático, não responda.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Sistema de Gestão TI - Recuperação de Senha
            
            Olá{f", {user_name}" if user_name else ""},
            
            Você solicitou a recuperação de senha para sua conta no Sistema de Gestão TI.
            
            Acesse o link abaixo para redefinir sua senha:
            {recovery_link}
            
            Este link é válido por 1 hora.
            
            Se você não solicitou esta recuperação, ignore este email.
            
            Sistema de Gestão TI - {datetime.now().strftime("%Y")}
            Este é um email automático, não responda.
            """
            
            # Anexar corpo do email
            msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Enviar email
            server = smtplib.SMTP(self.config['servidor'], int(self.config['porta']))
            
            if self.config.get('ssl', True):
                server.starttls()
            
            server.login(self.config['usuario'], self.config['senha'])
            server.send_message(msg)
            server.quit()
            
            return True, "Email enviado com sucesso"
            
        except Exception as e:
            return False, f"Erro ao enviar email: {str(e)}"
    
    def send_notification_email(self, to_email, subject, message, user_name=""):
        """Envia email de notificação genérico"""
        if not self.is_configured():
            return False, "SMTP não configurado"
        
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = f"{self.config.get('remetente_nome', 'Sistema de Gestão TI')} <{self.config.get('remetente_email', self.config['usuario'])}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Corpo do email
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{subject}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Sistema de Gestão TI</h1>
                    </div>
                    <div class="content">
                        <h2>{subject}</h2>
                        <p>Olá{f", {user_name}" if user_name else ""},</p>
                        <div style="white-space: pre-line;">{message}</div>
                    </div>
                    <div class="footer">
                        <p>Sistema de Gestão TI - {datetime.now().strftime("%Y")}</p>
                        <p>Este é um email automático, não responda.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Sistema de Gestão TI - {subject}
            
            Olá{f", {user_name}" if user_name else ""},
            
            {message}
            
            Sistema de Gestão TI - {datetime.now().strftime("%Y")}
            Este é um email automático, não responda.
            """
            
            # Anexar corpo do email
            msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Enviar email
            server = smtplib.SMTP(self.config['servidor'], int(self.config['porta']))
            
            if self.config.get('ssl', True):
                server.starttls()
            
            server.login(self.config['usuario'], self.config['senha'])
            server.send_message(msg)
            server.quit()
            
            return True, "Email enviado com sucesso"
            
        except Exception as e:
            return False, f"Erro ao enviar email: {str(e)}"

# Instância global do serviço de email
email_service = EmailService()

