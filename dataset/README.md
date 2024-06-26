## Download

This dataset can be downloaded from the [OneDrive link](https://bupteducn-my.sharepoint.com/:u:/g/personal/li_zhang_bupt_edu_cn/EQXjI1lpOw1Csod3H5w-4y4BcJGTETT5eiDXoo1fyCIhgA?e=80fLPp).

## Organization

Dataset structure:

```
groundtruth-traces
├── general
│  ├── trace_0
│  │  ├── 0.png
│  │  ├── 0_drawed.png
│  │  ├── 0.xml
│  │  ├── 0.vh
│  │  ├── 0.json
│  │  ├── 0.activity
│  │  ├── 1.png
│  │  ├── 1_drawed.png
│  │  ├── 1.xml
│  │  ├── 1.vh
│  │  ├── 1.json
│  │  ├── 1.activity
│  │  ├── 1.ess
│  │  ├── agg_plot.png
│  │  ├── eventStructs.txt
│  │  ├── instruction.txt
│  ├── trace_1
│  ├── trace_2
│  ├── ...
│  ├── trace_n
├── generated
├── googleapps
├── install
└── webshopping
```

Root folder:

- Task category: The ground-truth traces are divided into five distinct categories in the root folder: 
*general*, *googleapps*, *install*, and *webshopping* contain the tasks from [AITW](https://arxiv.org/abs/2307.10088); *generated* contains LlamaTouch's self-generated tasks.

Each category folder contains different ground-truth traces named *trace_[n]*, comprising the following files, sorted by index i starting from 0:

- *i*.png: Screenshot of the current UI
- *i*_drawed.png: Screenshot of the current UI with highlighted UI components using data in *i*.json
- *i*.xml: View hierarchy captured using the `adb uiautomator dump` command
- *i*.vh: Json-format view hierarchy captured with in-app AccessibilityService
- *i*.activity: Activity name of the foreground application in the current screen
- *i*.json: Simplified critical UI components with unique indices
- *i*.ess: Annotated essential states in the current screen; annotated indices correspond to indices in the file *i*.json
- eventStructs.txt: Action sequence to complete the task
- instruction.txt: Episode (a string uniquely representing the task) and task description
- agg_plot.png: A human-friendly and readable aggregate figure showing the sequence of screens and actions for completing the task


## How-to-use Guide

Users need to install the [LlamaTouch Evaluator](https://github.com/LlamaTouch/Evaluator) module first.

Refer to our example code [traverse_dataset_example.py](./traverse_dataset_example.py) to access episodes in the dataset. Users typically need to configure the task metadata path and dataset path as follows.

```python
helper = DatasetHelper(
    epi_metadata_path="/path/to/llamatouch_task_metadata.tsv",
    gr_dataset_path="/path/to/llamatouch_dataset"
)
```

The [LlamaTouch Evaluator](https://github.com/LlamaTouch/Evaluator?tab=readme-ov-file#using-the-dataset) module provides additional details about usage.

## Utilization Scripts

1. `gr_vis.py`: Plot aggregate figures for every ground-truth trace; this script requires the [LlamaTouch Evaluator](https:/github.com/LlamaTouch/Evaluator) module.

    ```
    # plot individual traces
    python3 gr_vis.py single /path/to/trace1 /path/to_trace2 ...

    # plot all traces
    python3 gr_vis.py all /path/to/dataset
    ```

2. `dataset_stats.py`: Calculate and show dataset statistics, including the number of actions, essential states, etc.

    ```
    python3 dataset_stats.py /path/to/dataset
    ```

3. `validate_metadata_dataset.py`: Validate the consistency of task descriptions between the task metadata file "llamatouch_task_metadata.tsv" and task descriptions stored "instructions.txt" in each trace folder.

    ```
    python3 dataset_stats.py llamatouch_task_metadata.tsv /path/to/dataset
    ```

## Utilization Scripts for Processing New Recorded Traces

A sequence of scripts for processing the recorded UI interaction traces.

1. `rename_tracedir.py`: Convert timestamp-based captured traces to indices-based traces.

2. `gen_uijson.py`: Filter important UI nodes from xml file and generate a json file for drawling bounding boxes.
    - Outputs: 0.json, 1.json, ...

3. `draw_bound.py`: Draw bounding boxes according to generated json file using `gen_uijson.py`.
    - Outputs: 0_drawed.png, 1_drawed.png, ...

4. `gr_vis.py`: See description in "Utilization scripts"

    ```
    python3 rename_tracedir.py [/path/to/trace_1] [/path/to/trace_2]

    python3 gen_uijson.py all [dataset_path]
    python3 gen_uijson.py single [/path/to/trace_1] [/path/to/trace_2] ...

    python3 draw_bound.py [/path/to/0.png] [/path/to/1.png] ...
    ```

