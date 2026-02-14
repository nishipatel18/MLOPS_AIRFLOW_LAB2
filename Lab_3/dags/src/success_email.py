from airflow.models import Variable
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from airflow.hooks.base import BaseHook
from jinja2 import Template


def send_success_email(**kwargs):
    conn = BaseHook.get_connection('email_smtp')
    sender_email = conn.login
    password = conn.password

    receiver_emails = 'your_email@gmail.com'  # define receiver email

    subject_template = 'Airflow Success: {{ dag.dag_id }} - Wine Quality Pipeline tasks succeeded'
    body_template = '''Hi team,

    The Wine Quality Random Forest Pipeline tasks in DAG {{ dag.dag_id }} succeeded.

    Tasks completed:
    1. Data Loading (Wine Quality Dataset)
    2. Data Preprocessing (Feature Scaling)
    3. Model Training (Random Forest Classifier)
    4. Model Evaluation

    Please check the Airflow UI for detailed logs.'''

    subject = Template(subject_template).render(dag=kwargs['dag'], task=kwargs['task'])
    body = Template(body_template).render(dag=kwargs['dag'], task=kwargs['task'])

    email_message = MIMEMultipart()
    email_message['Subject'] = subject
    email_message['From'] = sender_email
    email_message['To'] = ", ".join(receiver_emails)

    email_message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        email_message.replace_header('To', receiver_emails)
        server.sendmail(sender_email, receiver_emails, email_message.as_string())
        print(f"Success email sent successfully to {receiver_emails}!")

    except Exception as e:
        print(f"Error sending success email: {e}")

    finally:
        server.quit()
