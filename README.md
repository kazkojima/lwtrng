[> Intro
--------
LwTrng provides a small footprint TRNG core.

Only a simple ECP5 version of the random bit generator PHY is given ATM, though it can be easily ported to the other FPGAs or more sophisticated PHY can be constructed on them.

The current version of PHY is based on the phase jitter of 16 ring oscillators. The basic implementation is same with [David R. Piegdon's ringoscillator](https://github.com/dpiegdon/ringoscillator).

The PHY output is post-processed with the 18-stage duplexing module which is a conditional component. Each stage does duplexing with the Keccak-f200 function. A 32-bit random number is made by collecting a few bits from these stage's outputs. This random word can be read by CPU as CSR.

![Diagram of LwTrng](https://github.com/kazkojima/lwtrng/blob/duplexPP/doc/trng.png)

The resulted stream of random numbers are tested with dieharder and TestU01 with no significant problem.

[> Features
-----------
**TODO**

[> Getting started
------------------
**TODO**
The post process module is writen with nMigen and the verilog output is needed to use it from LiteX ATM. The command below will generate it. 
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

