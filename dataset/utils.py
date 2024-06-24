import re
from typing import List, Tuple


def extract_ess_from_file(ess_path: str) -> List[Tuple[str, str]]:
    ret: List[Tuple[str, str]] = []
    for line in open(ess_path):
        line = line.strip()
        ess = line.split("|")
        if line == "" or len(ess) == 0:
            continue
        for item in ess:
            match = re.search(r"(?P<keyword>\w+)<(?P<content>.+)>", item)
            if match:
                keyword: str = match.group("keyword")
                content: str = match.group("content")
                ret.append((keyword, content))
    return ret