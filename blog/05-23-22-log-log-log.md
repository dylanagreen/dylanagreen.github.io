@def title = "May, 2022 - Log Log Log"
@def tags = ["ctf", "crypto"]

# angstromCTF 2022 Retrospective: log log log
\toc

This challenge was one of two angstromCTF challenges that I was working on
for most of the competition, althoug of the two it was the only one I was able to
solve in time. The other was Strike-Slip Fault. Anyway, enough about my failures,
let's talk sucesses in log log log.

## Challenge Description

For this challenge we're given the following introductory text:

> What rolls down stairs, alone or in pairs?

As well as two files: *logloglog.sage* and *output.txt*. The contents of *output.txt* are

```
0xb4ec8caf1c16a20c421f4f78f3c10be621bc3f9b2401b1ecd6a6b536c9df70bdbf024d4d4b236cbfcb202b702c511aded6141d98202524709a75a13e02f17f2143cd01f2867ca1c4b9744a59d9e7acd0280deb5c256250fb849d96e1e294ad3cf787a08c782ec52594ef5fcf133cd15488521bfaedf485f37990f5bd95d5796b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
3
0xaf99914e5fb222c655367eeae3965f67d8c8b3a0b3c76c56983dd40d5ec45f5bcde78f7a817dce9e49bdbb361e96177f95e5de65a4aa9fd7eafec1142ff2a58cab5a755b23da8aede2d5f77a60eff7fb26aec32a9b6adec4fe4d5e70204897947eb441cc883e4f83141a531026e8a1eb76ee4bff40a8596106306fdd8ffec9d03a9a54eb3905645b12500daeabdb4e44adcfcecc5532348c47c41e9a27b65e71f8bc7cbdabf25cd0f11836696f8137cd98088bd244c56cdc2917efbd1ac9b6664f0518c5e612d4acdb81265652296e4471d894a0bd415b5af74b9b75d358b922f6b088bc5e81d914ae27737b0ef8b6ac2c9ad8998bd02c1ed90200ad6fff4a37
880
```

Right off the bat you need to do a little investigation to find out exactly what
the heck these numbers are. Correspondingly you should find out that the numbers
printed are

```
hex(p)
g
hex(a)
flagbits
```
where flagbits is the number of bits in the flag. $p$ is the prime number base
that we're working in such that $g^e = a$. So all we need to do is find $e$ to
recover the flag, easy right?

## Attempt 1
Obviously the first thing you do is google the challenge description
[for hints.](https://www.youtube.com/watch?v=-fQGPZTECYs) Unfortunately the only
thing you're going to find is a song that's going to be stuck in your head for
three days. Great.

Immediately I recognzied this as a discrete logarithm problem, since I had been
working on a Pohlig-Hellman algorithm at the end of picoCTF while trying to
solve NSA Backdoor (which I never successfully solved, although with an extra few
hours to debug I probably would have gotten there).

So I downloaded SageMath, wrote up a quick little script to try and solve it
in a subgroup of the group $p-1$ (since $p$ is a 2048 bit prime solving the
problem in that group would be nigh on impossible). Challenge solved.

Just kidding. Not sure what I did wrong but evidently this did not solve the log
for me. Maybe I was too impatient. My teammate responded by saying "well it's
obviously going to be harder than 'download SageMath and win'". Little did
we both know, but it actually was just
["download SageMath and win"](https://hackmd.io/@lamchcl/rJgPUtgI5#log-log-log).

What really happened was I forgot to raise $g$ and $a$ to the $q$ power before
finding the log, a necessary step when applying Pohlig-Hellman. Embarrasing,
but let's move on to what I *actually* did.

## Attempt 2
The previous section was somewhat facetious, so let me be serious again and explain
a little math that'll become relevant in a second. In the Pohlig-Hellman algorithm
you find the discrete log in subgroups of the main group and use the Chinese Remainder
Theorem to recombine them to find the log in the main group. However, in this problem,
the order of $GF(p)$ is $p-1 = q*2^{1024}$, where $q$ is a large prime. When you
apply Pohlig-Hellman you would find two discrete logs, one in the group of integers
modulo $q$ and one in the group of integers modulo $2^{1024}$. The former log is
almost as difficult to compute as the total log in $p$ so... what's the point?

Well, this is where the `flagbits` variable comes in. If you read `logloglog.sage`
you might realize that the flag is stored in the least significant bits of the
exponent $e$. Doing the discrete log in the group of integers modulo $2^{1024}$
will give you the 1024 least significant bits of the exponent $e$
(although proving that this is how modulo math works on binary numbers is
beyond the scope of this blog post, so just take it as an ansatz), and since
the number of flag bits (880) is less than 1024, you only need to find the log
modulo $2^{1024}$ to find the flag.

I didn't actually realize this until after the challenge was over, but I've also realized
that my method was just an efficient implementation of this lower order discrete log.
Essentially I just implemented a known algorithm for efficiently computing
discrete logs for integers where $p = 2^n + 1$ for some $n$.

With that primer out of the way let's look at how I worked this out. We can start
by using Fermat's Little Theorem:

$$ a^{p-1} = 1 \text{(mod p)} $$

for any $a$ coprime to $p$.

For a brief moment here, ignore that we already know $p$ and assume that the only
thing we know about $p$ is that it's prime and that therefore $p-1$ must be even.
I'm now going to asser that knowing this fact, and this fact alone,
we can discover the very last bit of $p-1$. Let's arbitrarily declare $x = g^e$.
Since $g$ is a generator of the group $GF(p)$, we know that $x$ and $p$ are coprime
and we can apply Fermat's Little Theorem: [^1]

$$ x^{p-1} = 1 \text{(mod p)} $$

What if we instead, however, raise $x$ to the $(p-1)/2$ power?

$$ x^{(p-1)/2} = g^{e(p-1)/2} =  ? \text{(mod p)} \label{x_pow}$$

If we rewrite $e = b_{n-1} 2^{n-1} + b_{n-2} 2^{n-2} + ... + b_{1} 2^1 + b_0 = e^\prime + b_0$
where $b_i$ is the $i$th bit of $e$ then we can rewrite Equation \eqref{x_pow} as

$$ g^{(e^\prime + b_0)(p-1)/2} =g^{e^\prime(p-1)/2}g^{b_0(p-1)/2} = g^{b_0(p-1) / 2} \text{(mod p)} $$

where I used Fermat's Little Theorem and the fact that $e^\prime$ must always be
even to simplify. Evidently, then:

$$ g^{b_0(p-1) / 2} = \begin{cases} 1 &\text{ if } b_0 = 0 \text{(mod p)} \\  p-1 &\text{ if } b_0 = 1 \text{(mod p)} \end{cases} $$

The $b_0=1$ case may not be obvious. Here's two-lines that prove that it's true, but
in reality it's not important since we only care that it doesn't equal 1:

$$ g^{(p-1) / 2} = 1^{1/2} \text{(mod p)} $$
$$ (p-1)^2 \text{(mod p)} = p^2 - 2p + 1 \text{(mod p)} = 1 \text{(mod p)} $$

So if we perform the exponentiation in Equation \eqref{x_pow} we can check the result
and recover the value of bit 0!

One bit isn't very useful on its own but... can we extend the method to find the
value in bit 1 using this knowledge?

Turns out we can! If $p-1$ is divisible by 4 in addition to 2, that is. I'll walk
through this step as well, and then present the case for an arbitrary $i$th bit
such that $i < 1024$ (in this problem).

We'll define a new variable $e_1 = e - b_0 = b_{n-1} 2^{n-1} + b_{n-2} 2^{n-2} + ... + b_{1} 2^1$.
Notice that $e_1$ is always even. Since $e_1$ is always even, when you raise $g^{e_1}$ to
the $(p-1)/2$ power, you'll always get 1:

$$ g^{e_1(p-1)/2} = g^{(e_1/2)^{p-1}} = 1 \text{(mod p)} $$

But remember how we recovered bit 0? By raising $g$ to a power such that we receive
$b_0/2$ in the exponent, which will then tell us whether it's equal to 0 or 1. $b_1$
is already multiplied by $2$, so you might guess that we would need to raise $g^{e_1}$
to the $(p-1)/4$ power to recover bit 1, and you would be correct:

$$ g^{(e_1^\prime + b_1 2^1)(p-1)/4} =g^{e_1^\prime(p-1)/4}g^{b_1(p-1)/2} = g^{b_1(p-1) / 2} \text{(mod p)} $$

$$ g^{b_1(p-1) / 2} = \begin{cases} 1 &\text{ if } b_1 = 0 \text{(mod p)} \\  p-1 &\text{ if } b_1 = 1 \text{(mod p)} \end{cases} \label{b_1}$$

where we defiend $e_1^\prime$ similarly as before:
$e_1 = b_{n-1} 2^{n-1} + b_{n-2} 2^{n-2} + ... + b_{1} 2^1 = e_1^\prime + b_{1} 2^1$

The final step to turn this into a repeatable algorithm is to recover $g^{e_1}$ from
$g^e$. Remember that we've already found the value of $b_0$. Therefore using the definition
of $e_1$ we can find:

$$ g^{e_1} = g^eg^{-b_0} \text{(mod p)} $$

Using Equation \eqref{b_1} we can get the value of bit 1! Note that this only works
if $(p-1)$ is divisible by 4. If it is not, then $(p-1)/4$ is not defined in GF(p),
and therefore cannot be used in the exponent of $g^e$.[^2]

Our very last step is to generalize this to the $i$th bit of $e$ for $i < 1024$.
This is left as an exercise for the reader, but I quote the result here:

$$ g^{e_i(p-1) / 2^i} = \begin{cases} 1 &\text{ if } b_i = 0 \text{(mod p)} \\  p-1 &\text{ if } b_i = 1 \text{(mod p)} \end{cases} \label{gen_1}$$

$$ e_i = e - \sum_{j=0}^i b_j 2^{j} \label{gen_2}$$

[^1]: If you know what this means you probably nodded your head. If you don't, just take it as true or look up the details elsewhere since explaining this would expand the scope of this writeup 10 fold.
[^2]: If this confuses you, remember that GF(p) is defined as integers modulo $p$, and if $(p-1)$ is not divisible by 4 then $(p-1)/4$ is not an integer.
## Code

I wrote my original implementation of Equations \eqref{gen_1} and \eqref{gen_2} in python, which worked
adequately. After confirming the method worked I actually went back and rewrote it
in Julia, which runs in ~1-2s compared to the nearly 10 of the python implentation.

\input{julia}{/_assets/scripts/log_solve.jl}

And when you run the code the flag pops right out, how easy is that?

\output{/_assets/scripts/log_solve.jl}
