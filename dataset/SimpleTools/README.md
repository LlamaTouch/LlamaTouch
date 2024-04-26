## Poster: Efficient and Accurate Mobile Task Automation through Learning from Code
This table contains the tasks used in the paper "Poster: Efficient and Accurate Mobile Task Automation through Learning from Code".

## Simple Mobile Tools
The mobile agent prototype is evaluated on 5 real-world open-source applications which are [Simple Mobile Tools](https://github.com/SimpleMobileTools).

We generate 22 simple tasks for evaluation, calculating the baseline completion steps by manual operations.

| App      | Task Description                                            | Baseline Steps | Our Method Steps | IsCompletion          | Steps Decrease Rate |
| -------- | ----------------------------------------------------------- | -------------- | ---------------- | --------------------- | ------------------- |
| sms      | Clear the recycle bin                                       | 3              | 1                | True                  | 66.67%              |
| sms      | Open setting                                                | 2              | 1                | True                  | 50%                 |
| sms      | Open the nearest conversation                               | 2              | 1                | False                 | 50%                 |
| sms      | Tell li I will not eat lunch today                          | 2              | 1                | True                  | 50%                 |
| sms      | List archived conversations                                 | 3              | 1                | True                  | 66.67%              |
| Calendar | Open setting                                                | 2              | 1                | True                  | 50%                 |
| Calendar | Open calendar                                               | 1              | 1                | True                  | 0%                  |
| Calendar | Tell me I will eat lunch tomorrow 11:30 am                  | 3              | 1                | False                 | 66.67%              |
| Calendar | Create a task: I will eat lunch tomorrow 11:30 am           | 3              | 1                | False                 | 66.67%              |
| gallery  | Open setting                                                | 3              | 1                | True                  | 66.67%              |
| gallery  | open gallery                                                | 1              | 1                | True                  | 0%                  |
| gallery  | Open the photo list                                         | 1              | 1                | True                  | 0%                  |
| gallery  | Open the video list                                         | 7              | 1                | False                 | 85.71%              |
| gallery  | Search screenshots                                          | 2              | 1                | False                 | 50%                 |
| Contacts | Open setting                                                | 3              | 1                | True                  | 66.67%              |
| Contacts | Open contacts                                               | 1              | 1                | True                  | 0%                  |
| Contacts | Edit a contact named li, phone number is 1234567890         | 2              | 1                | False                 | 50%                 |
| Contacts | Add a group named test                                      | 3              | 1                | False                 | 66.67%              |
| Notes    | Open setting                                                | 3              | 1                | True                  | 66.67%              |
| Notes    | Open notes                                                  | 1              | 1                | True                  | 0%                  |
| Notes    | Add I will eat lunch at xxx street at 12:00 to notes        | 1              | 1                | False                 | 0%                  |
| Notes    | What did I remember yesterday                               | 2              | 2                | False                 | 0%                  |
| Total    |                                                             | 51             | 23               | 13 (Completion Count) | 54.90%              |
