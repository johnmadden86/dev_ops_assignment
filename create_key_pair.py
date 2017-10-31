#!/usr/bin/env python3

import subprocess
import sys

new_key_name = sys.argv[1]
cmd = "aws ec2 create-key-pair --key-name " + new_key_name + " --query 'KeyMaterial' --output text > " + new_key_name + ".pem"
print(cmd)
(status, output) = subprocess.getstatusoutput(cmd)
print(status, output)
