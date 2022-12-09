from fractions import Fraction

# Define some methods to help with common tasks.
def flatten_list(list_of_lists, flat_list=[]):
    if flat_list == []:
        return flat_list
    else:
        for item in list_of_lists:
            if type(item) == list:
                flatten_list(item)
            else:
                flat_list.append(item)

        return flat_list


def rgb_to_hex(rgb):
    hex = ""
    for value in rgb:
        hex += "%02x" + str(value)
    return hex


def calculate_aspect_ratio(width, height):
    ratio_str = str(Fraction(width, height)).split("/")
    w = int(ratio_str[0])
    h = int(ratio_str[1])
    return w, h
