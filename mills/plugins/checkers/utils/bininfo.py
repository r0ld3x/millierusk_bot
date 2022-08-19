
from mills.plugins import BINS_DICT


def get_bin_info(bin_to_find: int):
    if str(bin_to_find[:6]) in BINS_DICT:
        xx = BINS_DICT[str(bin_to_find[:6])]
        return xx if not xx['prepaid'] else False
    else:
        return False

def get_bin_info_all(bin_to_find):
    
    if bin_to_find in BINS_DICT:
        xx = BINS_DICT[bin_to_find]
        return xx
    else:
        return False