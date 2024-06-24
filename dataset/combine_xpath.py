import json
import os
import re
import sys


def find_files_with_extension(directory, extension):
    files_with_extension = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                files_with_extension.append(os.path.join(root, file))
    return files_with_extension


def extract_number_and_xpath(file_path):
    prefix = file_path.rsplit(".", 2)[0]
    ess_file_path = f"{prefix}.ess"
    with open(ess_file_path, "r") as ess_file:
        content = ess_file.read()
        match = re.search(r"click<(\d+)>", content)
        if match:
            n = int(match.group(1))

    with open(file_path, "r") as ess_xpath_file:
        content = ess_xpath_file.read()
        with_xpath_match = re.search(r"click<(.+?)>", content)
        if with_xpath_match:
            xpath = with_xpath_match.group(1)
    return prefix, n, xpath


def update_json(prefix, n, xpath_value):
    json_file_path = f"{prefix}.json"
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    if isinstance(data, list) and n < len(data):
        data[n]["xpath"] = xpath_value

    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def main(directory):
    ess_with_xpath_files = find_files_with_extension(directory, ".ess.with_xpath")
    for file_path in ess_with_xpath_files:
        extract_number_and_xpath(file_path)
        prefix, n, xpath_value = extract_number_and_xpath(file_path)
        print(prefix, n, xpath_value)
        update_json(prefix, n, xpath_value)


if __name__ == "__main__":
    directory = sys.argv[1]  # Replace with your directory path
    main(directory)
