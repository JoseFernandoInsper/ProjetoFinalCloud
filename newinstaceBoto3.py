import sys
import boto3
from decouple import config
from botocore.exceptions import ClientError
import time

AWS_ACCESS_KEY_ID = config('aws_access_key_id')
AWS_SECRET_ACCESS_KEY = config('aws_secret_access_key')

session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key= AWS_SECRET_ACCESS_KEY, region_name= 'us-east-2')


ec2client_ohio = session.client('ec2', region_name='us-east-2')
ec2resource_ohio = session.resource('ec2', region_name='us-east-2')

ec2client_virginia = session.client('ec2', region_name='us-east-1')
ec2resource_virginia = session.resource('ec2', region_name='us-east-1')

ec2LoadBclient_virginia= session.client('ec2', region_name= 'us-east-1')
ec2AutoSclient_virginia= session.client('ec2', region_name= 'us-east-1')


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


    
def ohio():
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
      SecurityGroupIds=['sg-04f1b35ff4633d922'],
      SecurityGroups=['securityJose'],
      KeyName='josekeys',
      UserData=userData
    )
    instanceId = 0
    ec2client_ohio.get_waiter('instance_status_ok').wait(InstanceIds=[create_instanceOhio[0].id])
    print('passoi')
  except ClientError as e:
    print(e)


def VirginiaInst(ohioIp):
  Virginia=  """#!/bin/sh
      cd home/ubuntu
      sudo apt update
      git clone https://github.com/raulikeda/tasks.git
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
                ]
            },
        ],
      SecurityGroupIds=['sg-02b2377c79fdee256'],
      SecurityGroups=['securityJose'],
      KeyName='josekeysNV',
      UserData=Virginia
    )
    ec2client_virginia.get_waiter('instance_status_ok').wait(InstanceIds=[create_instanceVirginia[0].id])
    print("pasosu")
  except ClientError as e:
    print(e)


def del_img(img_name):
  response = ec2client_virginia.describe_images(
    Filters=[
      {
        'Name': 'name',
        'Values': [img_name]
      }
    ]
  )
  if len(response['Images'])>0:
    id_img = response['Images'][0]['ImageId']
    ec2client_virginia.deregister_image(ImageId=id_img)

def criar_img(instance_id, nome):
  img = ec2client_virginia.create_image(
    InstanceId = instance_id,
    NoReboot = True,
    Name=nome)
  ec2client_virginia.get_waiter('image_available').wait( ImageIds=[img["ImageId"]])
  return (img)

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

def delete_ASL(cliente, nome):
  response = cliente.describe_launch_configurations(LaunchConfigurationNames = [nome])
  if len(response['LaunchConfigurations'])>0:
    client.delete_launch_configuration(LaunchConfigurationName=nome)

def criar_ASL(cliente, nome, image, security_id):
  cliente.create_launch_configuration(
    LaunchConfigurationName=nome, ImageId=image, KeyName='josekeysNV', SecurityGroups=[security_id], InstanceType='t2.micro'
  )

def delete_AS(cliente, nome, launchName):
  response = cliente.describe_auto_caling_groups(AutoScalingGroupNames=[nome])
  for n in response['AutoScalinfGroups']:
    if n['AutoScalingGroupName'] == nome:
      cliente.delete_auto_scaling_group(
        AutoScalingGroupName=nome,
        ForceDelete=True
      )

def criar_AS(cliente,nome, launch_name):
  client.create_auto_scaling_group(
    AutoScalingGroupName=nome,
    LaunchConfigurationName=launch_name,
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
    LoadBalancerNames=['LoadBalancer'],
    CapacityRebalance=True
  )




delete_instancia(ec2client_ohio, 'instDB')
delete_instancia(ec2client_virginia, 'JoseVirginia')

ohio()
ohioip = definirIp(ec2client_ohio, 'instDB')

VirginiaInst(ohioip)
virId = definirId(ec2client_virginia, 'JoseVirginia')
del_img('joseORM')

img = criar_img(virId, 'joseORM')
delete_instancia(ec2client_virginia, 'JoseVirginia')

delete_LB(ec2LoadBclient_virginia, 'joseLB')
time.sleep(10)

criar_LB(ec2LoadBclient_virginia, joseLB, virId)
time.sleep(10)

delete_ASL(ec2AutoSclient_virginia, 'joseASL', virId)
time.sleep(10)

criar_ASL(ec2AutoSclient_virginia, 'joseAS', img,  virId)
time.sleep(10)

delete_AS(ec2AutoSclient_virginia,joseAS , joseASL  )
time.sleep(10)
