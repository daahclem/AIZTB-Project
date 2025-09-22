from ipfs_utils import upload_to_ipfs, get_ipfs_url


cid = upload_to_ipfs("blockchain/logs/sample_log.txt")
if cid:
    print(f"✅ Uploaded to IPFS with CID: {cid}")
    print(f"🔗 View at: {get_ipfs_url(cid)}")
else:
    print("❌ Upload failed.")
