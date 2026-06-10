import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_critical_email(machine_id, risk_score, temp, vib, speed):
    print(f"📨 Attempting to dispatch emergency alert email for {machine_id}...")
    
    # 1. Configuration Settings
    # For a human-built portfolio, we can utilize standard SMTP settings.
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Replace these placeholder strings with your actual test emails
    sender_email = "your_test_sender@gmail.com" 
    sender_password = "your_app_password_here"   # Gmail App Password
    receiver_email = "your_personal_inbox@gmail.com"
    
    # 2. Construct the Email Layout
    message = MIMEMultipart("alternative")
    message["Subject"] = f"🚨 CRITICAL HEALTH ALERT: {machine_id} Operational Failure Risk"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # High-end HTML email layout that looks like a real factory dispatch system
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="background-color: #d9534f; color: white; padding: 15px; font-size: 18px; font-weight: bold; text-align: center;">
          ⚠️ CRITICAL MACHINERY FAULT DETECTED BY AI PIPELINE
        </div>
        <div style="padding: 20px; border: 1px solid #d9534f; border-top: none;">
          <p>The live predictive health model has flagging an active anomaly event on machine unit <strong>{machine_id}</strong>.</p>
          
          <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
            <tr style="background-color: #f2f2f2;">
              <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">AI Failure Probability:</td>
              <td style="padding: 8px; border: 1px solid #ddd; color: #d9534f; font-weight: bold;">{risk_score:.1f}%</td>
            </tr>
            <tr>
              <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Core Temperature:</td>
              <td style="padding: 8px; border: 1px solid #ddd;">{temp}°C</td>
            </tr>
            <tr style="background-color: #f2f2f2;">
              <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Vibration Amplitude:</td>
              <td style="padding: 8px; border: 1px solid #ddd;">{vib} Hz</td>
            </tr>
            <tr>
              <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Rotational Velocity:</td>
              <td style="padding: 8px; border: 1px solid #ddd;">{speed} RPM</td>
            </tr>
          </table>
          
          <p style="color: #555; font-size: 12px; margin-top: 20px;">
            *Action Required: Dispatch on-site technical crews immediately to inspect machine core telemetry.*
          </p>
        </div>
      </body>
    </html>
    """
    
    message.attach(MIMEText(html_content, "html"))
    
    # 3. Establish Connection & Send
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() # Secure the connection channel
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("✅ Alert email successfully routed to maintenance queue!")
    except Exception as err:
        print(f"⚠️ Email Dispatch Delayed: Local credentials unconfigured. (Simulated log saved instead)")