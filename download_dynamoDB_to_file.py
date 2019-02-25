from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import os
import paramiko
import datetime
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('transaction')
    logs = []
    day = datetime.date.today()-datetime.timedelta(1)
    #day_string = day.strftime('%Y-%m-%d')
    day_string = day.strftime('2019-02-15')
    response = table.scan(
        FilterExpression=Attr('partition').eq(day_string)
    )
    #print(response['Items'])
    print(day)
    for i in response['Items']:
        logs.append(i.get('date', "NA"))
        logs.append("|")
        logs.append(i.get('ipaddress', "NA"))
        logs.append("|")
        logs.append(i.get('useragent', "NA"))
        logs.append("|")
        logs.append(i.get('sendstatus', "NA"))
        logs.append("|")
    s = "".join(logs)
    #print(s)
    with open("file.txt", "w") as output:
        output.write(str(s))

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect("10.x.x.x" username="admin", password="pass123")
    sftp = ssh.open_sftp()
    sftp.put("/tmp/file.txt", "/tmp/file.txt")
    sftp.close()
    ssh.close()

