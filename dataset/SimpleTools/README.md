## Poster: Efficient and Accurate Mobile Task Automation through Learning from Code
This table contains the tasks used in the paper "Poster: Efficient and Accurate Mobile Task Automation through Learning from Code".

## Simple Mobile Tools
The mobile agent prototype is evaluated on 5 real-world open-source applications which are [Simple Mobile Tools](https://github.com/SimpleMobileTools).

We generate 22 simple tasks for evaluation, calculating the baseline completion steps by manual operations.

| App      | Task Description                                            | Baseline Steps | Our Method Steps | IsCompletion          | Steps Decrease Rate |
| -------- | ----------------------------------------------------------- | -------------- | ---------------- | --------------------- | ------------------- |
| sms      | clear recycle bin                                           | 3              | 1                | True                  | 66.67%              |
| sms      | open setting                                                | 2              | 1                | True                  | 50%                 |
| sms      | open nearliest conversation                                 | 2              | 1                | False                 | 50%                 |
| sms      | tell zhangli i will not eat lunch today                     | 2              | 1                | True                  | 50%                 |
| sms      | list archived conversation                                  | 3              | 1                | True                  | 66.67%              |
| Calendar | open setting                                                | 2              | 1                | True                  | 50%                 |
| Calendar | open calendar                                               | 1              | 1                | True                  | 0%                  |
| Calendar | tell me i will eat lunch tommorrow 11:30 am                 | 3              | 1                | False                 | 66.67%              |
| Calendar | create a task: i will eat lunch tommorrow 11:30 am          | 3              | 1                | False                 | 66.67%              |
| gallery  | open setting                                                | 3              | 1                | True                  | 66.67%              |
| gallery  | Open gallery                                                | 1              | 1                | True                  | 0%                  |
| gallery  | open photo list                                             | 1              | 1                | True                  | 0%                  |
| gallery  | open video list                                             | 7              | 1                | False                 | 85.71%              |
| gallery  | search screenshot                                           | 2              | 1                | False                 | 50%                 |
| Contacts | open setting                                                | 3              | 1                | True                  | 66.67%              |
| Contacts | open contacts                                               | 1              | 1                | True                  | 0%                  |
| Contacts | edit a contact, name is zhangli, phone number is 1234567890 | 2              | 1                | False                 | 50%                 |
| Contacts | add a group, name is test                                   | 3              | 1                | False                 | 66.67%              |
| Notes    | open setting                                                | 3              | 1                | True                  | 66.67%              |
| Notes    | open notes                                                  | 1              | 1                | True                  | 0%                  |
| Notes    | add I will eat lunch at xxx street at 12:00 to notes        | 1              | 1                | False                 | 0%                  |
| Notes    | what i remember yesterday                                   | 2              | 2                | False                 | 0%                  |
| Total    |                                                             | 51             | 23               | 13 (Completion Count) | 54.90%              |
