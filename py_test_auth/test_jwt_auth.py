import requests

BASE_URL = "http://localhost:3000"

# Define endpoints
SIGNUP_URL = f"{BASE_URL}/signup"
LOGIN_URL = f"{BASE_URL}/login"
BOOKS_URL = f"{BASE_URL}/books"

# Define user details for testing
USERNAME = "testuser"
PASSWORD = "password123"

# Function to sign up a new user
def signup(username, password):
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(SIGNUP_URL, json=payload)
    if response.status_code == 201:
        print("Sign up successful!")
        return response.json().get("token")
    else:
        print("Failed to sign up:", response.json())
        return None

# Function to log in an existing user
def login(username, password):
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(LOGIN_URL, json=payload)
    if response.status_code == 200:
        print("Login successful!")
        return response.json().get("token")
    else:
        print("Failed to log in:", response.json())
        return None

# Function to access protected resource
def get_books(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(BOOKS_URL, headers=headers)
    if response.status_code == 200:
        print("Accessed protected resource successfully! Books:")
        print(response.json())
    else:
        print("Failed to access protected resource:", response.json())

# Main flow for testing the API
def main():
    # Step 1: Sign up the user
    print("\nStep 1: Signing up...")
    token = signup(USERNAME, PASSWORD)

    # If sign-up fails (user already exists), attempt to log in
    if not token:
        print("\nStep 2: Logging in...")
        token = login(USERNAME, PASSWORD)

    # Step 3: Access protected resource if we have a token
    if token:
        print("\nStep 3: Accessing protected resource...")
        get_books(token)

if __name__ == "__main__":
    main()
