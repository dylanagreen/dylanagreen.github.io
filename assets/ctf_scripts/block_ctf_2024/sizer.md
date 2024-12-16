```python

import time
from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

idcs = []
standard_alph = []
encrypt_alph = []

def is_same_type(c1, c2):
    if c1.isnumeric() and c2.isnumeric(): return True
    if c1.islower() and c2.islower(): return True
    if c1.isupper() and c2.isupper(): return True
    if c1 == c2: return True # handles the braces
    return False

# i = 37
# while i < 127:
#     p = remote('54.85.45.101', 8003)
#     to_send = chr(i)
#     p.sendline(to_send.encode("utf-8"))
#     try:
#         r = p.recv()
#     except EOFError: # try again if this was the case.
#         p.close()
#         continue
#     p.close()
#     i += 1

#     # Not a valid flag char.
#     if r.startswith(b"Invalid"):
#         continue
#     # print(i, to_send, r)

#     idcs.append(i - 1)
#     standard_alph.append(to_send)
#     encrypt_alph.append(r.decode())
#     time.sleep(0.05) # Give the server a little break as a treat.

# diffs = [int(encrypt_alph[i], 16) - idcs[i] for i in range(len(idcs))]
# print(standard_alph)
# print(diffs)

# for i in range(len(diffs)):
#     print(standard_alph[i], encrypt_alph[i], diffs[i])
# Above code determined the standard alphabet and its differences, although we didn't need it in the end.

# Remember that diffs is encrypt - ord(plain), plain = encrypt - diffs
standard_alph = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '}']
diffs = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -39, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -97, -61, -62]

double_dict = {}
# Unfortunately have to test ending on "}"
end_chars = ["0", "A", "a", "{", "}"]

diff = 0
# Don't need to go all the way to the end since two char strings will never start with } in the flag
for c1 in standard_alph[:-1]:
    for c2 in end_chars:
        p = remote('54.85.45.101', 8003)
        to_send = c1 + c2
        p.sendline(to_send.encode("utf-8"))
        try:
            r = p.recv()
        except EOFError: # try again if this was the case.
            p.close()
            continue
        p.close()

        # Not a valid flag char.
        if r.startswith(b"Invalid"):
            continue

        val = bytes_to_long(to_send.encode("utf-8"))
        received = int(r.decode(), 16)
        diff = received - val # encrypt - pt

        # Now generate the dict for everything with that starter char and end char combo
        # Since the diff is constant within end char types
        for c3 in standard_alph:
            if not is_same_type(c2, c3): continue
            to_send = c1 + c3
            val = bytes_to_long(to_send.encode("utf-8"))
            double_dict[hex(val + diff)[2:]] = to_send

        time.sleep(0.05) # Give the server a little break as a treat.

ct = "052c01be88c7f52cbdc3c084c7b1313828034370034dd13778342dff"
pt = ""

for i in range(len(ct) - 3, 0, -3):
    pt = double_dict[ct[i:(i + 3)]] + pt
print("f" + pt)

# flag{ImF1ll3dWithSte4kandCann0tD4nc3}
```