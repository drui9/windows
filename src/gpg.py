# check soft-hardware code signature
# monitor soft-hardware for changes
import gnupg, os, hashlib, base64

#stdout.clear()
cwd= os.getcwd()
gnupghome= os.path.join(cwd, '.gnupg')
if not os.path.exists(gnupghome):
  os.mkdir(gnupghome)

# --
gpg= gnupg.GPG(gnupghome=gnupghome)

if not os.path.exists('private-key'):
  # Prepare key generation parameters
  input_data = gpg.gen_key_input(
    name_real=grammer.instance_name,
    name_email='email@example.com',
    passphrase='passphrase',
    key_type='RSA',
    key_length=2048
  )

  # Generate the key
  key = gpg.gen_key(input_data)
  fingerprint = key.fingerprint
  print(f"Generated key with fingerprint: {fingerprint}")

  # Export public key (ASCII armored format)
  private_key = gpg.export_keys(fingerprint, True, passphrase='passphrase')
  with open('private-key', 'w') as pk:
    pk.write(private_key)
else:
  with open('private-key', 'r') as pk:
    private_key = pk.read()

# Import the key
#print(help(gpg.import_keys))
import_result = gpg.import_keys(private_key)
print(f"Imported {import_result.count} key(s)")
print(f"Fingerprints: {import_result.fingerprints}")
#print(gpg.list_keys(True))

# Read the file to encrypt
with open(grammer.instance_name, 'rb') as f:
    data = f.read()

# Encrypt using recipient's email or key ID
encrypted_data = gpg.encrypt(
    data, 
    'email@example.com',  # Recipient's key identifier
    always_trust=True         # Skip trust confirmation
)
encrypted_data = str(encrypted_data)
# Decrypt with passphrase
decrypted_data = gpg.decrypt(
    encrypted_data, 
    passphrase='passphrase'
)

# --
#print(decrypted_data)
print(decrypted_data.ok)  # True if decryption succeeded
#print(decrypted_data.stderr)  # Any error messages

# -------- fjle signing
with open('important_file.txt', 'rb') as f:
    data = f.read()

# Create a detached signature
signature = gpg.sign(
    data, 
    keyid=fingerprint,           # Your key fingerprint
    passphrase='your-secure-passphrase',
    detach=True                  # Creates separate signature file
)

# Save signature
with open('important_file.txt.sig', 'wb') as f:
    f.write(str(signature))
    
# 
# Read original file and signature
with open('important_file.txt.sig', 'rb') as f:
    sig_data = f.read()

# Verify signature
verified = gpg.verify(data, sig_data)

if verified:
    print(f"Signature valid! Signed by: {verified.username}")
    print(f"Key fingerprint: {verified.fingerprint}")
else:
    print("Signature invalid!")
    
    
# Export public key (ASCII armored format)
public_key = gpg.export_keys(fingerprint)  # False = public keys

with open('my_public_key.asc', 'w') as f:
    f.write(public_key)

# Export private key if needed (use with caution)
private_key = gpg.export_keys(fingerprint, True)  # True = private keys

# Read a public key file
with open('their_public_key.asc', 'r') as f:
    key_data = f.read()

# Import the key
import_result = gpg.import_keys(key_data)
print(f"Imported {import_result.count} key(s)")
print(f"Fingerprints: {import_result.fingerprints}")

# List all public keys
public_keys = gpg.list_keys()
for key in public_keys:
    print(f"Key: {key['keyid']} - {key['uids'][0]}")

# List private keys
private_keys = gpg.list_keys(True)
