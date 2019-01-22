#include <iostream>
#include <cmath>
#include <gmpxx.h>
#ifdef PY_COMPATIBLE_OUTPUT
#include <vector>
#else
int lowest_k = 0, highest_k = 0;
#endif

const int MAXN = 10000000;
const int MAX_LEN = MAXN; // Something like MAXN / (4.5 log n) will do
char str[MAX_LEN + 2];

int best_k(int n) {
  // If n = 10m, then S(n^k) = S(m^k)
  int m = n;
  while (m % 10 == 0) {
    m /= 10;
  }
  // Roughly, S(m^k) = k * 4.5 * log10(m) should be n,
  // so k should be roughly n / (4.5 * log10(m))
  return n / (4.5 * std::log10(m));
}

int main() {
  std::ios::sync_with_stdio(false);
  for (int n = 2; n < MAX_LEN; ++n) {
    bool good = false;
#ifdef PY_COMPATIBLE_OUTPUT
    std::vector<int> good_k;
#else
    int which_k;
#endif
    int K = best_k(n);
    for (int k = std::max(0, K + 2*lowest_k - 5); k <= K + 2*highest_k + 5; ++k) {
      mpz_class nk;
      mpz_ui_pow_ui(nk.get_mpz_t(), n, k);
      mpz_get_str(str, 10, nk.get_mpz_t());
      int sum = 0;
      for (int i = 0; str[i] != '\0'; ++i) {
	sum += str[i] - '0';
      }
      if (sum == n) {
	good = true;
#ifdef PY_COMPATIBLE_OUTPUT
	good_k.push_back(k);
#else
	which_k = k - K;
	lowest_k = std::min(lowest_k, which_k);
	highest_k = std::max(highest_k, which_k);
	break;
#endif
      }
    }

#ifdef PY_COMPATIBLE_OUTPUT
    std::cout << n << ": " << std::endl;
    if (good) {
      std::cout << "        [";
      for (int i = 0; i < good_k.size(); ++i) {
	std::cout << good_k[i];
	if (i < good_k.size() - 1) std::cout << ", ";
      }
      std::cout << "]" << std::endl;
    }
#else
    if (good) {
      std::cout << n << " " << which_k << " " << lowest_k << " " << highest_k << std::endl;
    }
#endif
  }
}
