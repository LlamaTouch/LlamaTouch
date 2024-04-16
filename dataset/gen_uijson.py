import json
import logging
import os
import re
import sys


def read_json(json_fp):
    if not os.path.exists(json_fp):
        return []
    with open(json_fp, "r") as f:
        data = json.load(f)
    return data


def get_feature(item, attrs=["class", "text", "resource-id", "content-desc", "bounds"]):
    feature = ""
    for attr in attrs:
        feature += item.get(attr, "") + " "
    return feature


def filter_condition(item):
    null_state = ["", None, "None", "null"]
    switch_class = [
        "android.widget.Switch",
        "android.widget.CheckBox",
        "android.widget.RadioButton",
        "android.widget.ToggleButton",
        "android.widget.Button",
        "android.widget.ImageButton",
        "android.widget.ImageView",
        "android.widget.TextView",
        "android.widget.EditText",
        "android.widget.ProgressBar",
        "android.widget.SeekBar",
        "android.widget.Spinner",
    ]

    if item.get("child_count") != 0:
        return (
            item.get("text", "") not in null_state
            or item.get("content_description", "") not in null_state
            and item.get("visible") == True
        )
    else:
        condition = (
            item.get("child_count") == 0
            and item.get("visible") == True
            and (
                item.get("text", None) not in null_state
                or item.get("content_description", None) not in null_state
                or item.get("class", None) in switch_class
            )
            # and "Image" not in item.get("class")
            # and "Button" not in item.get("class")
            and "Menu" not in item.get("class")
            and item.get("class") != "android.view.ViewGroup"
            and item.get("class") != "android.widget.FrameLayout"
            and item.get("class") != "android.widget.LinearLayout"
            and item.get("class") != "android.widget.RelativeLayout"
            and item.get("class") != "android.widget.HorizontalScrollView"
        )
        return condition


def simplify_vh(vh_file_path):
    with open(vh_file_path, "r") as f:
        data = json.load(f)
    filtered_data = []
    for item in data:
        if filter_condition(item):
            filtered_item = {
                "id": len(filtered_data),
                "class": (
                    str(item.get("class", "")).encode().decode("utf-8")
                    if item.get("class") is not None
                    else ""
                ),
                "text": (
                    str(item.get("text", "")).encode().decode("utf-8")
                    if item.get("text") is not None
                    else ""
                ),
                "resource-id": (
                    str(item.get("resource_id", "")).encode().decode("utf-8")
                    if item.get("resource_id") is not None
                    else ""
                ),
                "content-desc": (
                    str(item.get("content_description", "")).encode().decode("utf-8")
                    if item.get("content_description") is not None
                    else ""
                ),
                "bounds": (
                    str(item.get("bounds", "")).encode().decode("utf-8")
                    if item.get("bounds") is not None
                    else ""
                ),
                "enabled": item.get("enabled", False),
                "checked": item.get("checked", False),
                "checkable": item.get("checkable", False),
                "visible": item.get("visible", False),
                "selected": item.get("selected", False),
                "focused": item.get("focused", False),
                "focusable": item.get("focusable", False),
                "clickable": item.get("clickable", False),
                "long-clickable": item.get("long_clickable", False),
                "password": item.get("password", False),
                "scrollable": item.get("scrollable", False),
            }
            temp = filtered_item["bounds"]
            temp = temp.replace("], [", "][")[1:-1]
            temp = temp.replace(", ", ",")
            filtered_item["bounds"] = temp
            filtered_data.append(filtered_item)

    return filtered_data


def is_checkpoint_json_file(folder_path, index):
    checkpoint_path = os.path.join(folder_path, f"{str(index)}_drawed.png.text")
    print(f"checkpoint_path: {checkpoint_path}")
    return os.path.exists(checkpoint_path)


def get_noted_id(checkpoint_fp):
    noted_ids = []
    with open(checkpoint_fp, "r") as f:
        lines = f.readlines()
        for line in lines:
            pattern = re.compile(r"<(-?\d+)(?::.*?)?>")
            noted_ids += re.findall(pattern, line)

    for item in noted_ids:
        if item == "-1":
            noted_ids.remove(item)
        item = int(item)

    return noted_ids


def trans_json(vh_fp, json_fp):
    checkpoint_fp = json_fp[:-5] + "_drawed.png.text"
    noted_ids = get_noted_id(checkpoint_fp)
    new_json_data = simplify_vh(vh_fp)
    old_json_data = read_json(json_fp)
    index_map = dict()
    for noted_id in noted_ids:
        noted_id = int(noted_id)
        if noted_id >= len(new_json_data):
            logging.info(f"warning{noted_id} out of range! {vh_fp}")
            return old_json_data
        print(f"len of new_json_data: {len(new_json_data)}")
        # print(new_json_data)
        onode = old_json_data[noted_id]
        print(f"noted_id: {noted_id}")
        flag = False
        for nnode in new_json_data:
            if get_feature(onode) == get_feature(nnode):
                flag = True
                index_map[noted_id] = nnode["id"]
                # swap
                temp = new_json_data[noted_id]
                new_json_data[noted_id] = nnode
                new_json_data[nnode["id"]] = temp
                # swap id
                temp_id = new_json_data[noted_id]["id"]
                new_json_data[noted_id]["id"] = new_json_data[index_map[noted_id]]["id"]
                new_json_data[index_map[noted_id]]["id"] = temp_id
                print(f"warning: Found in new data! {vh_fp}:{noted_id}")
                logging.info(f"warning: Found in new data! {vh_fp}:{noted_id}")
                break
        if not flag:
            print(f"warning: Not found in new data! {vh_fp}:{noted_id}")
            logging.info(f"warning: Not found in new data! {vh_fp}:{noted_id}")
            temp = new_json_data[noted_id]
            new_json_data[noted_id] = onode
            new_json_data.append(temp)
            # swap id
            new_json_data[len(new_json_data) - 1]["id"] = len(new_json_data) - 1
    return new_json_data


def re_generated_json(vh_fp, json_fp, output_path):
    index = eval(os.path.splitext(os.path.basename(json_fp))[0])
    folder_path = os.path.dirname(json_fp)
    print(f"fpath: {folder_path}")

    if is_checkpoint_json_file(folder_path, index):
        new_json_data = trans_json(vh_fp, json_fp)
    else:
        new_json_data = simplify_vh(vh_fp)

    with open(output_path, "w") as f:
        json.dump(new_json_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    vh_files_path = []

    if len(sys.argv) == 1:
        cats = ["general", "generated", "googleapps", "install", "webshopping"]
        for sub_categories in cats:
            folder_path = sub_categories

            traces_path = os.listdir(folder_path)
            traces_path = [os.path.join(folder_path, trace) for trace in traces_path]
            traces_path = [trace for trace in traces_path if "trace" in trace]
            traces_path = [trace for trace in traces_path if os.path.isdir(trace)]

            for trace_path in traces_path:
                vh_files = [
                    file
                    for file in os.listdir(trace_path)
                    if file.rsplit(".", 1)[-1].lower() == "vh"
                ]
                for vh_file in vh_files:
                    vh_files_path.append(os.path.join(trace_path, vh_file))
    else:
        for path in sys.argv[1:]:
            vh_files_path.append(path)

    for vh in vh_files_path:
        re_generated_json(vh, vh[:-2] + "json", vh[:-2] + "json")
        print(f"convert {vh} to {vh[:-2] + 'json'}")
