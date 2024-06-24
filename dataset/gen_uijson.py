import json
import os
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from typing import List

from utils import extract_ess_from_file


def get_feature(item, attrs=["class", "text", "resource-id", "content-desc", "bounds"]):
    feature = ""
    for attr in attrs:
        feature += item.get(attr, "") + " "
    return feature


"""
def filter_condition_xml(element):
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
    child_count = len(element)
    text = element.get("text", "")
    content_description = element.get("content-desc")
    visible = element.get("visible") == "true"
    element_class = element.get("class")

    if child_count != 0:
        return (
            text not in null_state or content_description not in null_state
        ) and visible
    else:
        condition = (
            visible
            and (
                text not in null_state
                or content_description not in null_state
                or element_class in switch_class
            )
            and "Menu" not in element_class
            and element_class != "android.view.ViewGroup"
            and element_class != "android.widget.FrameLayout"
            and element_class != "android.widget.LinearLayout"
            and element_class != "android.widget.RelativeLayout"
            and element_class != "android.widget.HorizontalScrollView"
        )
        return condition


def simplify_xml(xml_file_path):
    tree = etree.parse(xml_file_path)
    root = tree.getroot()

    def _parse_element(element):
        return {
            "class": element.get("class", ""),
            "text": element.get("text", ""),
            "resource-id": element.get("resource-id", ""),
            "content-desc": element.get("content-desc", ""),
            "bounds": element.get("bounds", ""),
            "enabled": element.get("enabled") == "true",
            "checked": element.get("checked") == "true",
            "checkable": element.get("checkable") == "true",
            "visible": element.get("visible") == "true",
            "selected": element.get("selected") == "true",
            "focused": element.get("focused") == "true",
            "focusable": element.get("focusable") == "true",
            "clickable": element.get("clickable") == "true",
            "long-clickable": element.get("long-clickable") == "true",
            "password": element.get("password") == "true",
            "scrollable": element.get("scrollable") == "true",
            "child_count": len(element),
        }

    def _process_element(element):
        filtered_data = []
        for elem in element.iter():
            item = _parse_element(elem)
            if filter_condition_xml(item):
                filtered_item = {
                    "id": len(filtered_data),
                    "class": item["class"],
                    "text": item["text"],
                    "resource-id": item["resource-id"],
                    "content-desc": item["content-desc"],
                    "bounds": item["bounds"].replace("], [", "][").replace(", ", ",")[1:-1] if item["bounds"] else "",
                    "enabled": item["enabled"],
                    "checked": item["checked"],
                    "checkable": item["checkable"],
                    "visible": item["visible"],
                    "selected": item["selected"],
                    "focused": item["focused"],
                    "focusable": item["focusable"],
                    "clickable": item["clickable"],
                    "long-clickable": item["long-clickable"],
                    "password": item["password"],
                    "scrollable": item["scrollable"],
                    "xpath": elem.getroottree().getpath(elem),
                }
                filtered_data.append(filtered_item)
        return filtered_data

    return _process_element(root)
"""


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


def get_ess_ids(ess_path: str) -> List[int]:
    """For essential states annotated on a UI representation, return their IDs.
    Cases:
    - If k == "activity", the v is always 0. Ignore this case.
    """
    return [
        int(v)
        for k, v in extract_ess_from_file(ess_path)
        if v.isdigit() and int(v) >= 0 and k != "activity"
    ]


def trans_json(vh_path, json_path, ess_path):
    """Params:
    1. os.path.exists(vh_path): always True;
    2. os.path.exists(json_path): True only when the json file has been generated
    before; else False.
    3. os.path.exists(ess_path): True only when there are essential states
    annotated on this UI repr; else False.

    Cases:
    1. When there is ess_path, there must be json_path as ess_path is generated
    according to the contents in json_path. In this case, this method will
    generate a new json file without losing the key information of essential
    states.
    2. When there is no json_path and no ess_path, directly generate a new json
    file based on vh_path.
    """
    # if there is essential states in this UI repr, preserve UI components with
    # the same numeric id and replace the rest with the newest version of
    # simplified VH
    with open(json_path, "r") as f:
        old_json_data = json.load(f)
    if old_json_data is None:
        return simplify_vh(vh_path)

    if os.path.exists(ess_path):
        ess_ids: List[int] = get_ess_ids(ess_path)
    else:
        ess_ids = []
    # if there is no essential states associated with UI components (with numeric
    # ids), just replace the json file with the newest version of simplified VH
    if len(ess_ids) == 0:
        return simplify_vh(vh_path)

    # find data to be preserved in old_json_data
    preserved_data = {
        ui_comp["id"]: ui_comp for ui_comp in old_json_data if ui_comp["id"] in ess_ids
    }
    new_json_data = simplify_vh(vh_path)
    updated_data = []
    preserved_data_ids = list(preserved_data.keys())

    def _insert_with_index_update(lst: List, index: int, source: str, item: dict):
        """Params:
        - source: "new" or "preserved"
        """
        item["id"] = index
        item["source"] = source
        lst.append(item)
        return lst

    i = 0
    new_json_data_index = 0
    while new_json_data_index < len(new_json_data) or preserved_data_ids:
        if i in preserved_data:
            updated_data = _insert_with_index_update(
                updated_data, i, "preserved", preserved_data[i]
            )
            preserved_data_ids.remove(i)
        elif new_json_data_index < len(new_json_data):
            updated_data = _insert_with_index_update(
                updated_data, i, "new", new_json_data[new_json_data_index]
            )
            new_json_data_index += 1
        i += 1

        if new_json_data_index >= len(new_json_data):
            if not preserved_data_ids:
                break
            else:
                # add remaining preserved data to updated_data
                for id in preserved_data_ids:
                    updated_data = _insert_with_index_update(
                        updated_data, i, "preserved", preserved_data[id]
                    )
                    i += 1
                break

    # check are there any identical items in updated_data
    item_occurrences = defaultdict(list)
    for item in updated_data:
        excluded_keys = ["id", "source", "xpath"]
        item_copy = {k: v for k, v in item.items() if k not in excluded_keys}
        item_key = frozenset(item_copy.items())
        item_occurrences[item_key].append(item)

    # remove duplicated items in preserved data and new data
    # the definition of duplication: when the values of their attributes,
    # excluding 'xpath', 'source', and 'id' are the same
    # if there is duplication, move the old id to the new id and append to
    # updated_data_without_dup
    updated_data_without_dup = []
    for item_list in item_occurrences.values():
        if len(item_list) > 1:
            # print("Identical items found", item_list, "start to update the old one")
            new_item = None
            preserved_id = None
            for item in item_list:
                if item["source"] == "preserved":
                    preserved_id = item["id"]
                elif item["source"] == "new":
                    new_item = item

            if new_item is not None:
                if preserved_id is not None:
                    new_item["id"] = preserved_id
                updated_data_without_dup.append(new_item)
            else:
                raise Exception(
                    f"duplicated items found: {item_list}, but no preserved id to be updated found"
                )
        else:
            updated_data_without_dup.append(item_list[0])

    print(
        f"{vh_path}, old: {len(old_json_data)} items, new: {len(updated_data_without_dup)} items"
    )

    # sort updated_data_without_dup by the 'id' attribute of its items
    updated_data_without_dup.sort(key=lambda item: item["id"])
    return updated_data_without_dup


def re_generated_json(vh_path, json_path, output_path):
    """if there is essential state annotated on this UI repr, generate new json
    file without losing the key information of essential states
    else just simplify the vh file to generate json file
    """
    if os.path.exists(json_path):
        ess_path = json_path.replace(".json", ".ess")
        new_json_data = trans_json(
            vh_path=vh_path, json_path=json_path, ess_path=ess_path
        )
    else:
        new_json_data = simplify_vh(vh_path)

    with open(output_path, "w") as f:
        json.dump(new_json_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # paths of all traces to be processed
    all_trace_paths = []

    if len(sys.argv) < 3:
        print(
            "Usage: (1) Generate selected UI components json file for all traces: "
            "python gen_uijson.py all [dataset_path]"
        )
        print(
            "(2) Generate selected UI components json file for specific traces: "
            "python gen_uijson.py single [trace_path1] [trace_path2] ..."
        )
        exit(1)

    elif sys.argv[1] == "all":
        dataset_path = sys.argv[2]
        cats = ["general", "generated", "googleapps", "install", "webshopping"]
        for c in cats:
            folder_path = os.path.join(dataset_path, c)

            traces_path = [
                os.path.join(folder_path, trace) for trace in os.listdir(folder_path)
            ]
            traces_path = [
                trace
                for trace in traces_path
                if "trace" in trace and os.path.isdir(trace)
            ]
            all_trace_paths.extend(traces_path)

    elif sys.argv[1] == "single":
        [all_trace_paths.append(path) for path in sys.argv[2:]]

    # put all vh files to be processed into vh_files_path
    vh_paths = []
    for trace_path in all_trace_paths:
        [
            vh_paths.append(os.path.join(trace_path, file))
            for file in os.listdir(trace_path)
            if file.rsplit(".", 1)[-1].lower() == "vh"
        ]
    # with ProcessPoolExecutor(max_workers=8) as executor:
    #     for xml_path in xml_paths:
    #         executor.submit(re_generated_json, xml_path, xml_path.replace(".xml", ".json"), xml_path.replace(".xml", ".json_new"))

    for vh_path in vh_paths:
        re_generated_json(
            vh_path,
            vh_path.replace(".vh", ".json"),
            vh_path.replace(".vh", ".json_new"),
        )
