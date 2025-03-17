import argparse
import json
import os
from schnorr_lib import G,lift_x_even_y,y,point_add,bytes_from_point,has_even_y, p, sha256, bytes_from_int, n, int_from_bytes, int_from_hex, point_mul, x

JSON_FILE = "data.json"  # Change this to your actual JSON file path

def creator():
    parser = argparse.ArgumentParser(
        description='It checks the validity of the sign and returns True or False from a public key, a message and a signature'
    )
    parser.add_argument('-r', '--random', type=str, required=True, help='Signature')
    parser.add_argument("-p", "--public_key", type=str, required=True, help='Public key or public aggregate X~')
    parser.add_argument('-m', '--message', type=str, required=True, help='Message')

    args = parser.parse_args()
    random_hex = args.random
  

    R = int_from_hex(random_hex)
    R_point=lift_x_even_y(bytes_from_int(R))
    R=R if has_even_y(R_point) else n-R
    # print(R)
    public_key = int_from_hex(args.public_key)
    message = args.message

    # Generate alpha and beta
    alpha = os.urandom(32)
    alpha_int = int(alpha.hex(), 16) % n
    beta = os.urandom(32)
    beta_int = int(beta.hex(), 16) % n

    # Compute Malpha and Mbeta
    Malpha = point_mul(G, alpha_int)
    P_point = lift_x_even_y(bytes_from_int(public_key)) 
     # Full EC point
    if (y(P_point)==None):
        print("error in calculation of y of P_point")
    Mbeta = point_mul(P_point, beta_int)

    # Compute Rprime
    # Rprime = (R + Malpha + Mbeta) % n
    Rprime=point_add(R_point,point_add(Malpha,Mbeta))
    # Compute c
    msg = bytes_from_point((Rprime)) + message.encode()
    cprime = sha256(msg)
    c = (int_from_bytes(cprime) + beta_int) % n

    # Convert values to hexadecimal for JSON storage
    alpha_hex = hex(alpha_int).replace('0x', '').rjust(64, '0')
    beta_hex = hex(beta_int).replace('0x', '').rjust(64, '0')
    c_hex = hex(c).replace('0x', '').rjust(64, '0')
    # print(alpha_hex)
    # print(beta_hex)
    # print(c_hex)
    # Load existing JSON data
    data = {
        "users": [{
            "alpha": alpha_hex,
            "beta": beta_hex,
            "c": c_hex
        }]
    }

    # Save updated JSON (overwriting existing content)
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print("Values saved successfully:", data["users"])

if __name__ == "__main__":
    creator()
