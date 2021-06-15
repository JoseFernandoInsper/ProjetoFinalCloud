import sys
import boto3
from security_group import *
from instance import *
from image import *
from loadBalance import *
from botocore.exceptions import ClientError
import time


clientAutoScalling = boto3.client('autoscaling')

def delete_ASL(cliente, nome):
  response = cliente.describe_launch_configurations(LaunchConfigurationNames = [nome])
  try:
    if len(response['LaunchConfigurations'])>0:
      cliente.delete_launch_configuration(LaunchConfigurationName=nome)
  except ClientError as e:
    print(e)

def criar_ASL(cliente, nome, image, security_id):
  print("SG::::")
  print(security_id)
  print("IMG::::")
  print(image)
  cliente.create_launch_configuration(
    LaunchConfigurationName=nome,
    ImageId=image,
    KeyName='josekeyss',
    SecurityGroups=[security_id],
    InstanceType='t2.micro'
  )

def delete_AS(cliente, nome):
  response = cliente.describe_auto_scaling_groups(AutoScalingGroupNames=[nome])
  for n in response['AutoScalingGroups']:
    if n['AutoScalingGroupName'] == nome:
      cliente.delete_auto_scaling_group(
        AutoScalingGroupName=nome,
        ForceDelete=True
      )

def criar_AS(cliente,nome, launch_name):
  cliente.create_auto_scaling_group(
    AutoScalingGroupName=nome,
    LaunchConfigurationName=launch_name,
    #LaunchTemplate={
    #    'LaunchTemplateId': 'lt-016ee6f4c0d0eae0f',
    #    'Version': '$Latest',
    #},
    MinSize=2,
    MaxSize=5,
    DesiredCapacity=2,
    AvailabilityZones=[
      'us-east-1a',
      'us-east-1b',
      'us-east-1c',
      'us-east-1d',
      'us-east-1e',
      'us-east-1f'
    ],
    LoadBalancerNames=['JoseLoadBalance'],
    CapacityRebalance=True
  )
  print("poassoei")

