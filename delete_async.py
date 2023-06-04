import glob
import os
import asyncio
import time

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','JPG', 'JPEG', 'PNG'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


async def delete_file(file_path):
    try:
        file_location = os.path.join('static', file_path)
        if allowed_file(file_location):
            os.remove(file_location)
            print(f"Deleted file: {file_path}")
    except OSError as e:
        print(f"Error deleting file: {file_path} ({e})")


async def delete_files():
        files = os.listdir('static')  # Replace with the actual path and file extension

        # Delete each file asynchronously
        delete_tasks = [delete_file(file) for file in files]

        # Wait for all delete tasks to complete
        await asyncio.gather(*delete_tasks)

       

def start_deletion():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(delete_files())
    return 'File deletion has started.'

