import json
import os
from schnorr_lib import p, y, G, point_add, sha256, lift_x_even_y, bytes_from_int, n, int_from_bytes, int_from_hex, point_mul, x

def main():
    # Open and read the first JSON file
    with open("data.json", "r") as file1:
        data = json.load(file1)  

    # Extract "users" list safely
    users = data.get("users", [])

    # Open and read the second JSON file
    with open("users1.json", "r") as file2:
        user_data = json.load(file2)

    # Extract users from the second JSON file
    user_list = user_data.get("users", [])

    # Store the first user's details in variables (assuming at least one user exists)
    if users:
        user1 = users[0]  # First user in data.json
        alpha = user1.get("alpha")
        beta = user1.get("beta")
        c = user1.get("c")
    else:
        print("Error: No users found in data.json")
        return

    # Store the first user's details from users1.json
    if user_list:
        user2 = user_list[0]  # First user in users1.json
        private_key = user2.get("privateKey")
        nonce = user2.get("nonce")
        rnonce = user2.get("Rnonce")
        public_key = user2.get("publicKey")
    else:
        print("Error: No users found in users1.json")
        return

    # Compute Signature
    sig = (int_from_hex(nonce) + (int_from_hex(c) * int_from_hex(private_key)) % n) % n
    print("Signature:", hex(sig))
    sigPrime = (sig + int_from_hex(alpha)) % n  # Ensure modulo n

    # Save the signature in data.json without "0x"
    user1["signature"] = hex(sig)[2:]
    with open("data.json", "w") as file1:
        json.dump(data, file1, indent=4)
    print("Signature saved successfully in data.json")

# Run the function
main()
