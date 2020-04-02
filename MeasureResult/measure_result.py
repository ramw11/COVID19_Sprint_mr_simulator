# -*- coding: utf-8 -*-
"""
measure_result.py - define a data structure to hold medical measurement of the sensors

written by: Rami Warhaftig

Change Log:
26-03-2020 : creation
"""

import enum
import json
import requests
import uuid
import datetime
import random
import math


from MeasureResult import utilities

# Using enum class create enumerations
class SensorPos(str, enum.Enum):
    Left_Shoulder = 'Left_Shoulder'
    Right_Shoulder = 'Right_Shoulder'
    Chest = 'Chest'
    Back = 'back'

class PrimeryPriority:
    def __init__(self, pulse = random.randrange(60, 120),fev1 =random.randrange(30, 90),fvc = random.randrange(70, 90),\
                 tlc = random.uniform(4.0, 7.0),rv = random.uniform(0.5, 1.5),erv = 0,frc = 0,breath_rate = 12,\
                 wheezing = False,cough_presence_rate = 0):
        # proper 60 - 80 / min Pulse / min
        self.pulse = pulse
        # Forced Expiratory vol.per 1 sec L / sec
        self.fev1 = fev1
        # Forced vital capacity L / 10 sec
        self.fvc = fvc
        # Total lung capacity L
        self.tlc = tlc
        # Residual volume L
        self.rv = rv
        # Expiratory reserved volume 0.7 - 1.2 L
        self.erv = erv
        # Functional residual capacity volume 1.8 - 2.2 L (frc = rv + erv)
        self.frc = frc
        # proper 12 - 20 / min Breaths / min
        self.breath_rate = breath_rate
        # By detection algorithm binary(detection Y / N)
        self.wheezing = wheezing
        # Cough presence, rate, dry cough(classification) Cough / min
        self.cough_presence_rate = cough_presence_rate

class SeconderyPriority:
    def __init__(self, fever = 36.5,bpm = 10,rpmf = 0,saturation = 96,blood_pressure_h = 120,blood_pressure_l = 80):
        # proper between 36-37.5 , after ovuletion between 36.5-37°C
        self.fever = fever
        # Beats/min
        self.bpm = bpm
        # relative power at maximal flow (RPMF) between inspiratory and expiratory
        self.rpmf = rpmf
        # proper over 95% %SpO2
        self.saturation = saturation
        # proper between 90-140
        self.blood_pressure_h = blood_pressure_h
        # proper between 60-90
        self.blood_pressure_l = blood_pressure_l

class MeasureResult:
    def __init__(self, unitId="Sensor_1", patientId=str(uuid.uuid1()), age=random.randrange(20, 90),weight = random.randrange(70, 90),\
                 gender="Male", timeTag=str(datetime.datetime.now()),\
                 vendor='EarlySense', audioPath="path to audio on cloud",\
                 primery_priority = PrimeryPriority(), secondery_priority = SeconderyPriority()):
        self.unitId = unitId
        self.patientId = patientId
        self.age = age
        self.weight = weight
        self.gender = gender
        self.timeTag = timeTag
        # left_side, right_side_chest, back...
        #self.sensorPos = sensorPos
        self.vendor = vendor
        self.audioPath = audioPath
        self.primery_priority = primery_priority.__dict__
        self.secondery_priority = secondery_priority.__dict__

if __name__ == '__main__':
    mr_list = []
    for i in range(50):
        mr = MeasureResult()
        #fill header data
        mr.unitId = utilities.get_guid()
        mr.patientId = utilities.get_guid()
        mr.weight = utilities.get_clampt_gauss_namber(50,120,80,10)
        #fill primary_priority data
        # proper 60 - 80 / min Pulse / min
        mr.primery_priority['pulse'] = utilities.get_clampt_gauss_namber(50,130,75,20)
        # Forced Expiratory vol.per 1 sec L / sec
        mr.primery_priority['fev1'] = utilities.get_clampt_gauss_namber(20, 90,45,20)
        # Forced vital capacity L / 10 sec
        mr.primery_priority['fvc'] = utilities.get_clampt_gauss_namber(50, 80,60,10)
        # Total lung capacity L
        #mr.primery_priority.tlc = random.uniform(4.0,7.0)
        mr.primery_priority['tlc'] = utilities.get_clampt_gauss_namber(4.0, 7.0,5.5,1.5)
        # Residual volume L
        mr.primery_priority['rv'] = utilities.get_clampt_gauss_namber(0.5, 1.5,0.8,0.3)
        # Expiratory reserved volume 0.7 - 1.2
        mr.primery_priority['erv'] = utilities.get_clampt_gauss_namber(0.4,1.2,0.8,0.3)
        # Functional residual capacity volume 1.8 - 2.2 L (frc = rv + erv)
        mr.primery_priority['frc'] = mr.primery_priority['rv'] + mr.primery_priority['erv']
        # proper 12 - 20 / min Breaths / min
        mr.primery_priority['breath_rate'] = math.floor(utilities.get_clampt_gauss_namber(10,22,16,5))

        p = random.randrange(0, 100)
        # By detection algorithm binary(detection Y / N)
        if(p< 70):
            mr.primery_priority['wheezing'] = True

        p = random.randrange(0, 100)
        # Cough presence, rate, dry cough(classification) Cough / min
        if (p < 70):
            mr.primery_priority['cough_presence_rate'] = random.randrange(2, 7)

        #fill secondery_priority data
        # proper between 36-37.5 , after ovuletion between 36.5-37°C
        mr.secondery_priority['fever'] = utilities.get_clampt_gauss_namber(35,42,38.4,2.3)
        # Beats/min
        mr.secondery_priority['bpm'] = utilities.get_clampt_gauss_namber(50,120,90,20)
        # relative power at maximal flow (RPMF) between inspiratory and expiratory
        mr.secondery_priority['rpmf'] = 69
        # proper over 95% %SpO2
        mr.secondery_priority['saturation'] = utilities.get_clampt_gauss_namber(90,100,94.4,2.3)
        # proper between 90-140
        mr.secondery_priority['blood_pressure_h'] = utilities.get_clampt_gauss_namber(90,120,115,20)
        # proper between 60-90
        mr.secondery_priority['blood_pressure_l'] = utilities.get_clampt_gauss_namber(60,90,75,10)

        mr_list.append(mr)

        mr_json = json.dumps(mr.__dict__)
        print(mr_json)

        header_info = {'content-type': 'application/json'}
        try:
            requests.post('http://52.16.82.127:3000/mr', data=mr_json, headers=header_info)
        except Exception as e:
            print(f'server disconnected:  {str(e)} ')