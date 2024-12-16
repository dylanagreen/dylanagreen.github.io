```python
from pwn import *
import os
import math
from Crypto.Util.number import bytes_to_long, long_to_bytes

p = remote('54.85.45.101', 8010)

print(p.recvuntil(b"format:\n"))
print("sending")
p.sendline(b"flag") # Want to get how many bytes it is.

r = p.recvline()
ct = int(r.decode().strip().split(" ")[-1][2:], 16)
print(ct)

r = p.recvline()
n_bytes = int(r.decode().split(" ")[-1])
print(n_bytes)


print(p.recvuntil(b"format:\n"))
to_send = os.urandom(n_bytes).hex()
p.sendline(to_send.encode("utf-8"))

r = p.recvline()
print(r.decode().strip().split(" ")[-1][2:])
dc = int(r.decode().strip().split(" ")[-1][2:], 16)

dc_fault = 0
s = p.recvuntil(b"format:\n")

# We will proceed by sending the same string over and over until there is a fault
# We could also get unlucky and there's a fault in the first try so we must account for that
faulted_first = False
if b"Fault" in s:
    faulted_first = True
    print("Faulted first")

# 1/10 chance of faulting means in 20 tries we should for sure fault.
for i in range(20):
    p.sendline(to_send.encode("utf-8"))
    r = p.recvline()
    dc_fault = int(r.decode().strip().split(" ")[-1][2:], 16)

    s = p.recvuntil(b"format:\n")
    if (b"Fault" in s) or (not (b"Fault" in s) and faulted_first):
        break

N = 30392456691103520456566703629789883376981975074658985351907533566054217142999128759248328829870869523368987496991637114688552687369186479700671810414151842146871044878391976165906497019158806633675101
e = 65537

q = math.gcd(dc - dc_fault, N)
print(q)
p = N // q
print(p)
phi = (q - 1) * (p - 1)
d = pow(e, -1, phi)

pt = pow(ct, d, N)
print(q)
print(long_to_bytes(pt))

# flag{cr4ck1ng_RS4_w1th_f4ul7s}

```