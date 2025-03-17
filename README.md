# blind_schnorr_implementation
This repository contains an implementation of the Blind Schnorr Signature scheme, enabling blind signing for privacy-preserving authentication. It includes key generation, blind signing, and signature verification using secure randomization techniques. Clone the repo and follow the README for setup. Contributions are welcome! 🚀
# Blind Schnorr Signature Implementation

## Overview
Blind Schnorr Signatures are a cryptographic protocol that enables a signer to generate a signature on a message without seeing its contents. This provides privacy and is useful in applications such as anonymous credentials and digital cash systems.

This repository implements the Blind Schnorr Signature scheme, including:
- Key generation
- Blind signing process
- Signature verification
- Secure randomization techniques

## How It Works
1. **Key Generation**: The signer generates a public-private key pair.
2. **Blinding**: The sender blinds their message so the signer cannot see its content.
3. **Signing**: The signer signs the blinded message.
4. **Unblinding**: The sender removes the blinding factor, obtaining a valid signature.
5. **Verification**: Anyone can verify the signature against the original message.

## Repository Structure
```
├── schnorr_lib.py    # Core cryptographic functions
├── blinding.py        # Handles the blinding process
├── verify.py        # Signature verification
├── signature.py       # signature creation
├── key_gen.py       # Key generation 
```

## Installation & Setup
### Clone the Repository
```sh
git clone https://github.com/arnav7897/blind_schnorr_implementation.git
cd blind_schnorr_implementation
```

### Install Dependencies
Ensure you have Python 3 installed and install required libraries:
```sh
pip install -r requirements.txt
```

## Usage
### Key Generation
Run the key creator script to generate a key pair:
```sh
python3 key_gen.py  
```
# users1.json will be created 

### Blind Signing Process
1. Run the blinding.py to run blind process where it create users1.json and from there we can get value of rnounce and public_key:
```sh
python3 binding.py -r "rnounce" -p "public_key" -m "message"
```
# data.json will be created 

2. Use `signature.py` to create signature:
```sh
python3 signature.py
```
### Unbinding and verification
1. Use `verify.py` to create signature:
```sh
python3 verify.py
```
2. Inorder to check for other public key , signature , cin value one can use optional parsing like :
```sh
python3 verify.py -r "rnounce" -s "random signature" -p "random public_key" -c "random cin value"
```
## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License.

---
**Author:** Arnav Sharda , Rineet Pandey , Aniket Gupta

