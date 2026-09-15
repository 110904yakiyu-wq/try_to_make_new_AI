#!/usr/bin/env python3
import argparse
import importlib.util
import random
from pathlib import Path


def load_exp068():
    path = Path(__file__).resolve().parents[1] / "068_reversal_and_metric_robustness" / "run.py"
    spec = importlib.util.spec_from_file_location("exp068", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def swap_labels(schedule):
    return "".join("Q" if x == "P" else "P" for x in schedule)


def final_run_schedule(run_length):
    p_left = 8 - run_length
    q_left = 8
    prefix = []
    last = None
    while p_left + q_left:
        options = []
        if p_left:
            options.append("P")
        if q_left:
            options.append("Q")
        opposite = None if last is None else ("Q" if last == "P" else "P")
        if opposite in options:
            token = opposite
        else:
            token = "Q" if q_left >= p_left else "P"
        if token == "Q" and q_left == 1 and p_left > 0:
            token = "P"
        prefix.append(token)
        last = token
        if token == "P":
            p_left -= 1
        else:
            q_left -= 1
    assert prefix[-1] == "Q"
    schedule = "".join(prefix) + "P" * run_length
    assert schedule.count("P") == schedule.count("Q") == 8
    return schedule


def compare_with_event_budget(exp068, schedule, backgrounds, washout, train_event_budget):
    exp066 = exp068.load_exp066()
    exp066.exp = exp066.load_exp057()

    class Args:
        pass
    args = Args()
    args.backgrounds = backgrounds
    args.key_width = 3
    args.window_capacity = 6
    args.size = 18
    args.core_width = 3
    args.event_budget = train_event_budget
    args.recovery_events = 3
    args.washout_events = washout

    return exp068.compare(exp066, schedule, swap_labels(schedule), args, 7)[0]


def main():
    p = argparse.ArgumentParser(description="Experiment 069: schedule geometry audit.")
    p.add_argument("--backgrounds", type=int, default=16)
    args = p.parse_args()
    exp068 = load_exp068()

    jitter = "PQPQQPPQPQPQQPQP"  # 8 P, 8 Q, ends P
    c = compare_with_event_budget(exp068, jitter, args.backgrounds, 6, 3)
    print(f"jitter recent={c['recent']} old={c['old']} tie={c['tie']} strict={c['strict']}")

    print("train_event_budget_sweep")
    block = "Q" * 8 + "P" * 8
    for budget in range(1, 7):
        c = compare_with_event_budget(exp068, block, 8, 6, budget)
        print(f"budget={budget} recent={c['recent']} old={c['old']} tie={c['tie']} strict={c['strict']}")

    print("final_run_length_sweep")
    for run_length in range(1, 9):
        schedule = final_run_schedule(run_length)
        c = compare_with_event_budget(exp068, schedule, 8, 6, 3)
        print(f"run={run_length} schedule={schedule} recent={c['recent']} old={c['old']} tie={c['tie']} strict={c['strict']}")

    print("random_equal_count_schedules")
    rng = random.Random(12345)
    schedules = []
    while len(schedules) < 16:
        tokens = ["P"] * 8 + ["Q"] * 8
        rng.shuffle(tokens)
        if tokens[-1] != "P":
            continue
        schedule = "".join(tokens)
        if schedule not in schedules:
            schedules.append(schedule)
    for schedule in schedules:
        c = compare_with_event_budget(exp068, schedule, 4, 6, 3)
        print(f"schedule={schedule} recent={c['recent']} old={c['old']} tie={c['tie']} strict={c['strict']}")


if __name__ == "__main__":
    main()
