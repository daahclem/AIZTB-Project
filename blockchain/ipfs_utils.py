import requests

IPFS_API = "http://127.0.0.1:5001/api/v0"

def upload_to_ipfs(file_path):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(f"{IPFS_API}/add", files=files)
        if response.status_code == 200:
            return response.json()["Hash"]
        else:
            print("❌ Upload failed:", response.text)
            return None

def get_ipfs_url(cid):
    return f"https://ipfs.io/ipfs/{cid}"

def download_from_ipfs(cid, output_path):
    url = f"https://ipfs.io/ipfs/{cid}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print("❌ Download failed:", response.status_code)
        return False
