isprime = {0: False, 1: False, 2: True, 3: True, 4: False, 5: True}
def primes():
    n = 1
    while True:
        n += 1
        if n in isprime:
            if isprime[n]: yield n
            continue # Whether or not n is prime
        for p in primes():
            if p * p > n: break
            if n % p == 0:
                isprime[n] = False
                break
        if n in isprime: # i.e. False
            continue
        else: # absent i.e. n is prime
            isprime[n] = True
            yield n

def is_prime(n):
    if n in isprime: return isprime[n]
    for p in primes():
        if p >= n: break
        if n % p == 0:
            isprime[n] = False
            break
    return isprime[n]

fifac = {}
def first_factor(n):
    assert n >= 2
    if n in fifac: return fifac[n]
    for p in primes():
        if n % p == 0:
            fifac[n] = p
            return fifac[n]
        if p * p > n:
            fifac[n] = n
            return fifac[n]

def factor(n):
    on = n
    ans = []
    if n < 0:
        ans.append((-1, 1))
        n = -n
    if n in [0, 1]: return ans
    p = first_factor(n)
    power = 0
    while n % p == 0:
        n //= p
        power += 1
    ans.append((p, power))
    rest = factor(n)
    if rest: ans.extend(rest)
    # m = 1
    # for (p, power) in ans: m *= p ** power
    # assert m == on, (on, ans)
    return ans

def square_free_factorization(f):
    return [p for (p, k) in f if k % 2]

def qrs(N): 
    ans = set() 
    for x in range(N//2 + 1): 
        ans.add((x * x) % N)
    rans = set()
    for q in ans:
        rans.add(q)
        # rans.add(-q)
    return rans

def unique_values(d):
    values = [d[k] for k in d]
    values.sort()
    ans = []
    for v in values:
        if ans and ans[-1] == v:
            continue
        ans.append(v)
    return ans

def square_free_minimal_residues(N):
    # For each prime, keep the "smallest" residue in which it appears
    minimal = {}
    for q in qrs(N):
        ps = square_free_factorization(factor(q))
        if ps and ps[0] == (-1, 1): ps = ps[1:]
        for p in ps:
            if p not in minimal or len(ps) < len(minimal[p]) or len(ps) == len(minimal[p]) and ps < minimal[p]:
                minimal[p] = ps
    return minimal

def verify(N, debug=False):
    minimal = square_free_minimal_residues(N)
    nonresidues = set()
    isolatable = set()
    unisolatable = set()
    for p in primes():
      if p >= N: break
      if p in minimal:
        if len(minimal[p]) > 1:
            unisolatable.add(p)
        else:
            assert minimal[p] == [p]
            isolatable.add(p)
      else:
          nonresidues.add(p)
    min_unisolatable = min(unisolatable) if unisolatable else None
    ok = True
    if len(unisolatable) == 0 and not is_prime(N): ok = False
    verified = ok
    minimal[None] = []
    if debug and len(factor(N)) <= 2:
        # print(f'{N}: isolatable: {list(sorted(isolatable))[:20]} unisolatable: {list(sorted(unisolatable))[:20]} min_unisolatable: {min_unisolatable} of {list(sorted(qrs(N)))} verified: {verified}')
        print(f'{N}: isolatable: {len(isolatable)} unisolatable: {len(unisolatable)} from {min_unisolatable}={minimal[min_unisolatable]} nonresidues: {len(nonresidues)} prime: {is_prime(N)} verified: {verified}')
        if not verified:
            print(unique_values(minimal))
    return verified

    
