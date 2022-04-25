@def title = "April 24, 2022 - Sum O' Primes"

# picoCTF 2022 Retrospective: Sum O' Primes
\toc

In this write up I'll look at [Sum O' Primes](https://play.picoctf.org/practice/challenge/310?category=2&originalEvent=70&page=2), a considerably easier (in my opinion)
challenge than [Very Smooth](/blog/04-23-22-very-smooth). This challenge requires only rudimentary algebra
and the ability to take integer square roots (which thankfully we have a package for).

## Challenge Description

For this challenge we're given the following introductory text:

> We have so much faith in RSA we give you not just the product of the primes, but their sum as well!

As well as two files: *gen.py* and *output.txt*. The contents of *output.txt* are

```
x = 1c5d833516f25a832a331f349d2931d1577b3171d689da0391608dea7bbd9cda413d836db2f5c79da05755225c41af1cffbfaf1777b64abb521ac63e09d6101fe16fa7b98a647b94eccef0601681c34d4aa0ac9ded573f14460dc5dc5337d24bdf1f69325689346795adb0f9159cb2779463dce6e084adf861b61bd76bb160132
n = c6c7c7879953a678d8e6d2ab85248f19b3f7c4b1e0c4c3f5bc1b63946abcac0cc19523386a08bbb5bd09321b9023df091f162dd0e9b100da1b5d15f78523ea6d7c6d7c7cd8b5c287fcd5d91defc53a32885c0a6f16f3b13221bbd4b5254bb9dbfe79244d343841485ad38fb139abfa3c3bd50e4787b1e882d21ada914989c1497774bdaa046ad2366028bd31f9277c39f58fe6fc78c247c4159b8879eaa7e15301ce937a7491e7727e5ae6e7852df6f9fd3367e5bb178c7013805a16ee68f6cdf8f5f72b2fbc159c38244082b1c47f5814a494ac7b310c37fe68a85e4448885d0de8f93d21106121ff74c0c6452ff697b2d2660483af13ce82ebdc0293b24dad
c = 101ef1af3fd07a28858d5102e2448f29fd995f63df13b6e6a98d077e2330722af3374cd30652943fd1de006118024a4c86a23eae960b872e8d6c5735d73a05c40d039b6779b78f0fb90daf5011de05636b35a47416cb91712df3ca62f32bd2799b24d3b267a6140f98b07dfbb9e333bc71170776ce794f34674c232544df18e719698614958bbda4e371e58e22df63c2284f0f748af6ea0465f520ed8a70ba8d12307900216645b820c29a6297c1754a703a7caa1747ecf4d4bee49163366686ff15961db87f08007c302bde64c3e4dc165604a856b036c891ef4b0dd1fd9aec79f2a7d2d017c880c1a523d1d46868a99ee2b0046cacebe65da9a3ce3b7c9683

```

We are provided three numbers here, in contrast to Very Smooth. By inspecting
*gen.py* we can recover that $x = p + q$ and $n = pq$.

## Method
Looking at *gen.py* it should become evident that this is an RSA problem, once again. We are
given the encoded message, as well as the product and sum of the two primes used to produce
the encoding base $n$ (and therefore also the order of the group, i.e. the modulus).
In order to solve the problem we will need to recover the the base by finding the two
primes used to construct $n$.

The hint

> I love squares :)

actually didn't really help me this time. Not sure what the hint was supposed to try
and lead you towards, since I did this problem using high school level algebra.

We are given two equations with two unknowns to solve for:

$$ x = p + q $$
$$ n = pq $$

Substitute the second into the first and solve for $q$:

$$ x = n/q + q $$
$$ q^2 - xq + n = 0 $$
$$ q = \frac{x \pm \sqrt{x^2 - 4n}}{2} \label{sqrt}$$

I won't prove it here, but one of the two factors will correspond to the "plus"
and one to the "minus" in the equation above. You can prove it for yourself by
solving for $p$ instead of $q$ and recovering the same equation.

## Code

```python
a = x**2 - 4 * n

from gmpy2 import *
p = x + int(gmpy2.isqrt(a))
p = p // 2
q = n // p

e = 65537

m = lcm(p - 1, q - 1)
d = pow(e, -1, m)

mess = pow(c, d, n)
decrypt = hex(mess)
binascii.unhexlify(decrypt[2:])


```
You might recognize the last few lines as being the same as in Very Smooth, which
is intentional at least on the part of the picoCTF organizers. Most of the challenge
in this one was simply finding a way to take an integer square root in Python.
Since $p$ and $q$ are both known to be integers, the square root in Equation
\eqref{sqrt} must necessarily
produce an integer as well. However, raw python tries to take square roots on floats,
and the number inside the root is much too large and will overflow. You could do
something tricky, like I will in the upcoming Sequences post, but since gmpy can
take integer square roots its easier to just use that.

> b'picoCTF{...}'
Since the challenge is still solvable, I have redacted the actual flag, although
this blog post all but solves it for you.

All in all this one wasn't too bad, and I solved it much faster than Very Smooth.