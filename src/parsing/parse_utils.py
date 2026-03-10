# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parse_utils.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cel-hajj <cel-hajj@student.s19.be>        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/02 10:06:46 by cel-hajj        #+#    #+#               #
#  Updated: 2026/03/10 23:42:46 by cel-hajj        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

def raise_error(error_type: str, msg: str) -> int:
    """
    Prints a formatted error message to the console and returns an error code.

    Args:
        error_type (str): The category or specific type of the error
        (e.g., 'FILE ERROR').
        msg (str): The detailed explanation of the error to display to the
        user.

    Returns:
        int: Always returns -1 to indicate that a failure occurred.
    """
    print(f"[{error_type}]: {msg}")
    return -1
