import os
import shutil

def static_to_public(start_path:str,final_path:str):
    if os.path.exists(final_path):
        shutil.rmtree(final_path)
    shutil.copytree(start_path, final_path)
