import time
from multiprocessing import Process
from background.display_email import display_email, update_vars
from utils.email_utils import get_body, get_subject, get_email

def email_check():
    while True:
        # Extracting the latest email using the util function
        email = get_email()

        # Extracting the body using the util functions
        new_body = get_body(email)
        new_subject = get_subject(email)
        
        new_body = new_body.replace('\n', ' ').replace('\r', ' ')
        
        update_vars(new_subject, new_body)
        
        # check every 5 mins
        time.sleep(300)

if __name__ == '__main__':
    p1 = Process(target=display_email)
    p2 = Process(target=email_check)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
