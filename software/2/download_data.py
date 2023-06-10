from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import subprocess
import os
import json
import kaggle

usr_name = os.environ['KAGGLE_USERNAME']
key = os.environ['KAGGLE_KEY']
k = kaggle.KaggleApi({"username": usr_name, "key": key})

# Create kaggle.json file with the provided credentials
kaggle_json = {"username": os.environ['KAGGLE_USERNAME'], "key": os.environ['KAGGLE_KEY']}
os.makedirs(os.path.expanduser('home/runner/.kaggle'), exist_ok=True)
with open(os.path.expanduser('/home/runner/.kaggle/kaggle.json'), 'w') as f:
    json.dump(kaggle_json, f)
os.chmod(os.path.expanduser('/home/runner/.kaggle/kaggle.json'), 0o600)

api = KaggleApi()

# download the dataset using the kaggle API
api.dataset_download_files('uciml/electric-power-consumption-data-set', path=".")

# open the ZIP file in read mode
with zipfile.ZipFile('electric-power-consumption-data-set.zip', 'r') as zip_ref:
    # extract all files to the current working directory
    zip_ref.extractall()
