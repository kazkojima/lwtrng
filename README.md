[> Intro
--------
LwTrng provides a small footprint TRNG core.

Only a simple ECP5 version of the random bit generator PHY is given ATM, though it can be easily ported to the other FPGAs or more sophisticated PHY can be constructed on them.

The current version of PHY is based on the phase jitter of 16 ring oscillators. The basic implementation is same with [David R. Piegdon's ringoscillator](https://github.com/dpiegdon/ringoscillator). A 32-bit crc circuit gives 32-bit random numbers from that PHY output. This random word can be read by CPU as CSR.

PHY has a CSR-ed disable input which stops ring oscillators so to reduce the power consumption. When it's asserted, the generated numbers are the outputs of pure 32-bit LFSR, i.e. a psuedo random numbers. ECP5 version feedbacks the resulted number to ring ocillators so to perturb jitters.

For the cryptographic applications, it is highly desirable to add some conditional component to the raw output of this TRNG. The conditional component isn't included in the current design to save footprint. Some hardware/software SHA would be used as a good conditional component.

[> Features
-----------
**TODO**

[> Getting started
------------------
**TODO**
```
./setup.py install
```

[> Tests
--------
**TODO**

