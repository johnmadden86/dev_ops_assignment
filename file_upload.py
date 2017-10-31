#!/usr/bin/env python3
import sys
import boto3
import subprocess


s3 = boto3.resource("s3")

# takes four parameters
instance_ip = sys.argv[1]
key_pair = sys.argv[2]
bucket_name = sys.argv[3]
object_name = sys.argv[4]

# puts the image into a bucket
try:
    response = s3.Object(bucket_name, object_name).put(Body=open(object_name, 'rb'))
    print (response)
except Exception as error:
    print (error)

# uploads the image from the bucket to a html page
try:
    url = "https://s3-eu-west-1.amazonaws.com/" + bucket_name + "/" + object_name
    image_tag = "<img src=\"" + url + "\">"

    directory = "/usr/share/nginx/html/"
    web_page = "index.html"

    ssh = "ssh -t -o StrictHostKeyChecking=no -i " + key_pair + " ec2-user@" + instance_ip

    # creates page if not in existence
    cmd = ssh + " sudo touch " + directory + web_page
    print(cmd)
    (status, output) = subprocess.getstatusoutput(cmd)
    print(status, output)

    # gives full permissions to modify the file
    cmd = ssh + " sudo chmod +777 " + directory + web_page
    print(cmd)
    (status, output) = subprocess.getstatusoutput(cmd)
    print(status, output)

    # appends an img tag to the web page
    image_tag = '\"' + image_tag + '\"'
    echo = "echo " + image_tag + " >> " + directory + web_page
    cmd = ssh + " \'" + echo + "\'"
    print(cmd)
    (status, output) = subprocess.getstatusoutput(cmd)
    print(status, output)

    if status == 0:
        print("success")
        print("image appended to index page, visit " + instance_ip + " to view")
    else:
        print(output, "fail")

except Exception as err:
    print(err)
