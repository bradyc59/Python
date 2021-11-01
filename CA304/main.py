from fastapi import FastAPI # import so can use fastAPI
from pydantic import BaseModel #import so can be used for input through classes

description = """

## Ipcalc

You can input an **Ip address** and it will return the **class**, **number of networks**, **number of host bits**, **first address** and **last address** of that class.
\nFor example: 
\n**Input:** \n
{
  \n"address": "192.80.50.1"
}
\n**Output:** \n
{
  \n"address": "192.80.50.1",\n
  "Class": "C",\n
  "num_networks": "2097152",\n
  "host_bits": "256",\n
  "first_address": "192.0.0.0",\n
  "last_address": "223.255.255.255"\n
}


## Subnetcalc

You take in an **Ip address** and a **mask** and it will return the **cidr notation of the ip**, **number of subnets**, **addressable hosts per subnets**, **valid subnets**, **broadcast address**, **first address** and **last address**.
\n For example:
\n **Input: ** \n
{
	\n"address": "192.168.10.0",\n
	"mask": "255.255.255.192"\n
}
\n**Output:** \n
{
  \n"address": "192.168.10.0",\n
  "mask": "255.255.255.192",\n
  "address_cidr": "192.168.10.0/26",\n
  "num_subnets": 4,\n
  "Addressable hosts per subnet:": 62,\n
  "valid_subnets": [
    "192.168.10.0",
    "192.168.10.64",
    "192.168.10.128",
    "192.168.10.192"
  ],\n
  "broadcast_address": [
    "192.168.10.63",
    "192.168.10.127",
    "192.168.10.191",
    "192.168.10.255"
  ],\n
  "first_address": [
    "192.168.10.1",
    "192.168.10.65",
    "192.168.10.129",
    "192.168.10.193"
  ],\n
  "last_address": [
    "192.168.10.62",
    "192.168.10.126",
    "192.168.10.190",
    "192.168.10.254"
  ]\n
}

## Supernetcalc

You can take in a list of **Ip adressess** and it will return the **Ip address with cidr notation** and the **mask of the ip**.

\n For example:
\n**Input:** \n
{
    \n"address":["205.100.0.0","205.100.1.0","205.100.2.0","205.100.3.0"]\n
}
\n**Output:** \n
{
\n"addresses":["205.100.0.0","205.100.1.0","205.100.2.0","205.100.3.0"]\n
  "Address": "205.100.0.0/22",\n
  "Mask": "255.255.252.0"\n
}
"""

app = FastAPI(    title="Conor's Ip Caluclator",
    description=description,
    version="0.0.1",
)


classes={ # a dictionary given to us by Michael to get a certain classes network and host bits
    'A':{

        'network_bits':7,

        'host_bits':24

    },

    'B':{

        'network_bits':14,

        'host_bits':16

    },

    'C':{

        'network_bits':21,

        'host_bits':8

    },

    'D':{

        'network_bits':'N/A',

        'host_bits':'N/A'

    },

    'E':{

        'network_bits':'N/A',

        'host_bits':'N/A'

    },

}

class IP(BaseModel): # using the BaseModel in class so I can input an ip address
    address: str


def get_class_A(ip_add: IP): # gets all the stats of a class A ip address
    ip_dict = ip_add.dict() # creating a dictionary so i can add all stats to the dictionary at once
    ip_dict.update({"Class": "A", "num_networks" : (str(2 ** (classes["A"]["network_bits"]))), "host_bits": (str(2 ** (classes["A"]["host_bits"]))), "first_address": "0.0.0.0","last_address": "127.255.255.255"})
    return ip_dict # returning all stats of ip address that was added to dictionary

def get_class_B(ip_add: IP): # gets all the stats of a class B ip address
    ip_dict = ip_add.dict()
    ip_dict.update({"Class": "B", "num_networks" : (str(2 ** (classes["B"]["network_bits"]))), "host_bits": (str(2 ** (classes["B"]["host_bits"]))), "first_address": "128.0.0.0","last_address": "191.255.255.255"})
    return ip_dict

def get_class_C(ip_add: IP): # gets all the stats of a class C ip address
    ip_dict = ip_add.dict()
    ip_dict.update({"Class": "C", "num_networks" : (str(2 ** (classes["C"]["network_bits"]))), "host_bits": (str(2 ** (classes["C"]["host_bits"]))), "first_address": "192.0.0.0","last_address": "223.255.255.255"})
    return ip_dict

def get_class_D(ip_add: IP): # gets all the stats of a class D ip address
    ip_dict = ip_add.dict()
    ip_dict.update({"Class": "D", "num_networks" : "N/A", "host_bits": "N/A", "first_address": "224.0.0.0", "last_address": "239.255.255.255"})
    return ip_dict

def get_class_E(ip_add: IP): # gets all the stats of a class E ip address
    ip_dict = ip_add.dict()
    ip_dict.update({"Class": "E", "num_networks" : "N/A", "host_bits": "N/A", "first_address": "240.0.0.0", "last_address": "255.255.255.255"})
    return ip_dict

@app.post('/ipcalc') # having post request so i can input data through FastAPI
def ipcalc(ip_add: IP):
    new_ip_add = ip_add.address.split(".") # splitting ip address at each bit
    first_bits = int(new_ip_add[0]) # getting the first bit so we can determine what class the ip address is
    if first_bits <= 127: # class A address
        return get_class_A(ip_add) # calling the function if its class A
    elif first_bits >= 128 and first_bits <= 191: # class B address
        return get_class_B(ip_add) # calling the function if its class B
    elif first_bits >= 192 and first_bits <= 223: # class C address
        return get_class_C(ip_add) # calling the function if its class C
    elif first_bits >= 224 and first_bits <= 239: # class D address
        return get_class_D(ip_add) # calling the function if its class D
    elif first_bits >= 240 and first_bits <= 255: # class E address
        return get_class_E(ip_add) # calling the function if its class D


class Subnet(BaseModel):
    address: str
    mask: str

def find_unmasked_bits(i, bin_list): # iterating through the ip as binary to see how many 0's there are in it
    unmasked = 0
    while i < 4:
        for num in bin_list[i]:
            if int(num) == 0:
                unmasked += 1
        i += 1
    return unmasked

def addressable_hosts(ip_add): # finding all addressable hosts per ip
    unmasked = 0
    bin = dec_to_binary(ip_add.mask)
    if ip_add.mask.split(".")[2] == "255": # class C
        i = 0
        unmasked = find_unmasked_bits(i, bin)
    elif ip_add.mask.split(".")[2] != "255": # class B
        i = 2
        unmasked = find_unmasked_bits(i, bin)

    host = (2 ** unmasked - 2) # subtract two for network and broadcast addresses
    return host


def cidr_not(ip_add): # finding the cidr notation for the ip
    binary = dec_to_binary(ip_add.mask)
    bin_string = "".join(binary)
    network_bits = 0
    for n in bin_string: # counting through to see how many 1's there are in the ip
        if int(n) == 1:
            network_bits += 1
    return (str(ip_add.address)+"/"+str(network_bits)) # returning the ip address alongside the cidr notation with it

def num_of_subnets(ip_add): #finding the number of subnets for the mask
    i = 0
    binary_list = dec_to_binary(ip_add.mask)
    subnet_bits = 0
    while i < 4:
        for num in binary_list[3]: # seeing how many 1's there are in the mask in the last bit
            if int(num) == 1:
                subnet_bits += 1
            i += 1

    return 2 ** subnet_bits


def valid_subnets(ip_add):
    subnets = [] # empty list which will fill with valid subnets
    index_final_bit = ip_add.address.rindex(".") #gets the index of the last set of bits
    bits = ip_add.mask.split(".")
    blocksize = 256 - int(bits[3])
    for i in range(0, int(bits[3]) + 1, blocksize):
        subnets.append(ip_add.address[: index_final_bit] + "." + str(i)) # append each valid subnet to a list

    return subnets

def broadcast_address(ip_add):
    broadcast_add = []
    bits = ip_add.mask.split(".")
    blocksize = 256 - int(bits[3])
    index_final_bit = ip_add.address.rindex(".")
    for i in range(blocksize, int(bits[3]) + 1, blocksize):
        broadcast_add.append(ip_add.address[: index_final_bit] + "." + str(i - 1))
    broadcast_add.append(ip_add.address[: index_final_bit] + "." + str(255)) # broadcast address of last subnet is always 255

    return broadcast_add

def first_address(ip_add):
    i = 0
    first_add = []
    subnets = valid_subnets(ip_add)
    while i < len(subnets):
        index_subnet = ip_add.address.rindex(".") + 1 #get the index of the subnet
        subnet = subnets[i][index_subnet:] # store the start of each valid host for subnet
        subnet = int(subnet) + 1 # to get first value in valid hosts
        first_add.append(ip_add.address[:index_subnet] + str(subnet)) # joining the valid host to original ip
        i += 1
    return first_add

def last_address(ip_add):
    i = 0
    last_add =[]
    broadcast_add = broadcast_address(ip_add)
    while i < len(broadcast_add):
        index_broadcast = ip_add.address.rindex(".") + 1
        broadcast = broadcast_add[i][index_broadcast:]
        broadcast = int(broadcast) - 1 # to get last value in valid hosts
        last_add.append(ip_add.address[:index_broadcast] + str(broadcast))
        i += 1
    return last_add


@app.post('/subnet')
def subnetcalc(ip_add: Subnet): # updating dictionary with all the outputs from each function
    ip_dict = ip_add.dict()
    if ip_add.address:
        ip_dict.update({"address_cidr": cidr_not(ip_add)})
        ip_dict.update({"num_subnets": num_of_subnets(ip_add)})
        ip_dict.update({"Addressable hosts per subnet:": addressable_hosts(ip_add)})
        ip_dict.update({"valid_subnets": valid_subnets(ip_add)})
        ip_dict.update({"broadcast_address": broadcast_address(ip_add)})
        ip_dict.update({"first_address": first_address(ip_add)})
        ip_dict.update({"last_address": last_address(ip_add)})

    return ip_dict

class Supernet(BaseModel):
    address : list # allows me to input a list of ip addresses


def get_ip_add(ip_add):
    binary_list = []
    for ip in ip_add.address: # for each ip address in the list
        bin = dec_to_binary(ip) #converting to binary
        bin_string = "".join(bin)
        binary_list.append(bin_string) #adding the binary list to the list as one string value

    i = 0
    j = 1
    count = 0

    while i < len(binary_list):
        if binary_list[i][count] == binary_list[j][count]:
            count += 1
        else:
            break

    common_prefix = binary_list[0][0: count-1]

    common_prefix_list = []

    for bit in common_prefix:
        common_prefix_list.append("1") # add a one to the list each time its encounter in the list
    return ip_add.address[0]+"/"+str(len(common_prefix_list)) # find the length of the list of 1's to find the cidr notation

def get_mask_add(ip_add):
    '''
    repeating the same proccess for the ones in order to count 0's alongside with them to
    return the mask
    '''
    binary_list = []
    for network in ip_add.address:
        bin = dec_to_binary(network)
        bin_string = "".join(bin)
        binary_list.append(bin_string)

    i = 0
    j = 1
    count = 0

    while i < len(binary_list):
        if binary_list[i][count] == binary_list[j][count]:
            count += 1
        else:
            break

    common_prefix = binary_list[0][0: count - 1]
    len_rest_of_network = len(binary_list[0][count-1:])

    common_prefix_list = []

    for bit in common_prefix:
        common_prefix_list.append("1")

    for i in range(0, len_rest_of_network, 1):
        common_prefix_list.append("0") # finding all 0's and adding them to the common_prefix list
    net_mask = "".join(common_prefix_list)

    net_mask_list = []
    net_mask_list.append(net_mask[0:8]) #splitting the list so i can get each bit in the ip address as binary and appending them to a list
    net_mask_list.append(net_mask[8:16])
    net_mask_list.append(net_mask[16:24])
    net_mask_list.append(net_mask[24:32])
    return to_dec(net_mask_list) # converting each bit back to an ip address

@app.post('/supernet')
def supernetcalc(ip_add: Supernet):
    ip_dict = ip_add.dict()
    if ip_add.address:
        ip_dict.update({"Address" : get_ip_add(ip_add)})
        ip_dict.update({"Mask" : get_mask_add(ip_add)})
    return ip_dict

'''
These are helper functions which allow me to convert a ip address to binary and vice versa
'''
def dec_to_binary(ip_add):
    new_ip_add = ip_add.split(".")
    return ['{0:08b}'.format(int(x)) for x in new_ip_add]

def to_dec(ip_add_list):
    return '.'.join([str(int(x, 2)) for x in ip_add_list])