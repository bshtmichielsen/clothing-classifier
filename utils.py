import urllib.request
import numpy, os, pathlib, zipfile
from urllib.error import HTTPError
from PIL import Image

def download_and_extract_repo(repo_user, repo_name, local_dir):
    os.makedirs(local_dir, exist_ok=True)
    main_zip_url = f"https://github.com/{repo_user}/{repo_name}/archive/refs/heads/main.zip"
    master_zip_url = f"https://github.com/{repo_user}/{repo_name}/archive/refs/heads/master.zip"
    zip_file_path = os.path.join(local_dir, "repo.zip")
    def download_zip(url):
        try:   
            urllib.request.urlretrieve(url, zip_file_path)
            return True
        except HTTPError as e:
            if e.code == 404:
                return False
            else:
                raise
    if not download_zip(main_zip_url):
        if not download_zip(master_zip_url):
            raise Exception(f"Cannot download {repo_user}/{repo_name}: both main.zip and master.zip not found")
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(local_dir)
    os.remove(zip_file_path)
    if os.path.exists(os.path.join(local_dir, repo_name + "-main")):
        os.rename(os.path.join(local_dir, repo_name + "-main"), os.path.join(local_dir, repo_name))
    elif os.path.exists(os.path.join(local_dir, repo_name + "-master")):
        os.rename(os.path.join(local_dir, repo_name + "-master"), os.path.join(local_dir, repo_name))

def load_image(file, size):
    img = Image.open(file)
    img = img.resize((size, size))
    return numpy.array(img).flatten()

def load_labelled_images(path, size):
    labels = list()
    files = list()
    for file_info in [x for x in pathlib.Path(path).glob("**/*.jpg")]:
        labels.append(file_info.parts[len(file_info.parts)-2])
        files.append(str(file_info))
    imgs = numpy.array([load_image(f, size) for f in files])
    return imgs, numpy.array(labels) 