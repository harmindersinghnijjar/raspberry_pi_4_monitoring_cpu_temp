import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import datetime
import os

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('email_sender.log', mode='a')
log_format = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s - '
                               '[%(process)d:%(thread)d]')
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

def send_initial_email(subject, text, to, files):
    """Send an initial email with attachments."""
    send_email(subject, text, to, files)

def send_followup_email(subject, text, to, video_path):
    """Send a follow-up email with attachments."""
    send_email(subject, text, to, [video_path])

def send_email(subject, text, to, files):
    """Send an email with attachments."""
    assert isinstance(to, list)
    assert isinstance(files, list)

    msg = MIMEMultipart()
    msg['From'] = 'your_email@example.com'  # Replace with your email address
    msg['To'] = ', '.join(to)
    msg['Date'] = datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for file in files:
        part = MIMEBase('application', "octet-stream")
        with open(file, 'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')
        msg.attach(part)

    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('your_email@example.com', 'your_email_password')  # Replace with your email and password
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp.quit()
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        print(f"Failed to send email: {e}")
