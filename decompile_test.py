import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()
    
evt_path = os.path.join(os.getcwd(), "extracted_ards", "al00.ard", "evt.script")
lib.editengine.spawnscript_extract(evt_path, os.path.join(os.getcwd(), "fak.txt"))