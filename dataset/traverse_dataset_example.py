from typing import List

from evaluator.task_trace import (
    DatasetHelper,
    TaskTrace,
    get_all_actions,
    get_all_screenshot_paths,
    get_all_vh_paths,
)

helper = DatasetHelper(
    epi_metadata_path="llamatouch_task_metadata.tsv",
    gr_dataset_path="llamatouch_dataset_0521"
)

episodes: List[str] = helper.get_all_episodes()

# only print first 10 tasks
for epi_id in episodes[:10]:
    task_description: str = helper.get_task_description_by_episode(epi_id)
    print(task_description)

    trace: TaskTrace = helper.load_groundtruth_trace_by_episode(epi_id)
    screenshots = get_all_screenshot_paths(trace)
    vhs = get_all_vh_paths(trace)
    actions = get_all_actions(trace)

    print(screenshots)
    print(vhs)
    print(actions)