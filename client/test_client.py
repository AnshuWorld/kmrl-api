import requests

files = {"files": open("sample.txt", "rb")}
res = requests.post("http://localhost:8000/process-doc/", files=files)
print(res.json())
