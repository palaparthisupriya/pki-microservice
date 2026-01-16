import requests
import json

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    # Step 1: Read student public key from PEM file
    try:
        with open("student_public.pem", "r") as f:
            public_key = f.read().strip()
    except FileNotFoundError:
        print("Error: student_public.pem not found!")
        return

    # Step 2: Prepare HTTP POST request payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    # Step 3: Send POST request to instructor API
    print(f"Sending request to API...")
    try:
        # Note: We use a timeout of 10 seconds to avoid hanging
        response = requests.post(
            api_url, 
            json=payload, 
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Step 4: Parse JSON response / Handle error responses
        if response.status_code == 200:
            data = response.json()
            encrypted_seed = data.get("encrypted_seed")
            
            # Step 5: Save encrypted seed to file
            if encrypted_seed:
                with open("encrypted_seed.txt", "w") as f:
                    f.write(encrypted_seed)
                print("✅ Success! Seed saved to encrypted_seed.txt")
            else:
                print("❌ API returned 200 but no seed was found in JSON.")
        
        elif response.status_code == 403:
            print("❌ 403 Forbidden: The API rejected your Student ID or Repo URL.")
            print(f"Server says: {response.text}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")

# EXECUTION
# Ensure the URL matches exactly what was in your objective text
target_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"
# RE-CHECK YOUR STUDENT ID HERE
my_id = "23A91A05H7" 
my_repo = "https://github.com/palaparthisupriya/pki-microservice"

request_seed(my_id, my_repo, target_url)