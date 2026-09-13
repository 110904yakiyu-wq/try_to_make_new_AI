#!/usr/bin/env python3
import argparse
import importlib.util
import math
import statistics
from pathlib import Path


def load_exp000():
    path = Path(__file__).resolve().parents[1] / "000_ca_null_substrate" / "run.py"
    spec = importlib.util.spec_from_file_location("exp000", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inject_core(exp, state, pos, core_value, width):
    out = state[:]
    bits = exp.int_to_bits(core_value, width)
    n = len(out)
    for j, bit in enumerate(bits):
        out[(pos + j) % n] = bit
    return out


def run_training(exp, initial, training_core, schedule, train_steps, pos, width):
    state = initial[:]
    schedule = set(schedule)

    for t in range(train_steps):
        if t in schedule:
            state = inject_core(exp, state, pos, training_core, width)
        state = exp.step_ring(state)

    return state


def probe_impact(exp, state, probe_core, pos, width, probe_steps):
    baseline = state[:]
    probed = inject_core(exp, state, pos, probe_core, width)

    for _ in range(probe_steps):
        baseline = exp.step_ring(baseline)
        probed = exp.step_ring(probed)

    changed = sum(a != b for a, b in zip(baseline, probed))
    return changed / len(state)


def parse_schedule(text):
    values = sorted({int(x.strip()) for x in text.split(",") if x.strip()})
    if not values:
        raise ValueError("training schedule must not be empty")
    return values


def main():
    exp = load_exp000()
    parser = argparse.ArgumentParser(
        description="Experiment 003: experience-specific response assay."
    )
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--a", type=int, default=0b011)
    parser.add_argument("--b", type=int, default=0b101)
    parser.add_argument("--schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=24)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--position-stride", type=int, default=1)
    parser.add_argument("--show-extremes", type=int, default=8)
    args = parser.parse_args()

    if args.a >= (1 << args.core_width) or args.b >= (1 << args.core_width):
        raise SystemExit("A and B must fit within core-width")

    schedule = parse_schedule(args.schedule)
    if schedule[-1] >= args.probe_time:
        raise SystemExit("probe-time must be after the final training exposure")

    initial = exp.make_initial(args.size, "single")
    rows = []

    for pos in range(0, args.size, args.position_stride):
        state_a = run_training(
            exp, initial, args.a, schedule, args.probe_time, pos, args.core_width
        )
        state_b = run_training(
            exp, initial, args.b, schedule, args.probe_time, pos, args.core_width
        )

        aa = probe_impact(exp, state_a, args.a, pos, args.core_width, args.probe_steps)
        ab = probe_impact(exp, state_a, args.b, pos, args.core_width, args.probe_steps)
        ba = probe_impact(exp, state_b, args.a, pos, args.core_width, args.probe_steps)
        bb = probe_impact(exp, state_b, args.b, pos, args.core_width, args.probe_steps)

        score = ((ab - aa) + (ba - bb)) / 2.0
        rows.append((pos, score, aa, ab, ba, bb))

    scores = [row[1] for row in rows]
    mean = statistics.mean(scores)
    stdev = statistics.stdev(scores) if len(scores) > 1 else 0.0
    stderr = stdev / math.sqrt(len(scores)) if scores else float("nan")
    t_like = mean / stderr if stderr > 0 else float("nan")

    print(f"positions={len(rows)}")
    print(
        f"A={format(args.a, f'0{args.core_width}b')} "
        f"B={format(args.b, f'0{args.core_width}b')}"
    )
    print(
        f"schedule={schedule} probe_time={args.probe_time} "
        f"probe_steps={args.probe_steps}"
    )
    print(f"mean_cross_over_score={mean:.9f}")
    print(f"stdev={stdev:.9f}")
    print(f"stderr={stderr:.9f}")
    print(f"mean_over_stderr={t_like:.6f}")
    print()

    k = max(0, args.show_extremes)
    if k:
        print("most negative positions:")
        for pos, score, aa, ab, ba, bb in sorted(rows, key=lambda r: r[1])[:k]:
            print(
                f"pos={pos:>3} score={score:+.6f} "
                f"AA={aa:.6f} AB={ab:.6f} BA={ba:.6f} BB={bb:.6f}"
            )

        print()
        print("most positive positions:")
        for pos, score, aa, ab, ba, bb in sorted(
            rows, key=lambda r: r[1], reverse=True
        )[:k]:
            print(
                f"pos={pos:>3} score={score:+.6f} "
                f"AA={aa:.6f} AB={ab:.6f} BA={ba:.6f} BB={bb:.6f}"
            )


if __name__ == "__main__":
    main()
