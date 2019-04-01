import mpmath

lines = open('good3.txt').readlines()

sums = {}
threshold = 50000

def Li(x): return mpmath.li(x, offset=True)

last_printed = -threshold

for (i, line) in enumerate(lines):
    m = i + 1
    n = int(line.split()[0])
    # if n % 10 == 0: continue
    w = n // threshold
    if w not in sums: sums[w] = [0] * 9
    sums[w][n % 9] += 1

    if n - last_printed < threshold:
        continue
    last_printed = n

    def ratios_str_sum(nums):
        assert len(nums) == 9
        ratios = [nums[i] * 9 / li for i in range(9)]
        ratios_sum = sum(ratios)
        ratios_str = [mpmath.nstr(f, 4) for f in ratios]
        return ratios_str, ratios_sum

    print("%s %s: " % (m, n))
    for ww in range(w + 1):
        print("    %s" % sums[ww])
    for ww in range(w + 1):
        li = max(1, Li(threshold * (ww + 1)) - Li(threshold * ww))
        ratios_str, ratios_sum = ratios_str_sum(sums[ww])
        print("    %s %s %s %s" % (ww, ratios_str, ratios_sum, mpmath.nstr(sum(sums[ww]) / li, 4)))
    all_sums = [sum(sums[ww][i] for ww in range(w + 1)) for i in range(9)]
    li = max(1, Li(n))
    ratios_str, ratios_sum = ratios_str_sum(all_sums)
    print("    %s %s %s %s" % (n, ratios_str, ratios_sum, mpmath.nstr(sum(all_sums) / li, 4)))
    
