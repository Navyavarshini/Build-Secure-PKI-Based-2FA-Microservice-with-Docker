import requests
import json

with open("student_public.pem","r") as f:
    public_key = f.read()

data = {
  "student_id": "23MH1A4209",
  "github_repo_url": "https://github.com/Navyavarshini/Build-Secure-PKI-Based-2FA-Microservice-with-Docker",
  "public_key": public_key
}

url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
resp = requests.post(url, json=data)
print(resp.json())

with open("encrypted_seed.txt","w") as f:
    f.write(resp.json().get("encrypted_seed",""))
