#!/usr/bin/env python3
import argparse
import math


def cyclic_disjoint_subset_count(window_capacity, width, arity):
    # Number of arity-k start-position sets on a ring of N=m*w bits whose
    # width-w windows are pairwise disjoint. Standard cyclic spacing count.
    n = window_capacity * width
    reduced = n - (width - 1) * arity
    if reduced <= 0:
        return 0
    return n * math.comb(reduced, arity) // reduced


def main():
    parser = argparse.ArgumentParser(description="Experiment 058: K7 subset oracle vs K8 prefix scan scaling.")
    parser.add_argument("--width", type=int, default=5)
    parser.add_argument("--min-capacity", type=int, default=4)
    parser.add_argument("--max-capacity", type=int, default=12)
    args = parser.parse_args()

    for capacity in range(args.min_capacity, args.max_capacity + 1):
        k7 = sum(
            cyclic_disjoint_subset_count(capacity, args.width, arity)
            for arity in range(2, capacity + 1)
        )
        # N physical starts, at most capacity-1 closure tests after the first window.
        k8 = args.width * capacity * (capacity - 1)
        print(
            f"capacity={capacity} k7_subset_candidates={k7} "
            f"k8_prefix_checks={k8} ratio={k7 / k8:.6f}"
        )


if __name__ == "__main__":
    main()
