import re
import json


def get_match(regex, s):
    res = re.match(regex, s)
    if res is None:
        raise ValueError()
    return res.groups()


printj = lambda x: print(json.dumps(x, indent=4, default=str))
