import os
import sys
from collections import defaultdict

import pandas as pd


def proc_action_agg_file(filepath: str):
    ret = defaultdict(int)
    for line in open(filepath):
        line = line.strip()
        action_type = line.split()[0]
        ret[action_type] += 1
    return ret


def get_action_stats(dataset_path: str):
    categories = os.listdir(dataset_path)

    # get the action set
    action_set = set()
    for c in categories:
        category_path = os.path.join(dataset_path, c)
        if not os.path.isdir(category_path):
            continue

        for trace in os.listdir(category_path):
            trace_path = os.path.join(category_path, trace)
            if not os.path.isdir(trace_path):
                continue

            action_agg_file = os.path.join(trace_path, "eventStructs.txt")
            action_ret = proc_action_agg_file(action_agg_file)
            action_set.update(action_ret.keys())

    # build a dataframe
    columns = ["trace"]
    for action in action_set:
        columns.append(action[1:-1].lower())
    df = pd.DataFrame(columns=columns)

    # iterate the dataset again to fill the dataframe
    for c in categories:
        category_path = os.path.join(dataset_path, c)
        if not os.path.isdir(category_path):
            continue

        for trace in os.listdir(category_path):
            trace_path = os.path.join(category_path, trace)
            if not os.path.isdir(trace_path):
                continue

            action_agg_file = os.path.join(trace_path, "eventStructs.txt")
            action_ret = proc_action_agg_file(action_agg_file)

            row = [trace_path]
            for action in action_set:
                row.append(action_ret.get(action, 0))

            df.loc[len(df)] = row

    # Assuming df is your DataFrame
    non_zero_counts = df[columns[1:]].astype(bool).sum()

    # Calculate sum
    sums = df[columns[1:]].sum()

    # Calculate mean using non-zero counts as the base
    means = sums / non_zero_counts

    # Calculate median
    medians = df[columns[1:]].where(df != 0).median()

    # Calculate standard deviation
    stddevs = df[columns[1:]].where(df != 0).std()

    # Create a new DataFrame for the statistics
    stats = pd.DataFrame(
        {
            "sum": sums,
            "# Tasks W/ action": non_zero_counts,
            "mean": means,
            "median": medians,
            "stddev": stddevs,
        }
    )

    print(stats)


def get_ess_stats_cnts(dataset_path):
    categories = os.listdir(dataset_path)

    for c in categories:
        category_path = os.path.join(dataset_path, c)
        if not os.path.isdir(category_path):
            continue

        for trace in os.listdir(category_path):
            trace_path = os.path.join(category_path, trace)
            if not os.path.isdir(trace_path):
                continue

            ess_file_lists = []
            for f in os.listdir(trace_path):
                if f.endswith(".ess"):
                    ess_file_path = os.path.join(trace_path, f)
                    ess_file_lists.append(ess_file_path)
            print(f"{trace_path} has {len(ess_file_lists)} ess files")


def extract_all_ess_from_single_trace(trace_path):
    all_ess = defaultdict(int)
    for f in os.listdir(trace_path):
        if f.endswith(".ess"):
            ess_file_path = os.path.join(trace_path, f)
            for line in open(ess_file_path):
                line = line.strip()
                ess = line.split("|")
                if line == "" or len(ess) == 0:
                    continue
                for p in ess:
                    p_keyword = p.split("<")[0] if p != "fuzzy<-1>" else p
                    all_ess[p_keyword] += 1
    return all_ess


def get_ess_primitive_distribution(dataset_path):
    categories = os.listdir(dataset_path)

    primitive_set = set()
    for c in categories:
        category_path = os.path.join(dataset_path, c)
        if not os.path.isdir(category_path):
            continue

        for trace in os.listdir(category_path):
            trace_path = os.path.join(category_path, trace)
            if not os.path.isdir(trace_path):
                continue

            ess = extract_all_ess_from_single_trace(trace_path)
            primitive_set.update(ess.keys())

    # build a dataframe
    columns = ["trace"]
    for primitive in primitive_set:
        columns.append(primitive)
    df = pd.DataFrame(columns=columns)

    for c in categories:
        category_path = os.path.join(dataset_path, c)
        if not os.path.isdir(category_path):
            continue

        for trace in os.listdir(category_path):
            trace_path = os.path.join(category_path, trace)
            if not os.path.isdir(trace_path):
                continue

            ess = extract_all_ess_from_single_trace(trace_path)
            row = [trace_path]
            for p in primitive_set:
                row.append(ess.get(p, 0))
            df.loc[len(df)] = row

    # Assuming df is your DataFrame
    non_zero_counts = df[columns[1:]].astype(bool).sum()

    # Calculate sum
    sums = df[columns[1:]].sum()

    # Calculate mean using non-zero counts as the base
    means = sums / non_zero_counts

    # Calculate median
    medians = df[columns[1:]].where(df != 0).median()

    # Calculate standard deviation
    stddevs = df[columns[1:]].where(df != 0).std()

    # Create a new DataFrame for the statistics
    stats = pd.DataFrame(
        {
            "sum": sums,
            "# Tasks W/ primitive": non_zero_counts,
            "mean": means,
            "median": medians,
            "stddev": stddevs,
        }
    )

    print(stats)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python dataset_stats.py <dataset_path>"
    dataset_path = sys.argv[1]
    get_action_stats(dataset_path)
    get_ess_stats_cnts(dataset_path)
    get_ess_primitive_distribution(dataset_path)
