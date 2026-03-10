# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parse_config.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cel-hajj <cel-hajj@student.s19.be>        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/02 07:38:49 by cel-hajj        #+#    #+#               #
#  Updated: 2026/03/04 12:07:21 by cel-hajj        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""
TODO
"""
from typing import Any, Dict, List, Union, Tuple
from .parse_utils import raise_error


def validate_concurrency(extracted_data: Dict[str, Any],
                         mandatory_keys: List[str]) -> Tuple[bool, str]:
    """
    TODO
    """
    # Checks whether all of the mandatory key have a value and if
    # the coordinates at ENTRY are different from the coordinates at EXIT.
    if (not all(key in extracted_data for key in mandatory_keys) or
            extracted_data["ENTRY"] == extracted_data["EXIT"]):
        return (False, "Not all mandatory keys are present in the input data, \
or the ENTRY coordinates are identical to the EXIT coordinates. ENTRY and \
EXIT must be distinct.")

    # Checks whether ENTRY and EXIT are in the bounds of WIDTH and HEIGHT.
    elif (extracted_data["ENTRY"][0] >= extracted_data["WIDTH"] or
          extracted_data["ENTRY"][1] >= extracted_data["HEIGHT"]):
        return (False, "The ENTRY coordinates are outside the allowed grid \
boundaries. Both ENTRY x and y must be less than WIDTH and HEIGHT \
respectively.")
    elif (extracted_data["EXIT"][0] >= extracted_data["WIDTH"] or
          extracted_data["EXIT"][1] >= extracted_data["HEIGHT"]):
        return (False, "The EXIT coordinates are outside the allowed grid \
boundaries. Both EXIT x and y must be less than WIDTH and HEIGHT \
respectively.")

    # Imposes bounds if the user chooses the Backtracking algorithm to avoid
    # maximum recursion depth.
    elif (extracted_data["ALGORITHM"] == "Backtracking" and
          (extracted_data["WIDTH"] > 40 or extracted_data["HEIGHT"] > 40)):
        return (False, "The Backtracking algorithm has been selected, but the \
grid size is too large. To prevent maximum recursion depth errors, WIDTH and \
HEIGHT must each be 40 or less.")
    return (True, "")


def validate_and_format_data(key: str, data: Any) -> Tuple[bool, Any]:
    """
    TODO
    """
    data_requirements = {
        # This dictionary represents the main data checker. Each entry is
        # composed of a verifier function (Index 0) that verifies if the data
        # passed is valid and a transform function (Index 1) that will
        # transform the data from string to it's attended type.
        "WIDTH": [lambda v: 20 <= int(v) <= 200, lambda t: map(int, t)],
        "HEIGHT": [lambda v: 20 <= int(v) <= 200, lambda t: map(int, t)],
        "ENTRY": [lambda v: (parts := v.split(",")) and len(parts) == 2
                  and all(0 <= int(p) for p in parts),
                  lambda t: (int(t.split(',')[0]), int(t.split(',')[1]))],
        "EXIT": [lambda v: (parts := v.split(",")) and len(parts) == 2
                 and all(0 <= int(p) for p in parts),
                 lambda t: (int(t.split(',')[0]), int(t.split(',')[1]))],
        "OUTPUT_FILE": [lambda v: len(v.strip()) > 0, lambda t: t],
        "PERFECT": [lambda v: v == "True" or v == "False",
                    lambda t: t == "True"],
        "SEED": [lambda v: 0 <= int(v) <= 200, lambda t: map(int, t)],
        "ALGORITHM": [lambda v: v == "Kruskal" or v == "Backtracking",
                      lambda t: t]
    }
    try:
        # Calls the verifier function with the data given as an argument.
        is_valid = data_requirements[key][0](data)
        if is_valid:
            return (True, data_requirements[key][1](data))
        else:
            return (False, None)
    except ValueError:
        return (False, None)


def validate_and_extract_config(cf_data: List[str]) -> Union[Dict[str, Any],
                                                             int]:
    """
    TODO
    """
    mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                      "PERFECT"]
    optional_keys = ["SEED", "ALGORITHM"]

    # Dictionary used for error handling.
    validation_conditions = {
        "WIDTH": "Integer between 20 and 200 (inclusive)",
        "HEIGHT": "Integer between 20 and 200 (inclusive)",
        "ENTRY": "Two non-negative integers separated by a comma (x,y), e.g., \
0,5",
        "EXIT": "Two non-negative integers separated by a comma (x,y), e.g., \
19,10",
        "OUTPUT_FILE": "Non-empty string specifying the output file name",
        "PERFECT": "Boolean: True or False",
        "SEED": "Integer between 0 and 200 (inclusive)",
        "ALGORITHM": "Either 'Kruskal' or 'Backtracking"
    }

    # Default values for the optional keys
    extracted_data = {"SEED": 42, "ALGORITHM": "Kruskal"}

    for data in cf_data:
        # Split each line in the file at the first '=' present.
        splitted_data = data.split("=", 1)
        if len(splitted_data) != 2:
            return raise_error("FORMAT ERROR", "Please make sure to respect \
the required file format: 'ARGUMENT'='VALUE'.")

        key = splitted_data[0].strip()
        value = splitted_data[1].strip()
        # Checks whether the parameter is valid and not forbidden.
        if key not in mandatory_keys + optional_keys:
            return raise_error("RULE ERROR", f"Non defined argument found: \
'{key}'. Please make sure not to include forbidden arguments and \
to only include mandatory arguments and optional arguments if needed. \
(WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT, SEED, ALGORITHM)")
        else:
            # Validates the data by verifying bounds and transforming it
            # to the appropriate type.
            valid_data = validate_and_format_data(key, value)
            if valid_data[0]:
                # Add entry to the dictionary if the data is valid with
                # the key as the name of the parameter and as the data the
                # formatted data from validate_and_format_data().
                extracted_data[key] = valid_data[1]
            else:
                return raise_error("DATA ERROR", f"""The value provided to \
'{key}' is not valid! You provided: '{value}'. This does not follow the \
rule linked to {key}: {validation_conditions[f'{key}']}""")

    # After validating and transforming every data, this function checks
    # whether the different parameters are bounded and not overlaping.
    data_bounded = validate_concurrency(extracted_data, mandatory_keys)
    if not data_bounded[0]:
        return raise_error("BOUND ERROR", data_bounded[1])
    return extracted_data


def parse_config(argc: int, argv: List[Any]) -> Union[Dict[str, Any], int]:
    """
    TODO
    """
    if argc != 2:
        return raise_error("ARGUMENTS ERROR", """The arguments provided to \
the program are not valid.

Please make sure to run the program with only one argument and as follows,
$> python3 a_maze_ing.py '<file name>'""")

    # Gets the argument given in first position.
    config_file = argv[1]
    try:
        # 'cf' represents 'Config File'.
        with open(config_file, 'r', encoding="utf-8") as cf:
            # This applies .strip() on all of the lines of the file. This
            # will remove white spaces on the left and right of each string.
            stripped_cf_data = list(map(lambda ln: ln.strip(),
                                    cf.readlines()))
            # THis filters the list of lines and removes lines starting with #
            # to avoid comments and lines that are empty.
            final_cf_data = list(filter(lambda ln: len(ln) > 0
                                        and not ln.startswith("#"),
                                        stripped_cf_data))
            return validate_and_extract_config(final_cf_data)
    except OSError:
        return raise_error("FILE ERROR", f"""The file name you provided: \
'{config_file}' could not be processed.
Please make sure to provide a valid file name.""")
