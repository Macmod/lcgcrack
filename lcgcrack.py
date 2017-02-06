from pwn import process
import gmpy

# Linear Congruential Generator
def lcg(seed, a, c, m):
    last = seed
    while True:
        yield last
        last = (a * last + c) % m

def get_next(prng):
    prng.recv(1024)
    prng.sendline('2')
    return int(prng.recvline())

def send_next(prng, n):
    prng.sendline('1')
    prng.recv(1024)
    prng.sendline(str(n))
    print(prng.recv(1024))

# Remote PRNG
# prng = remote('195.154.53.62', 7412)
prng = process('lcg/lcg')

# Sequence from remote PRNG
seq = [get_next(prng) for k in range(6)]
print('Got this sequence to analyze: ')
print(seq)

# Equation from 3 sequence values:
# 842389455, 3301052331, 1833279318

# 3301052331 = a*842389455 + c (mod m)
# 1833279318 = a*3301052331 + c (mod m)
# 3301052331 - 1833279318 = a * (842389455 - 3301052331) (mod m)

# a * -2458662876 = 1467773013 (mod m)
# This equation, solved for a, can be expressed as:
def get_a(m, seq):
    k = (seq[0] - seq[1]) % m
    inv = int(gmpy.invert(k, m))

    return (inv * (seq[1] - seq[2])) % m

# Observed maximum value after leaking a bunch of numbers (modulus must be close!)
max_seen = 4294915818

# Amount of numbers to test after the observed maximum
n_tests = 1000000

# Test a bunch of modulus
for n in range(max_seen, max_seen+n_tests):
    a = get_a(n, seq)
    if a != 0: # If an a exists
        # Figure out the c for this a
        c = (seq[1] - seq[0]*a) % n

        # Create an LCG with initial value = seq[0]
        # And test whether it produces the same values
        candidate_lcg = lcg(seq[0], a, c, n)
        flag = True
        for i in seq:
            if next(candidate_lcg) != i:
                flag = False

        # If so, show values for N, A and C
        # Then generate ten next values and send
        if flag == True:
            print '[M,A,C]', [n, a, c]
            for k in range(10):
                num = next(candidate_lcg)
                print '[SEND]', num
                send_next(prng, num)

            print(prng.recv(1024))
