import os
import mimetypes
import time
import imaplib
import email

username = "kamandtrix@gmail.com"
password = "svmfjncazrvivceo"

def get_email():
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)

    # Select the mailbox you want to check
    mail.select("inbox")

    # Search for all emails and get the latest email ID
    status, email_ids = mail.search(None, "ALL")
    latest_email_id = email_ids[0].split()[-1]

    # Fetch the latest email by ID
    status, email_data = mail.fetch(latest_email_id, '(RFC822)')
    raw_email = email_data[0][1]

    # Return the email message object  
    return email.message_from_bytes(raw_email), latest_email_id


processed_email_ids = set()

def get_email_body_and_image():
    email, email_id = get_email()

    if email_id in processed_email_ids: 
        return None, None
    
    # Add the email ID to the set of processed email IDs
    processed_email_ids.add(email_id)

    # Extract the body from the email
    body = None
    if email.is_multipart():
        for part in email.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Check for the main text part of the email
            if "text/plain" in content_type and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()
                break

    # Check for attachments
    image_path = None
    if email.is_multipart():
        for part in email.walk():
            content_disposition = str(part.get("Content-Disposition"))
            # Check if part is an attachment
            if "attachment" in content_disposition:
                # Check if the attachment is an image
                mime_type, encoding = mimetypes.guess_type(part.get_filename())
                if mime_type and mime_type.startswith('image'):
                    # Save the image
                    image_path = save_image(part.get_payload(decode=True), part.get_filename())
                    break  # Exit once the first image is found, assuming one image per email

    return body, image_path

def save_image(image_data, filename):

    # Determine the base directory dynamically
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure there's a directory to save images
    img_dir = os.path.join(base_dir, 'stored-images')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    # Generate a unique filename based on the original filename
    base, ext = os.path.splitext(filename)
    unique_filename = base + "_" + str(int(time.time())) + ext  # appending timestamp

    image_path = os.path.join(img_dir, unique_filename)
    
    # Write the image data to the file
    with open(image_path, 'wb') as f:
        f.write(image_data)

    return image_path
