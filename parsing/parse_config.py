# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parse_config.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cel-hajj <cel-hajj@student.s19.be>        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/02 07:38:49 by cel-hajj        #+#    #+#               #
#  Updated: 2026/03/02 13:54:32 by cel-hajj        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, Dict, List, Union
from .parse_utils import raise_error


def validate_concurrency(extracted_data: Dict[str, Any],
                         mandatory_keys: List[str],
                         optional_keys: List[str]) -> bool:
    if (not all(key in extracted_data for key in mandatory_keys) or
            extracted_data["ENTRY"] == extracted_data["EXIT"]):
        return False
    elif (extracted_data["ENTRY"][0] >= extracted_data["WIDTH"] or
          extracted_data["ENTRY"][1] >= extracted_data["HEIGHT"]):
        return False
    elif (extracted_data["EXIT"][0] >= extracted_data["WIDTH"] or
          extracted_data["EXIT"][1] >= extracted_data["HEIGHT"]):
        return False
    return True


def validate_and_format_data(key: str, data: Any) -> List[Any]:
    """
    """
    data_requirements = {
        "WIDTH": [lambda v: 20 <= int(v) <= 200, lambda t: int(t)],
        "HEIGHT": [lambda v: 20 <= int(v) <= 200, lambda t: int(t)],
        "ENTRY": [lambda v: (parts := v.split(",")) and len(parts) == 2
                  and all(0 <= int(p) for p in parts),
                  lambda t: (int(t.split(',')[0]), int(t.split(',')[1]))],
        "EXIT": [lambda v: (parts := v.split(",")) and len(parts) == 2
                 and all(0 <= int(p) for p in parts),
                 lambda t: (int(t.split(',')[0]), int(t.split(',')[1]))],
        "OUTPUT_FILE": [lambda v: len(v.strip()) > 0, lambda t: t],
        "PERFECT": [lambda v: v == "True" or v == "False",
                    lambda t: t == "True"],
        "SEED": [lambda v: 0 <= int(v) <= 200, lambda t: int(t)],
        "ALGORITHM": [lambda v: v == "Kruskal" or v == "Backtracking",
                      lambda t: t]
    }
    try:
        is_valid = data_requirements[key][0](data)
        if is_valid:
            return [True, data_requirements[key][1](data)]
        else:
            return [False]
    except ValueError:
        return [False]


def validate_and_extract_config(cf_data: List[str]) -> Union[Dict[str, Any],
                                                             None]:
    """
    """
    mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                      "PERFECT"]
    optional_keys = ["SEED", "ALGORITHM"]
    extracted_data = {"SEED": None, "ALGORITHM": None}

    for data in cf_data:
        splitted_data = data.split("=", 1)
        if len(splitted_data) != 2:
            return raise_error("tyooooope", "msg")
        elif not splitted_data[0] in mandatory_keys + optional_keys:
            return raise_error("tyzzzzzpe", "msg")
        else:
            valid_data = validate_and_format_data(splitted_data[0],
                                                  splitted_data[1])
            if valid_data[0]:
                extracted_data[splitted_data[0]] = valid_data[1]
            else:
                return raise_error("tyaaaape", "msg")
    if not validate_concurrency(extracted_data, mandatory_keys, optional_keys):
        return raise_error("type", "msg")
    return extracted_data


def parse_config(argc: int, argv: List[Any]) -> Union[Dict[str, Any], None]:
    """
    """
    if argc != 2:
        return raise_error("type", "msg")
    config_file = argv[1]
    try:
        with open(config_file) as cf:
            stripped_cf_data = list(map(lambda ln: ln.strip(),
                                    cf.readlines()))
            final_cf_data = list(filter(lambda ln: len(ln) > 0
                                        and not ln.startswith("#"),
                                        stripped_cf_data))
            return validate_and_extract_config(final_cf_data)
    except (FileNotFoundError, PermissionError):
        return raise_error("type", "msg")
