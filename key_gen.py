import argparse, json, os, schnorr_lib
from schnorr_lib import n , point_mul, G, x, pubkey_point_gen_from_int ,bytes_from_point, has_even_y

def create_keypair():
    users = {
        "$schema": "./users_schema.json",
        "users": []
    }

    privkey = os.urandom(32)
    privkey_int = int(privkey.hex(), 16) % n
    publickey = pubkey_point_gen_from_int(privkey_int)
    privkey_even = privkey_int if has_even_y(publickey) else n - privkey_int

    nonce=os.urandom(32)
    nonce_int=int(nonce.hex(),16) % n

    Rnonc=point_mul(G,nonce_int)
    
    nonce_int=nonce_int if has_even_y(Rnonc) else n - nonce_int
    Rnonce=x(Rnonc)
    # print(Rnonce)
    # print(nonce_int)
    hex_privkey = hex(privkey_int).replace('0x', '').rjust(64, '0')
    hex_nonce = hex(nonce_int).replace('0x', '').rjust(64, '0')
    hex_pub=hex(x(publickey)).replace('0x', '').rjust(64, '0')
    hex_Rnonce=hex(Rnonce).replace('0x', '').rjust(64, '0')
    users["users"].append({
    "privateKey": hex_privkey,
    "nonce":hex_nonce ,
    "Rnonce": hex_Rnonce,
    "publicKey": hex_pub
    
    })
    return users

def main():
    users = create_keypair()

    json_object = json.dumps(users, indent=4)
    with open("users1.json", "w") as f:
        f.write(json_object)

    print("Keypair generated:" )


if __name__ == "__main__":
    main()
