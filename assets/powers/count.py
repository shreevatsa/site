def isprime(n):
    if n < 2: return False
    d = 2
    while d * d <= n:
        if n % d == 0: return False
        d += 1
    return True
# print([n for n in range(100) if isprime(n)])

lines = open('output.txt').readlines()
N = 1
xs = []
ys = [] # Primes
zs = [] # "good" N
ws = [] # Their ratio
num_primes = 0
num_good = 0
for i in range(len(lines) - 1):
  if lines[i].startswith(' '): continue
  N += 1
  num_primes += (1 if isprime(N) else 0)
  num_good += (1 if lines[i + 1].startswith(' ') else 0)
  xs.append(N)
  ys.append(num_primes)
  zs.append(num_good)
  ws.append(None if (num_primes == 0 or N < 10) else num_good * 1.0 / num_primes)

# print(xs)
# print(ys)
# print(zs)
# print(ws)
print('Now plotting')

import matplotlib
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)

# fig, ax1 = plt.subplots()
ax1 = plt
ax1.title("The growth of primes and of ``good'' N")
ax1.xlabel('$N$')
ax1.plot(xs, ys, label="primes")
ax1.plot(xs, zs, label="good N")
ax1.legend(loc='lower right')
# plt.plot(xs, ys, marker='s', linestyle='None', label='$S(N^k)$', markersize=0.9, markeredgewidth=0, markerfacecolor='red', markerfacecoloralt='red', color='red', fillstyle='full')
print('Saving figure')

# ax2 = ax1.twinx()
# ax2.plot(xs, ws, label="ratio")
# ax2.legend(loc='upper left')

plt.savefig("compare.png", dpi=600)

      
