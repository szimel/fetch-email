import imaplib
import smtplib
import email
from email.header import decode_header

username = "kamandtrix@gmail.com"
password = "svmfjncazrvivceo"

def send_email(subject, body):
    receiver_email = "zamdaman9999@gmail.com"
    # Set up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Log into the server
    server.login(username, password)

    # Send the email
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(username, receiver_email, message)

    # Disconnect from the server
    server.quit()

def wrap_text(text, font, max_width):
    """
    Wrap text to fit within a specified width.
    """
    words = text.split(' ')
    wrapped_lines = []
    current_line = words[0]
   
    for word in words[1:]:
        # Test the width with the new word added
        test_line = current_line + ' ' + word
        # If the width with the new word doesn't exceed the max width
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word

    wrapped_lines.append(current_line)
    return '\n'.join(wrapped_lines)

# extract body from email
def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
           
            # Extract only the plain text content
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode()
        return "There was an error, text Samuel"
    else:
        return msg.get_payload(decode=True).decode()

# Extract subject from email
def get_subject(msg):
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        return subject.decode(encoding if encoding else "utf8")
    return subject

# grabs latest email
def get_email():
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)

    # Select the mailbox you want to check
    mail.select("inbox")

    # Search for all emails
    result, messages = mail.search(None, "ALL")
    email_ids = messages[0].split(b' ')

    # Get the latest email
    result, message = mail.fetch(email_ids[-1], "(RFC822)")

    # Extract the email content
    msg = email.message_from_bytes(message[0][1])
    
    # Close the connection
    mail.logout()
    
    return msg
