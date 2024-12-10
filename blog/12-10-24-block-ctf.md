@def title = "October, 2024 - One For Your, One For Me"
@def tags = ["ctf", "crypto"]

# BlockCTF 2024 Retrospective
\toc

I still participate in CTFs about once monthly, keeps my math skills sharp considering
the only category I can ever contribute to reliably is crypto (since I'm the only
player on the team who likes math, apparently). Recently we
participated in [Block CTF](https://2024.blockctf.com/) and I cleared all
three crypto challenges within the first ~14 hours. Figured I would write them
up for posterity.

I'd like to get back into doing writeups more frequently, because its
proven that explaining a concept helps ensure that you actually understand it,
and I'd like to significantly improve my cryptography skills for the more difficult
CTFs.

## Sizer Cipher (100 pts)

> I made my own encryption scheme- check it out!
> 052c01be88c7f52cbdc3c084c7b1313828034370034dd13778342dff

This is a sourceless crypto, which means it'll be slightly guessy at least
until we can figure out what the cipher actually does. It's also reasonable
to assume that the provided hex string is the encrypted version of the flag.

A lot of this challenge is guessing and checking until you figure out
to some small degree what the encryption is doing. After a while you can realize
that the server encrypts in two character blocks, left padding with null bytes
to ensure that the length is a multiple of two.

We don't necessarily know
the length of the flag, but it's fine since we can just decrypt right to left
and either it'll be an even length or it'll be an odd length and we know the
first character anyway since all flags are formatted as `flag{}`.

Each two char block is encrypted by adding a constant value to the block
depending on the ending char type (digit, uppercase
letter, lowercase letter, or {}) and the value of the starter char.[^1]


The server also has a silent rejection of certain characters. We can determine the
set of "allowed" characters by querying every single byte value (there's only
256 anyway) to determine that there are 64 allowed chars:

> 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}

To decrypt we can build a lookup table
that matches each possible two char combination to its encrypted value and then
matching the encryptions to the encrypted string. Doing this requires
$63 \times 5$ queries to the server of various starting char (63) + end char type (5) combinations.
We only need 63 starting chars since no group will ever start with `}`.

\textinput{/_assets/ctf_scripts/block_ctf_2024/sizer.md}


[^1]: After the conclusion of the CTF I realized that the encryption was an addition and a multiplication combined, and we could have done this with a significantly fewer amount of queries.

## Where's My Key? (150 pts)

>The flag server is providing encrypted flags. It looks like there might be a bug in the code and I can't figure out how to decrypt it.

I did this challenge last, because on first glance it looked quite tricky. In reality
it was actually very straightforward due to the simple fact that the
server doesn't do any sort of input sanitization.

The server implements a very straightforward [Elliptic Curve Diffie-Hellman (ECDH)](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman)
key exchange scheme, using Curve25519.[^2] ECDH is almost identical to
normal Diffie-Helman, substituting math over an elliptic curve rather than
an integer ring. Briefly for ECDH, suppose
we have two cryptologists Andy and Becky. Andy and Becky each generate their
private key, $a$ and $b$, which in this case are just integers. In order to safely
share their keys, and calculate a shared secret, Andy shares $(a * G)$ to
Becky, while Becky shares $(b * G)$ to Andy. The two can then each (independently)
calculate the shared secret $(a * b * G)$. $G$ here, in ECDH, refers to the
generator point used for the chosen elliptic curve.

The security of ECDH is linked to the difficulty of calculating
the "elliptic curve discrete logarithm problem." That is to say,
 given $(a * G)$ and $G$ it is difficult to impossible to calculate the value of $a$.
Thus an interceptor who receives $(a * G)$ and $(b * G)$ cannot calculate the
shared secret $(a * b * G)$ from these values.

In this challenge the server accepts your public key $(a * G)$, then calculates
its own private and public keys as well as the shared secret. In "standard"
ECDH the server is then supposed to share its public key, $(b * G)$ with you,
but due to a (intentional) bug in the code it does not, so you have no way
of knowing the shared secret... or do you? More on this in a second.

The server then uses the shared secret as the key in an AES encryption in
CTR (counter) mode with a random initialization vector (IV). The server then
gives you the encrypted flag and the IV, with the assumption that you know
the key. The exact mode for the AES encryption here is only relevant as far as
we need to know what it is for decryption, given the key.

The problem is then basically solved if you know the shared secret. One
approach is to try and reconstruct the shared secret, but the server uses a random
private key every time. An alternative method is if you can somehow *force* the
server to have a specific shared secret then you also win. As foreshadowed
before the server does not do any input sanitization or validation. Note, then,
if you generate your ECDH private key as a string of null bytes, such that $a = 0$
then the shared secret $a * b * G = 0$. Knowing this and the returned IV and ciphertext
you can decrypt the flag.

\textinput{/_assets/ctf_scripts/block_ctf_2024/key.md}


[^2]: This key exchange/curve combination is typically referred to as x25519.

## Glitch in the Crypt: Exploiting Faulty RSA Decryption (200 pts)
> A high-security server, SecureVault Inc., uses RSA encryption to protect sensitive data. The server utilizes a 1024-bit RSA key and employs the CRT optimization during decryption to improve performance.
>Due to a hardware fault, the server occasionally introduces errors during the decryption process. Specifically, the fault affects the computation of m_p = c^{d_p} mod p during the CRT step, causing m_p to be incorrect, while m_q = c^{d_q} mod q remains correct.
>As an experienced cryptanalyst, you have managed to obtain access to the server's decryption service. Your goal is to exploit the faulty decryption results to recover the prime factors p and q of the RSA modulus n, effectively breaking the encryption scheme and recovering the private key.

The challenge description above essentially outlines exactly how to solve this
challenge. The server is a standard RSA decryption oracle that has a 10% chance
to introduce a fault into the [CRT reconstruction](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Using_the_Chinese_remainder_algorithm)
 when decrypting RSA.

Section 2.1 of the paper [Fault Attacks for CRT Based RSA: New Attacks, New Results, and New Countermeasures](https://dl.ifip.org/db/conf/wistp/wistp2007/KimQ07.pdf)
outlines the solution to the challenge although with a few mathematical steps skipped
that I will outline below.

To decrypt a message in base RSA we calculate

$$ m = c^d ~\text{mod}~ n $$.

The CRT allows us to compute the value mod $n$ by instead computing the
decryptions in the subgroups mod $p$ and mod $q$. The math to do this
is slightly more involved, first computing the decryption exponents in
the subgroups:

$$ d_p = d ~\text{mod}~ (p-1) $$
$$ d_q = d ~\text{mod}~ (q-1) $$

As well as the inverse of q in the p group:
$$ q_{inv} = q^{-1}  ~\text{mod}~ p$$

Then using the CRT, using notation that matches both Wikipedia and the challenge
script:
$$ m_1 = c^{d_p} ~\text{mod}~ p $$
$$ m_2 = c^{d_q} ~\text{mod}~ q $$
$$ h = q_{inv}(m_1 - m_2) ~\text{mod}~ p$$
$$ m = m_2 + hq $$

This is pretty standard CRT, given the modulus of the message in $p$ and $q$ we
thus compute the modulus of the message in mod $n = pq$ in the last line. For
small messages, this is actually slower than just directly calculating the decryption
in mod $n$, but for large messages this is faster or more memory efficient.

A fault attack necessitates a mistake in calculating either $m_1$ or $m_2$, such
that we do not correctly calculate the decryption in that subgroup. In this
specific challenge the server simulates a fault in calculating $m_1$. A fault
in $m_2$, in this notation, would actually be harder to detect and crack, although
with respect to the first point
the server alerts you that a fault occurred (it would have been perhaps more interesting
if it had not).

What happens when $m_1$ is calculated incorrectly? Consider taking the difference
of two different decryptions, $A$ and $B$ of the same original ciphertext:

$$ m_A - m_B = m_{2,A} + h_A q - m_{2, B} - h_B q  = 0?$$

If both decryptions are the same, with no faults, then this value is obviously
equal to zero. However, consider that there is a fault in $m_1$ (but not $m_2$):

$$ m_A - m_B = h_A q - h_B q  = (h_A - h_B) q $$

This value is proportional to $q$! It should be clear then that $GCD(m_A - m_B, N) = q,$[^3]
with $p$ following from $p = N / q$. Knowing $p$ and $q$ we can easily reconstruct
$d$ and perform the decryption ourself!

\textinput{/_assets/ctf_scripts/block_ctf_2024/faulty.md}

[^3]: Assuming that $m_A > m_B$, simply swap the two if it is not.


## Conclusion

We ended up placing 30th, and for a brief moment I was the MVP with my
crypto clear although that was deposed in the last few hours of the challenge.
Alas, perhaps next time.



