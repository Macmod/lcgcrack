Linear Congruential Generator cracker for ALEXCTF 2017's Crypto5 challenge.
This approach differs from the others in that it does not attempt to find the period of the LCG (which depending on the scenario can be quite a difficult task), but instead solves the congruence system to get the coefficients.

The challenge is to crack a remote PRNG that leaks its next values.
Writeup can be found at `@todo`.

The `lcg` folder contains a reconstruction of the specific LCG used for the challenge.

This LCG is the one used in `lcgcrack.py`, although for the challenge source code was not provided.
