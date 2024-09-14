import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Function to send an email with an attachment
def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    with open(attachment_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
    msg.attach(part)

    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, smtp_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# Define the target URL (example)
url = 'https://punchng.com/feed/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# Define the keywords to search for
risk_keywords = ['Rape', 'Kidnapping', 'Terrorism', 'Assaults', 'Homicide', 'Cultism', 'Piracy', 'Drowning', 'Armed Robbery', 'Fire Outbreak', 'Unsafe Route/Violent Attacks', 'Human Trafficking', 'Organ Trafficking']
life_death_keywords = ['Killed','casualties','casualty', 'dies', 'death', 'kill']
state_keywords = ['Abuja','Abia','Adamawa','Akwa Ibom','Anambra','Bauchi','Bayelsa','Benue','Borno','Cross River','Delta','Ebonyi','Edo','Ekiti','Enugu','Gombe','Imo','Jigawa','Kaduna','Kano','Katsina','Kebbi','Kogi','Kwara','Lagos','Nassarawa','Niger','Ogun','Ondo','Osun','Oyo','Plateau','Rivers','Sokoto','Taraba','Yobe','Zamfara']
case_situation_keywords = ['victims','victim','injured']

# Extract and categorize the news
data = []
for item in soup.find_all('item'):
    title = item.title.get_text()
    link = item.link.get_text()

    risk_indicator = 'NO'
    life_death = 'NO'
    state = 'NO'
    case_situation = 'NO'

    for keyword in risk_keywords:
        if keyword.lower() in title.lower():
            risk_indicator = keyword
            break

    for keyword in life_death_keywords:
        if keyword.lower() in title.lower():
            life_death = keyword
            break

    for keyword in state_keywords:
        if keyword.lower() in title.lower():
            state = keyword
            break

    for keyword in case_situation_keywords:
        if keyword.lower() in title.lower():
            case_situation = keyword
            break

    data.append({
        'title': title, 
        'link': link, 
        'Risk Indicator': risk_indicator,
        'Life/Death': life_death,
        'States': state,
        'Case Situation': case_situation
    })

# Store data in a DataFrame and save as CSV
df = pd.DataFrame(data)
csv_filename = 'news_headlines.csv'
df.to_csv(csv_filename, index=False)

# Email configuration
#sender_email = ""
sender_email = os.environ.get('USER_EMAIL')
receiver_email = "riskcontrolservicesnig@gmail.com"
subject = "Daily News Headlines"
body = "Please find attached the latest news headlines with categorized information."
smtp_server = "smtp.gmail.com"
smtp_port = 587
#smtp_password = ""
smtp_password = os.environ.get('USER_PASSWORD')
# Send the email
send_email(sender_email, receiver_email, subject, body, csv_filename, smtp_server, smtp_port, smtp_password)

print("Scraping, categorization, and email sent successfully.")


