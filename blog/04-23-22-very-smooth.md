@def title = "April 23, 2022 - Very Smooth"

# picoCTF 2022 Retrospective: Very Smooth
\toc

This is going to be the first in a series of write ups detailing some of the
challenges I solved for picoCTF 2022. I'll detail some of the math and algorithms
necessary to solve the challenges, most of which are cryptography related (since
of the four categories that's the one I'm most well versed in).

In this write up we look at [**Very Smooth**](https://play.picoctf.org/practice/challenge/315?category=2&originalEvent=70&page=1).

## Challenge Description

For this challenge we're given the following introductory text:

> Forget safe primes... Here, we like to live life dangerously... >:)

As well as two files: *gen.py* and *output.txt*. The contents of *output.txt* are

```
n = c5261293c8f9c420bc5291ac0c14e103944b6621bb2595089f1641d85c4dae589f101e0962fe2b25fcf4186fb259cbd88154b75f327d990a76351a03ac0185af4e1a127b708348db59cd4625b40d4e161d17b8ead6944148e9582985bbc6a7eaf9916cb138706ce293232378ebd8f95c3f4db6c8a77a597974848d695d774efae5bd3b32c64c72bcf19d3b181c2046e194212696ec41f0671314f506c27a2ecfd48313e371b0ae731026d6951f6e39dc6592ebd1e60b845253f8cd6b0497f0139e8a16d9e5c446e4a33811f3e8a918c6cd917ca83408b323ce299d1ea9f7e7e1408e724679725688c92ca96b84b0c94ce717a54c470d035764bc0b92f404f1f5
c = 1f511af6dd19a480eb16415a54c122d7485de4d933e0aeee6e9b5598a8e338c2b29583aee80c241116bc949980e1310649216c4afa97c212fb3eba87d2b3a428c4cc145136eff7b902c508cb871dcd326332d75b6176a5a551840ba3c76cf4ad6e3fdbba0d031159ef60b59a1c6f4d87d90623e5fe140b9f56a2ebc4c87ee7b708f188742732ff2c09b175f4703960f2c29abccf428b3326d0bd3d737343e699a788398e1a623a8bd13828ef5483c82e19f31dca2a7effe5b1f8dc8a81a5ce873a082016b1f510f712ae2fa58ecdd49ab3a489c8a86e2bb088a85262d791af313b0383a56f14ddbb85cb89fb31f863923377771d3e73788560c9ced7b188ba97

```

## Method
Looking at *gen.py* it should become evident that this is an RSA problem. We are
given the encoded message, as well as the product of the two primes used to produce
the encoding base $n$ (and therefore also the order of the group, i.e. the modulus).
In order to solve the problem we will need to recover the the base by finding the two
primes used to construct $n$.

The hint

> Don't look at me... Go ask Mr. Pollard if you need a hint!

and the title of the challenge (Very Smooth) should key you in to the fact that
for this RSA problem, the primes $p$ and $q$ are smooth, and therefore $n$ is theoretically
easy to factor given the right algorithm.

The task then is easy. Factor $n$ to get $p$ and $q$, at which point we can reproduce
code directly from **gen.py** to decode the flag.

For this challenge it seems right to use [**Pollard's p-1 algorithm**](https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm) to factor $n$. I've linked wikipedia but will provide
a brief overview of the algorithm here anyway.

## Pollard's p-1 Algorithm

This section on the algorithm will not be mathematically rigorous, the point here
is only for you to understand the *principle* behind the algorithm, in broad enough
strokes to be satisfying.

Pollar's algorithm is based on Fermat's little theorem, which says

$$ a^{K * (p-1)} \equiv 1 \text{(mod p)} , \label{little}$$

where $a$ is an integer *coprime* to $p$, $K$ is a random integer, and $p$ is a prime.
Coprime means that $a$ and $p$ are do not share any common factors except 1. You
can derive this formula pretty easily if you start wih

$$ a^{p} \equiv a \text{(mod p)} .$$

Try it for yourself!

Let's take a brief aside into modulo arithmetic for a moment. For an arbitrary
integer $n = pq$ where $p$ and $q$ are prime and an arbitrary integer $K_1$,
all you need to know here is that

$$ K_1 p \equiv 0 \text{(mod p)} ,$$

from which it follows that if

$$ x \equiv 1 \text{(mod p)} \label{x-1}$$

then

$$ x - 1 \equiv K_2 p . \label{xequiv}$$
Be sure to note that Equation \eqref{xequiv} is not in modulo arithmetic, and $K_2$
is an arbitrary integer.

We now have all the pieces we need to undestand *what* exactly Pollard's p-1 algorithm
is trying to do. Assume we're factoring $n = pq$, where $p$ and $q$ are two "large" primes.[^1]
The algorithm works specifically to find factors such that $p-1$ is powersmooth. [^2]
We search through the space to find a value $x$ such that Equation \eqref{x-1} is true.
From there we can find the greatest common divisor between $x-1$ and $n$ which returns
to us $p$. You can check for yourself that the greatest common divisor between
$n$ and $x-1$, given that both $n$ and $x-1$ are multiples of $p$ must be $p$, if
$p$ is a large prime (the largest prime factor $x-1$, at least) and $x-1 < n$. Importantly
the value of $K_2$ (in this syntax) is completely irrelevant.

The key to Pollard's p-1 algorithm is the method by which it searches this space using Equation \eqref{little}.
If you can make the exponent a large enough number with enough prime factors, you should
(hopefully) be able to find $p$. Wikipedia outlines an algorithm, but for this challenge
I found [a slightly modified version](https://www.untruth.org/~josh/math/pollard-p-1.pdf)
to run quicker and more successfully.

## Code

In pseudocode, to factor $n$:
```
a <- 2
j <- 2
B <- 1e9 (the maximum smoothness bound)

while j <= B:
  a <- a^j mod n
  g <- gcd(a-1, n)
  if 1 < g < n:
    return g
  j <- j + 1
return fail
```

and the resultant python code I used to solve the problem:

```python
a = 2
j = 2
B = 1e9
while j <= B:
    a = pow(a, j, n)
    g = gcd(a - 1, n)

    if 1 < g < m:
        break

    j += 1

print(g)
```
Once you have $g$ you have $p$, and therefore can find $q$:

```python
p = g
q = n // p
```

Once you have $p$ and $1 < g < n$ you can recover the flag:[^3]

```python
import binascii

e = 0x10001

m = lcm(p - 1, q - 1)
d = pow(e, -1, m)

mess = pow(c, d, n)
decrypt = hex(mess)
print(binascii.unhexlify(decrypt[2:]))
```

> b'picoCTF{...}'
Since the challenge is still solvable, I have redacted the actual flag, although
the principles in this blog post can help you solve it.

Quite a fun little challenge!

[^1]: In fact there is no necessity that $p$ nor $q$ be large, this algorithm works for small primes too.
[^2]: I won't explain what this means here, you can either take it as an ansatz or check [wikipedia](https://en.wikipedia.org/wiki/Smooth_number#Powersmooth_numbers) for a more detailed explanation.
[^3]: This is a simple reversal of RSA encoding, where the exponent $e$ is pulled from *gen.py*. Read up on RSA if this doesn't make sense.