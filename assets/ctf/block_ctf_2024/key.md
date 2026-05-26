```python
import json

from pwn import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

X25519_KEY_SIZE = 32
# null bytes * anything = null bytes :)
# hence secret will be null bytes
client_pub = bytes(X25519_KEY_SIZE)

p = remote('54.85.45.101', 8001)

to_send = {"client_pub": client_pub.hex()}
p.sendline(json.dumps(to_send).encode())

r = p.recv().decode("utf-8")
d = json.loads(r)
print(d)

iv = bytes.fromhex(d["iv"])
ct = bytes.fromhex(d["ct"])

cipher = Cipher(algorithms.AES(client_pub), modes.CTR(iv))
decryptor = cipher.decryptor()
pt = decryptor.update(ct) + decryptor.finalize()

print(pt)

# flag{0000_wh0_knew_pub_keys_c0uld_be_bad_0000}
```