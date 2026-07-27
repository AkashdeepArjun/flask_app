
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = 'sg2plzcpnl508264.prod.sin2.secureserver.net'
SMTP_PORT = 465
SENDER_EMAIL = 'akash@laziakeey.in'
SENDER_PASSWORD = 'akash@cpanel007007'  # <--- Put new password here
RECIPIENT_EMAIL = 'wadhwaarjun007@gmail.com' # <--- Put your test email here

print("Connecting to SMTP server...")

try:
    # Port 465 uses SSL directly
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
    print("SSL Connection established. Attempting login...")
    
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("Login successful!")

    msg = MIMEText("This is a direct Python SMTP test.")
    msg['Subject'] = "Direct SMTP Test"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    server.sendmail(SENDER_EMAIL, [RECIPIENT_EMAIL], msg.as_string())
    print("Email sent successfully via direct smtplib!")
    server.quit()

except Exception as e:
    print("\n--- EXACT SMTP ERROR ---")
    print(e)
    print("------------------------\n")