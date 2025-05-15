import os
import uuid

TMP_BASE_DIR = "/tmp"

def get_unique_tmp_dir():
    """
    Generate a unique temporary directory path for each download request.
    This prevents race conditions when multiple users download files simultaneously.
    """
    unique_id = str(uuid.uuid4())
    tmp_dir = os.path.join(TMP_BASE_DIR, f"magdas_download_{unique_id}")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        
    return tmp_dir
