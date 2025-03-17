import json
import argparse
import os

from schnorr_lib import (
    p, y, G, point_add, sha256, lift_x_even_y, 
    bytes_from_int, n, int_from_bytes, int_from_hex, 
    point_mul, x
)

def load_json(file_path):
    """Load JSON data from a file safely."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON in '{file_path}': {e}")
        return None

def main():
    # Load data from JSON files
    data = load_json("data.json")
    user_data = load_json("users1.json")

    if data is None or user_data is None:
        return  # Exit if files failed to load

    # Extract users
    users = data.get("users", [])
    user_list = user_data.get("users", [])

    # Ensure required user data exists
    if not users or not user_list:
        print("Error: No users found in one or both JSON files")
        return

    # Extract first user's details
    user1 = users[0]  # First user in data.json
    alpha = user1.get("alpha")
    beta = user1.get("beta")
    c = user1.get("c")
    signature = user1.get("signature")

    user2 = user_list[0]  # First user in users1.json
    private_key = user2.get("privateKey")
    nonce = user2.get("nonce")
    rnonce = user2.get("Rnonce")
    public_key = user2.get("publicKey")

    # Ensure all required values are available
    if None in [signature, public_key, c, rnonce]:
        print("Error: Missing required data in JSON files")
        return

    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Verify a Schnorr signature from a public key, message, and signature'
    )
    parser.add_argument('-s', '--signature', type=str, required=False, default=signature, help='Signature (default from JSON)')
    parser.add_argument('-p', '--public_key', type=str, required=False, default=public_key, help='Public key (default from JSON)')
    parser.add_argument('-c', '--cin', type=str, required=False, default=c, help='cin (default from JSON)')
    parser.add_argument('-r', '--nonce', type=str, required=False, default=rnonce, help='nonce (default from JSON)')

    args = parser.parse_args()

    sig_hex = args.signature
    public_key = args.public_key
    c = args.cin
    rnonce = args.nonce

    # Validate hex inputs before processing
    try:
        sig = int_from_hex(sig_hex)
        public_key_int = int_from_hex(public_key)
        c_int = int_from_hex(c)
        rnonce_int = int_from_hex(rnonce)
    except ValueError:
        print("Error: Invalid hex value in inputs")
        return
    
    # Compute points
    V_point = point_mul(G, sig)

    try:
        P = lift_x_even_y(bytes_from_int(public_key_int))
    except Exception as e:
        print(f"Error: Failed to compute P: {e}")
        return

    if y(P) is None:
        print("Error in calculation of y of P in verification")
        return

    T_point = point_mul(P, n - c_int)
    T = point_add(V_point, T_point)

    # Validate signature
    if x(T) == rnonce_int:
        print("YES - Signature is valid")
    else:
        print("NO - Signature is invalid")

if __name__ == "__main__":
    main()