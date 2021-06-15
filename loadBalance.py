import sys
import boto3
from security_group import *
from instance import *
from image import *
from botocore.exceptions import ClientError
import time

elbLoadBalance = boto3.client('elb', region_name='us-east-1')

def delete_LB(cliente, nome):
  cliente.delete_load_balancer(LoadBalancerName=nome)

  time.sleep(30)

def criar_LB(cliente, nome, security_Id):
  response = cliente.create_load_balancer(
    LoadBalancerName=nome,
    Listeners=[
      {
        'Protocol': 'HTTP',
        'LoadBalancerPort': 80,
        'InstancePort': 8080
      }],
    AvailabilityZones=[
      'us-east-1a',
      'us-east-1b',
      'us-east-1c',
      'us-east-1d',
      'us-east-1e',
      'us-east-1f'
    ],
    SecurityGroups=[security_Id],
    Tags=[
      {
        'Key': 'Name', 'Value': 'joseLB'
      }
    ]
  )
  with open("dns.txt", "w") as file:
    file.write(response['DNSName'])
