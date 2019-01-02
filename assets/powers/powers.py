import matplotlib
import matplotlib.pyplot as plt
import sys

def S(m): return sum(ord(c) - ord('0') for c in str(m))

def data(N):
  xs = []
  ys = []
  k = 1
  while True:
    print(k)
    if k > 170 or len(str(N ** k)) > 5 * N: break
    s = S(N ** k)
    xs.append(k)
    ys.append(s)
    k += 1
  return (xs, ys)

if __name__ == '__main__':
  M = int(sys.argv[1])
  xs, ys = data(M)
  plt.rc('text', usetex=True)
  plt.axhline(y=M, color='green', label='N', linewidth=0.2)
  plt.xlabel('$k$')
  plt.ylabel('$S(N^k)$', rotation='horizontal')
  plt.title(r'The sum of digits of $N^k$, for $N = %s$' % M)
  plt.plot(xs, ys, marker='s', linestyle='None', label='$S(N^k)$', markersize=0.9, markeredgewidth=0, markerfacecolor='red', markerfacecoloralt='red', color='red', fillstyle='full')
  plt.legend(loc='lower right')
  plt.savefig("powers-%s.png" % M, dpi=600)
