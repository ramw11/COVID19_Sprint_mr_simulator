
import json
import jsonpickle
from datetime import date
import random
import csv
import requests

def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__ }
    d.update(vars(obj))
    return d

def serialize_test(obj):
    if isinstance(obj,date):
        serial = obj.isoformat()
        return serial
    return obj.__dict__

def get_clampt_gauss_namber(minval,maxval,avg,stddev):
    num = min(maxval, max(minval, random.gauss(avg, stddev)))
    return num

def get_gauss_namber(minval,maxval,avg,stddev):
    num = random.gauss(avg, stddev)
    return num

def get_guid():
    response = requests.get('http://52.16.82.127:3000/new_id')
    return response.json()['new_id']


if __name__ == '__main__':
    nums = []
    for i in range(1000):
        nums.append(get_gauss_namber(50, 120, 80, 10))

    print (nums)
    # Assuming res is a flat list
    with open('d:\weights1.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in nums:
            writer.writerow([val])
            # with open('d:\weights.txt', mode='wt', encoding='utf-8') as myfile:
    #     myfile.write('\n'.join(str(nums)))

