import functools
import math
import gmpy

def _crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def _crack_unknown_multiplier(states, modulus):
    a = (states[2] - states[1])
    inv = int(gmpy.invert(states[1]-states[0] % modulus, modulus))
    multiplier = (a * inv) % modulus
    return _crack_unknown_increment(states, modulus, multiplier)

def _crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:],diffs[2:])]
    modulus = abs(functools.reduce(lambda x,y: math.gcd(x,y),zeroes))
    return _crack_unknown_multiplier(states, modulus)

def crack(seq):
    return _crack_unknown_modulus(seq)
