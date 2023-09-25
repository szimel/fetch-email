import time
# import os
# os.chdir('/home/kamandtrix/Desktop/fetch-email/')


from multiprocessing import Process, Manager
from background.display_email import display_email
from utils.email_utils import get_email_body_and_image

def email_check(shared_dict):
    while True:
        # Extracting the latest email's body, image path, and email ID
        body, image_path = get_email_body_and_image()

        # if we have a new email
        if body is None: 
            continue 
        else: 
            body = body.replace('\n', ' ').replace('\r', ' ')
            shared_dict['body'] = body
            shared_dict['image_path'] = image_path
        
        #check every 5 mins
        time.sleep(300)


if __name__ == '__main__':
    with Manager() as manager:
        shared_dict = manager.dict(body='', image_path=None)

        p1 = Process(target=display_email, args=(shared_dict,))
        p2 = Process(target=email_check, args=(shared_dict,))

        p1.start()
        p2.start()

        p1.join()
        p2.join()
