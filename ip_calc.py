'''
This module contains functions.
'''
def get_ip_from_raw_address(raw_address: str) -> str:
    """
    This function gets raw address and returns IP.
    >>> get_ip_from_raw_address("192.168.1.65/28")
    '192.168.1.65'
    """
    if func_checker(raw_address) == None:
        return None
    prefix = raw_address.split("/")[1]
    return raw_address[:-(len(prefix)+1)]

def get_network_address_from_raw_address(raw_address: str) -> str:
    """
    This function returns network address based on
    raw_address and mask.
    >>> get_network_address_from_raw_address("192.168.1.65/28")
    '192.168.1.64'
    """
    if func_checker(raw_address) == None:
        return None
    binary = get_binary_mask_from_raw_address(raw_address)
    address = raw_address.split("/")[0]
    lst = []
    bina = binary.split(".")
    adr = address.split(".")
    for i in range(4):
        lst.append(str(int(adr[i]) & int(bina[i], 2)))
    return ".".join(lst)

def get_broadcast_address_from_raw_address(raw_address: str) -> str:
    """
    This function returns IP of broadcast based on
    raw_address.
    >>> get_broadcast_address_from_raw_address("192.168.1.65/28")
    '192.168.1.79'
    """
    if func_checker(raw_address) == None:
        return None
    binary = get_binary_mask_from_raw_address(raw_address)
    address = raw_address.split("/")[0]
    lst = list(binary)
    for i in range(len(lst)):
        if lst[i] == "1":
            lst[i] = "0"
        elif lst[i] == "0":
            lst[i] = "1"
    inv_lst = "".join(lst).split(".")
    lst_0 = []
    adr = address.split(".")
    for i in range(4):
        lst_0.append(str(int(adr[i]) | int(inv_lst[i], 2)))
    return ".".join(lst_0)

def get_binary_mask_from_raw_address(raw_address: str) -> str:
    """
    This function returns binary mask of
    raw_address.
    >>> get_binary_mask_from_raw_address("192.168.1.65/28")
    '11111111.11111111.11111111.11110000'
    """
    if func_checker(raw_address) == None:
        return None
    prefix = int(raw_address.split("/")[1])
    zeros = 32 - prefix
    binary = "0"*zeros
    output = binary.rjust(32, "1")
    return output[:8]+"."+output[8:16]+"\
."+output[16:24]+"."+output[24:]

def get_first_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    This function returns a first usable ip address
    based on raw_address.
    >>> get_first_usable_ip_address_from_raw_address("192.168.1.65/28")
    '192.168.1.65'
    """
    if func_checker(raw_address) == None:
        return None
    net_id = get_network_address_from_raw_address(raw_address)
    lst = net_id.split(".")
    lst[-1] = str(int(lst[-1]) + 1)
    return ".".join(lst)

def get_penultimate_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    This function returns pre-last ip address
    based on raw_address.
    >>> get_penultimate_usable_ip_address_from_raw_address("192.168.1.65/28")
    '192.168.1.77'
    """
    if func_checker(raw_address) == None:
        return None
    br_id = get_broadcast_address_from_raw_address(raw_address)
    lst = br_id.split(".")
    lst[-1] = str(int(lst[-1]) - 2)
    return ".".join(lst)

def get_number_of_usable_hosts_from_raw_address(raw_address: str) -> str:
    """
    This function returns amount of possible local
    ip addresses.
    >>> get_number_of_usable_hosts_from_raw_address("192.168.1.65/28")
    14
    """
    if func_checker(raw_address) == None:
        return None
    prefix = int(raw_address.split("/")[1])
    number = 2**(32-prefix) - 2
    return number

def get_ip_class_from_raw_address(raw_address: str) -> str:
    """
    This function returns an ip class
    based on raw_address.
    >>> get_ip_class_from_raw_address("192.168.1.65/28")
    'C'
    """
    if func_checker(raw_address) == None:
        return None
    first = int(get_ip_from_raw_address(raw_address).split(".")[0])
    if first <128:
        return "A"
    elif first <192:
        return "B"
    elif first <224:
        return "C"
    elif first <240:
        return "D"
    return "E"

def check_private_ip_address_from_raw_address(raw_address: str) -> bool:
    """
    This function returns a bool
    based on is this ip address private or not.
    >>> check_private_ip_address_from_raw_address("192.168.1.65/28")
    True
    """
    if func_checker(raw_address) == None:
        return None
    ipx = get_ip_from_raw_address(raw_address).split(".")
    if (ipx[0] == "10" or (ipx[0] == "172" and ipx[1] == "16")
    or (ipx[0] == "172" and ipx[1] == "31")
    or (ipx[0] == "192" and ipx[1] == "168")):
        return True
    return False

def func_checker(raw_address: str) -> str:
    """
    This function checks if given string is
    a normal type of ip address with prefix.
    If it isn't, returns None.
    >>> func_checker("192.168.1.65/28")
    True
    """
    if  not isinstance(raw_address, str):
        return None
    elif len(raw_address) > 18 or len(raw_address) < 9:
        return None
    elif (list(raw_address).count(".") != 3
    or list(raw_address).count("/") != 1):
        return None
    lst = raw_address.split(".")
    prefix = lst[-1].split("/")[1]
    if len(prefix) == 0 or len(prefix) > 2 or int(prefix) > 30:
        return None
    try:
        lst[-1] = prefix
        for i in range(len(lst)):
            lst[i] = int(lst[i])
            if lst[i] < 0 or lst[i] > 255:
                return None
    except ValueError:
        return None
    return True
