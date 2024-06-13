"""
This script is used to check the consistency of task descriptions between the 
metadata file 'llamatouch_task_matadata.tsv' and tasks inside each subfolder.
"""

import os
import sys

import pandas as pd


def check_all_tasks(metadata_path: str, dataset_path: str):
    df = pd.read_csv(metadata_path, sep="\t")

    for _, row in df.iterrows():
        task_path = os.path.join(dataset_path, row["path"], "instruction.txt")
        assert os.path.exists(task_path)

        with open(task_path) as f:
            lines = f.readlines()
        task_description = lines[1].strip()

        if task_description != row["description"]:
            print(f"Task description mismatch [{row['path']}]")
            print(f"(metadata) '{row['description']}'")
            print(f"(dataset)  '{task_description}'")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python validate_metadata_dataset.py <metadata_path> <dataset_path>"
        )
        sys.exit(1)

    check_all_tasks(sys.argv[1], sys.argv[2])
