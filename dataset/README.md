## Download

This dataset can be downloaded from the [OneDrive link](https://bupteducn-my.sharepoint.com/:u:/g/personal/li_zhang_bupt_edu_cn/EQggNRdjPXBDoWZ7wiMWXrkBAESYZYqciwtbaKmoYXkZ7g?e=muvel0).

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


## How to use

TODO: show how to use the [LlamaTouch Evaluator](https://github.com/LlamaTouch/Evaluator) module to access each episode in the dataset.

## Utils

A sequence of scripts for processing the recorded UI interaction trace:

1. `rename_tracedir.py`: convert timestamp-based captured traces to *0.png, 0.xml, 1.png, 1.xml, ...*

2. `gen_uijson.py`: filter important UI nodes from xml file and generate a json file for drawling bounding boxes; output file: *0.json, 1.json, ...*

3. `draw_bound.py`: draw bounding boxes according to generated json file using `gen_uijson.py`; output file: *0_drawed.png, 1_drawed.png, ...*

Utilization scripts to enhance the dataset:

- `gr_vis.py`: Plot aggregate figures for each ground-truth trace; this script requires the [LlamaTouch Evaluator](https://github.com/LlamaTouch/Evaluator) module.

