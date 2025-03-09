import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationManager:
    def __init__(self):
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': '587',
            'email': '',
            'password': ''
        }

    def configure_email(self, config):
        """E-posta ayarlarını yapılandırır"""
        self.email_config.update(config)

    def send_email(self, to_email, subject, message):
        """E-posta gönderir"""
        try:
            if not all(self.email_config.values()):
                return False, "E-posta ayarları eksik"

            msg = MIMEMultipart()
            msg['From'] = self.email_config['email']
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(
                self.email_config['smtp_server'],
                self.email_config['smtp_port']
            )
            server.starttls()
            server.login(
                self.email_config['email'],
                self.email_config['password']
            )
            
            server.send_message(msg)
            server.quit()
            return True, "E-posta başarıyla gönderildi"
            
        except Exception as e:
            return False, f"E-posta gönderilirken hata oluştu: {str(e)}" 