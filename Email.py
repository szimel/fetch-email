import time
# import os
# os.chdir('/home/kamandtrix/Desktop/fetch-email/')


from multiprocessing import Process, Manager
from background.display_email import display_email
from utils.email_utils import get_body, get_subject, get_email

def email_check(shared_dict):
    while True:
        # Extracting the latest email using the util function
        email = get_email()

        # Extracting the body using the util functions
        new_body = get_body(email)
        new_subject = get_subject(email)
        
        new_body = new_body.replace('\n', ' ').replace('\r', ' ')

        shared_dict['subject'] = new_subject
        shared_dict['body'] = new_body
        
        # check every 5 mins
        time.sleep(300)

if __name__ == '__main__':
    with Manager() as manager:
        shared_dict = manager.dict()
        shared_dict['subject'] = ''
        shared_dict['body'] = ''

        p1 = Process(target=display_email, args=(shared_dict,))
        p2 = Process(target=email_check, args=(shared_dict,))

        p1.start()
        p2.start()

        p1.join()
        p2.join()
