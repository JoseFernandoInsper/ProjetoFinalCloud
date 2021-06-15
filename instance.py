import sys
import boto3
from security_group import *
from botocore.exceptions import ClientError
import time

ec2client_virginia = boto3.client('ec2', region_name='us-east-1')
ec2resource_virginia = boto3.resource('ec2', region_name='us-east-1')

ec2client_ohio = boto3.client('ec2', region_name='us-east-2')
ec2resource_ohio = boto3.resource('ec2', region_name='us-east-2')

waiteast1 = ec2client_virginia.get_waiter('instance_status_ok')
waiteast2 = ec2client_ohio.get_waiter('instance_status_ok')


def definirIp(cliente, nome):
  instanceIp = cliente.describe_instances(
    Filters=[
      {
        'Name': 'tag:Name',
        'Values': [nome]
      },
      {
        'Name': 'instance-state-name',
        'Values': ['running']
      }
    ]
  )
  ip = instanceIp['Reservations'][0]['Instances'][0]['PublicIpAddress']
  return(ip)

def definirId(cliente, nome):
  instanceId = cliente.describe_instances(
    Filters=[
      {
        'Name': 'tag:Name',
        'Values': [nome]
      },
      {
        'Name': 'instance-state-name',
        'Values': ['running']
      }

    ]
  )
  id = instanceId['Reservations'][0]['Instances'][0]['InstanceId']
  return(id)


def ohio(security_g):
  userData= """#!/bin/sh
      cd home/ubuntu
      sudo apt update
      git clone https://github.com/JoseFernandoInsper/ProjetoFinalCloud.git
      cd ProjetoFinalCloud
      chmod +x criar_bd.sh
      ./criar_bd.sh
      """
  try:
    create_instanceOhio = ec2resource_ohio.create_instances(
      ImageId='ami-0dd9f0e7df0f0a138',
      InstanceType = 't2.micro',
      MaxCount=1,
      MinCount=1,
      TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'instDB'
                    },
                ]
            },
        ],
      SecurityGroupIds=[security_g],
      KeyName='josekeeyss',
      UserData=userData
    )
    instanceId = 0
    ec2client_ohio.get_waiter('instance_status_ok').wait(InstanceIds=[create_instanceOhio[0].id])
    # print('passoi')
  except ClientError as e:
    print(e)

def VirginiaInst(ohioIp, security_g):
  Virginia=  """#!/bin/sh
      cd home/ubuntu
      sudo apt update
      git clone https://github.com/JoseFernandoInsper/tasks.git
      sudo sed -i 's/node1/{0}/' /home/ubuntu/tasks/portfolio/settings.py
      cd tasks
      ./install.sh
      cd ..
      sudo reboot
      """.format(ohioIp)
  try:
    create_instanceVirginia = ec2resource_virginia.create_instances(
      ImageId = 'ami-00ddb0e5626798373',
      InstanceType = 't2.micro',
      MaxCount=1,
      MinCount=1,
      TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'JoseVirginia'
                    },
                ],
            },
        ],
      SecurityGroupIds=[security_g],
      KeyName='josekeyss',
      UserData=Virginia
    )
    ec2client_virginia.get_waiter('instance_status_ok').wait(InstanceIds=[create_instanceVirginia[0].id])
    # print("pasosu")
  except ClientError as e:
    print(e)


def delete_instancia(cliente, nome):
  instance_id = cliente.describe_instances(
    Filters=[
      {
        'Name': 'tag:Name',
        'Values': [nome]
      }
    ]
  )
  ids = []
  for reservation in (instance_id["Reservations"]):
    for instance in reservation["Instances"]:
      ids.append(instance['InstanceId'])
  
  try:
    if len(ids)>0:
      cliente.terminate_instances(InstanceIds=ids)
      cliente.get_waiter('instance_terminated').wait(InstanceIds=ids)
  except ClientError as e:
    print(e)

