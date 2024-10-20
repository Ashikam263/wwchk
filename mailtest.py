from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email credentials
sender_email = "your-email@example.com"
receiver_email = "your-email@example.com"
email_password = "your-password"

# WhatsApp contact to monitor
contact_name = "Person Name"

# Set up Selenium for Edge browser
options = webdriver.EdgeOptions()
options.add_argument("--user-data-dir=C:/Users/Your-User-Name/AppData/Local/Microsoft/Edge/User Data")
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# Send email function
def send_email(status, timestamp):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"WhatsApp Contact {status}"

    body = f"The contact {contact_name} is now {status}.\nTime: {timestamp}"
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")

input("Press Enter after scanning QR code to continue...")

# Initialize start time
start_time = time.time()  # Capture the start time when the script begins
last_status = None

try:
    while True:
        time.sleep(5)  # Check every 5 seconds

        try:
            # Locate contact and check if they are online
            contact = driver.find_element(By.XPATH, f"//span[@title='{contact_name}']")
            contact.click()
            online_status = driver.find_element(By.XPATH, "//span[contains(text(),'online')]")

            if online_status and last_status != 'online':
                last_status = 'online'
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{contact_name} came online at {timestamp}")
                send_email('online', timestamp)

        except:
            if last_status == 'online':
                last_status = 'offline'
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{contact_name} went offline at {timestamp}")
                send_email('offline', timestamp)

        # Keep running for 24 hours
        if time.time() - start_time > 86400:  # 24 hours in seconds
            break

finally:
    driver.quit()
