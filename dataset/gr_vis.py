import copy
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from evaluator.task_trace import DatasetHelper, TaskTrace
from evaluator.utils.visualization import plot_episode
from PIL import Image

helper = DatasetHelper()


def plot_by_folder(trace_folder: str):
    episode, task_description = open(
        os.path.join(trace_folder, "instruction.txt")
    ).readlines()
    episode = episode.strip()
    task_description = task_description.strip()

    trace = helper._load_groundtruth_trace_by_path(trace_folder)

    c = trace_folder.split("/")[0]

    output_file = os.path.join(trace_folder, "agg_plot.png")
    plot_single_trace(
        epi=episode,
        category=c,
        task_description=task_description,
        task_trace=trace,
        output_file=output_file,
    )


def plot_single_trace(
    epi: str,
    category: str,
    task_description: str,
    task_trace: TaskTrace,
    output_file: str,
):

    ui_infos_for_plot = []
    step_id = 0
    for ui_state in task_trace:
        current_ui_state = {
            "image": None,
            "episode_id": None,
            "category": None,
            "step_id": None,
            "goal": None,
            "result_action": [None, None],
            "result_touch_yx": None,
            "result_lift_yx": None,
            "image_height": 1140,
            "image_width": 540,
            "image_channels": 3,
            "ui_positions": None,
            "ui_text": None,
            "ui_type": None,
            "ui_state": None,
            "essential_states": None,
        }
        img = Image.open(ui_state.screenshot_path).convert("RGB")
        img_arr = np.array(img)
        current_ui_state["image_height"] = img.height
        current_ui_state["image_width"] = img.width
        current_ui_state["category"] = category
        current_ui_state["image"] = img_arr
        current_ui_state["episode_id"] = epi
        current_ui_state["step_id"] = step_id
        step_id += 1
        current_ui_state["goal"] = task_description
        current_ui_state["result_action"][0] = ui_state.action.action_type
        current_ui_state["result_action"][1] = ui_state.action.typed_text
        current_ui_state["result_touch_yx"] = ui_state.action.touch_point_yx
        current_ui_state["result_lift_yx"] = ui_state.action.lift_point_yx

        if ui_state.state_type == "groundtruth":
            ess = ui_state.essential_state
            current_ui_state["essential_states"] = ess
            # passing the whole ui_state for a quick implementation
            current_ui_state["ui_state"] = ui_state

        ui_infos_for_plot.append(copy.deepcopy(current_ui_state))
    plot_episode(
        ui_infos_for_plot,
        show_essential_states=True,
        show_annotations=False,
        show_actions=True,
        output_file=output_file,
    )


def plot_all():

    from concurrent.futures import ProcessPoolExecutor

    e = ProcessPoolExecutor(max_workers=30)

    cats = ["general", "generated", "googleapps", "install", "webshopping"]
    for c in cats:
        for trace in os.listdir(c):
            if not os.path.isdir(os.path.join(c, trace)):
                continue

            episode, task_description = open(
                os.path.join(c, trace, "instruction.txt")
            ).readlines()
            episode = episode.strip()
            task_description = task_description.strip()

            trace_id = trace
            trace_path = os.path.join(c, trace)
            trace = helper._load_groundtruth_trace_by_path(trace_path)

            output_file = os.path.join(trace_path, "agg_plot.png")
            print(f"{c}, {trace_path}, {episode}, {output_file}")
            e.submit(
                plot_single_trace,
                epi=episode,
                category=c,
                task_description=task_description,
                task_trace=trace,
                output_file=output_file,
            )

    plt.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        plot_all()
    else:
        for item in sys.argv[1:]:
            plot_by_folder(item)
