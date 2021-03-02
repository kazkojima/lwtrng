[> Intro
--------
LwTrng provides a small footprint TRNG core. The current implementation generates ~10Mbits/sec random data with 60MHz sytem clock.

Only a simple ECP5 version of the random bit generator PHY is given ATM, though it can be easily ported to the other FPGAs or more sophisticated PHY can be constructed on them.

The current version of PHY is based on the phase jitter of 16 ring oscillators. The basic implementation is same with [David R. Piegdon's ringoscillator](https://github.com/dpiegdon/ringoscillator).

The PHY output is post-processed with the 18-stage duplexing([1],[2]) module which is a conditional component. Each stage does duplexing with the Keccak-f200([1]) function. A 32-bit random number is made by collecting a few bits from these stage's outputs. This random words are fifo'ed and can be read by CPU as CSR.

![Diagram of LwTrng](https://github.com/kazkojima/lwtrng/blob/main/doc/trng.png)

Excluding the FIFO part, it consumes ~500 slices on ECP5.

[> Features
-----------
**TODO**

[> Getting started
------------------
**TODO**

The post process module is writen with nMigen and its verilog output is needed to use it from LiteX ATM. The command below will generate the verilog file. 
```
pushd lwtrng/pp/verilog
make
popd
```
To register LwTrng module to your python environment, run setup.py.
```
./setup.py develope --user
```


[> Tests
--------
**TODO**

The resulted stream of random numbers are tested with dieharder and TestU01 with no significant problem.

```
========= Summary results of Alphabit =========

 Version:          TestU01 1.2.3
 File:             rand32-64G.bin
 Number of bits:   68654879232
 Number of statistics:  17
 Total CPU time:   00:29:34.16

 All tests were passed
```
```
========= Summary results of Rabbit =========

 Version:          TestU01 1.2.3
 File:             rand32-64G.bin
 Number of bits:   68654879232
 Number of statistics:  40
 Total CPU time:   01:15:28.02

 All tests were passed

```

[> Links
-------------

[1] Team Keccak,
[The Keccak-p permutations](https://keccak.team/keccakp.html)

[2] Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche,
[Duplexing the sponge: single-pass authenticated encryption and other applications](https://www.researchgate.net/publication/221274795_Duplexing_the_Sponge_Single-Pass_Authenticated_Encryption_and_Other_Applications)
