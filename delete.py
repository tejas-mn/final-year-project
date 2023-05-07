# importing required modules
import os
import time
import threading

current_time = time.time()
  
# "day" is the number of seconds in a day : 86400
day = 30.0
  
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','JPG', 'JPEG', 'PNG'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def scheduleDelete(folder : str , NoOfdays : int):
    print("--------")
    threading.Timer(day*NoOfdays, scheduleDelete, ['static' , 1]).start()
    list_of_files = os.listdir('static')   
    for i in list_of_files:
        file_location = os.path.join('static', i)

        # file_time is the time when the file is modified
        # file_time = os.stat(file_location).st_mtime

        # if a file is modified before N days then delete it | and file_time < current_time - day*NoOfdays
        if(allowed_file(i) ):
            print(f" Delete : {i}")
            os.remove(file_location)