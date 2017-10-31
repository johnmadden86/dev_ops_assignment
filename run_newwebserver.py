#!/usr/bin/env python3
import subprocess

import boto3
import time
import sys
from pathlib import Path

# takes key name (with .pem extension) as a parameter
key_name = sys.argv[1]

# checks file exists, and if file extension is correct
key_file = Path(key_name)
if key_file.is_file():
    print("key file found")
    if key_name[-4:] == ".pem":
        print("file extension ok")
    else:
        print("Error, wrong file extension")
else:
    print("Error, file not found")
    exit(0)

print("Key: " + key_name)
key_name_no_extension = key_name[:-4] # remove .pem extension

file_upload = " check_webserver.py"

ec2 = boto3.resource("ec2")
instances = ec2.create_instances(
    ImageId="ami-acd005d5",           # Ireland region
    KeyName=key_name_no_extension,
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=["sg-6f804314"], # Security group is pre-configured to allow public access
    UserData='''#!/bin/bash
                yum -y update
                yum -y install nginx
                yum -y install python36
                service nginx start
                chkconfig nginx on''',
    InstanceType="t2.micro")

print(instances)
instance = instances[0]

instance.create_tags(
    Resources=[instance.id],
    Tags=[
        {'Key': 'Name', 'Value': 'Test_instance'},
    ])

print ("An instance with ID", instance.id, "has been created.")

instance.reload()      # ensures instance object has current live instance data

while not instance.public_ip_address:
    instance.reload() # waitd until public IP has been assigned before continuing
print("Public IP address:", instance.public_ip_address)

host_name = " ec2-user@" + instance.public_ip_address
ssh = "ssh -o StrictHostKeyChecking=no -i " + key_name + host_name
cmd = ssh + " pwd"
print(cmd)
time.sleep(60) # pause to allow for ssh connection
(status, output) = subprocess.getstatusoutput(cmd)
print(status, output)

# uploads check_webserver file
scp = "scp -i " + key_name + file_upload + host_name + ":."
print(scp)
(status, output) = subprocess.getstatusoutput(scp)
print(status, output)

# gives files executable permissions
cmd = ssh + " chmod +x" + file_upload
print(cmd)
(status, output) = subprocess.getstatusoutput(cmd)
print(status, output)

# runs check_webserver
cmd = ssh + " ./" + file_upload[1:] # deletes preceding space
print(cmd)
(status, output) = subprocess.getstatusoutput(cmd)
print(status, output)

# get stats
stat_file = "stats-" + instance.public_ip_address + ".txt"

cmd = ssh + " vmstat > " + stat_file
print(cmd)
(status, output) = subprocess.getstatusoutput(cmd)
print(status, output)

cmd = ssh + " netstat >> " + stat_file
print(cmd)
(status, output) = subprocess.getstatusoutput(cmd)
print(status, output)

cmd = ssh + " ps -A >> " + stat_file
print(cmd)
(status, output) = subprocess.getstatusoutput(cmd)
print(status, output)

