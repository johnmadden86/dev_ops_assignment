#!/usr/bin/env python3

"""A tiny Python program to check that nginx is running.
Try running this program from the command line like this:
  python3 check_webserver.py
"""

import subprocess

def check_nginx():
    cmd = 'ps -A | grep nginx | grep -v grep'

    (status, output) = subprocess.getstatusoutput(cmd)

    if status > 0:  
        print("Nginx Server IS NOT running")

        print("Starting nginx")
        subprocess.getstatusoutput('sudo service nginx start')
        check_nginx() # recursive call to re-check status
    else:
        print("Nginx Server IS running")

# Define a main() function.
def main():
    check_nginx()
      
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

