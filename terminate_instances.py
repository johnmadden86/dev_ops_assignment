#!/usr/bin/env python3
import sys
import boto3
ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
    response = instance.terminate()
    print (response)

