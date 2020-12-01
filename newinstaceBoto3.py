import boto3
from decouple import config
#from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = config('aws_access_key_id')
AWS_SECRET_ACCESS_KEY = config('aws_secret_access_key')

session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key= AWS_SECRET_ACCESS_KEY, region_name= 'us-east-2')


ec2client_ohio = session.client('ec2', region_name='us-east-2')
ec2resource_ohio = session.resource('ec2', region_name='us-east-2')

ec2client_virginia = session.client('ec2', region_name='us-east-1')
ec2resource_virginia = session.resource('ec2', region_name='us-east-1')

ec2LoadBclient_virginia= session.client('ec2', region_name= 'us-east-1')
ec2AutoSclient_virginia= session.client('ec2', region_name= 'us-east-1')

userData= """#!/bin/sh
    cd home/ubuntu
    sudo apt update
    git clone https://github.com/JoseFernandoInsper/ProjetoFinalCloud.git
    cd ProjetoFinalCloud
    chmod +x criar_bd.sh
    ./criar_bd.sh
    """
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

Virginia=  """#!/bin/sh
    cd home/ubuntu
    sudo apt update
    git clone https://github.com/raulikeda/tasks.git
    sudo sed -i 's/node1/{0}/' /home/ubuntu/tasks/portfolio/settings.py
    cd tasks
    ./install.sh
    cd ..
    sudo reboot
    """

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
  KeyName='josekeys',
  UserData=Virginia
)