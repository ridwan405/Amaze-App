import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAVE_DIRECTORY = BASE_DIR/'utils'/'temp'

def handle_uploaded_file(f):
    with open(os.path.join(SAVE_DIRECTORY, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)