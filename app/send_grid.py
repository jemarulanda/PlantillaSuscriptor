from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendGrid(object):
    @classmethod
    def create_message(cls, api_key:str, from_email:str, emails:list ,message:str):
        for email in emails:
            message_send = Mail(
                from_email=from_email,
                to_emails=email['email'],
                subject='Integración WMSOrdenesCompra Publish',
                html_content=f"<strong>El sistema presenta la siguiente novedad:</strong></br><p>{message}</p>"
            )
            cls.send_message(api_key, message_send)      

    @classmethod
    def send_message(cls, api_key:str, message:str):
        try:
            sg = SendGridAPIClient(api_key)
            sg.send(message)
        except Exception as e:
            print(str(e))