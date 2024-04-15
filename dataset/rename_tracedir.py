import os
import re
import shutil
import sys


def proc_single_trace(folder_path: str):
    ignore_files = ["eventStructs.txt", "instuction.txt", "resolution.txt"]

    for subfolder in ["processed_image", "json"]:
        path_to_delete = os.path.join(folder_path, subfolder)
        if os.path.exists(path_to_delete):
            shutil.rmtree(path_to_delete)
            print(f"delete: {subfolder}")

    files = os.listdir(folder_path)

    pattern = re.compile(
        r"^(emulator-5554 \d{4}_\d{1,2}_\d{1,2} (\d{2}_\d{2}_\d{2})).*\.(txt|png|vh|xml)$"
    )
    file_groups = {}
    for file in files:
        if file in ignore_files:
            continue
        match = pattern.match(file)
        if match:
            timestamp = match.group(2)
            if timestamp not in file_groups:
                file_groups[timestamp] = []
            file_groups[timestamp].append(file)

    sorted_timestamps = sorted(file_groups.keys())

    for index, timestamp in enumerate(sorted_timestamps):
        for file in sorted(file_groups[timestamp]):
            if ".png_hierarchy.vh" in file:
                new_name = f"{index}.vh"
            elif ".xml" in file:
                new_name = f"{index}.xml"
            elif "activityName.txt" in file:
                new_name = f"{index}.activity"
            elif "png_image.png" in file:
                new_name = f"{index}.png"
            else:
                print(f"{file} unknown suffix")

            old_file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(folder_path, new_name)
            os.rename(old_file_path, new_file_path)
            print(f"rename '{file}' to '{new_name}'")


def proc_all():
    cats = ["general", "webshopping", "generated", "install", "googleapps"]
    for c in cats:
        trace_folders = os.listdir(c)

        for trace_folder in trace_folders:
            trace_path = os.path.join(c, trace_folder)
            if os.path.isdir(trace_path):
                proc_single_trace(trace_path)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        proc_all()
    else:
        for path in sys.argv[1:]:
            proc_single_trace(path)
