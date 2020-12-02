import sys
import boto3
from botocore.exceptions import ClientError

ec2client_virginia = session.client('ec2', region_name='us-east-1')

def delete(cliente, nome_grupo):
  descricao = cliente.describe_security_groups()
  for grupo in descricao['SecurityGroups']:
    if grupo['groupName'] == nome_grupo:
      cliente.delete_security_group(GroupName=nome_grupo)

def criarsg(cliente, nome_grupo):
  response = cliente.describe_vpcs()
  vpcid = response.get('Vpcs', [{}])[0].get('VpcId', '')

  response = cliente.create_security_group(GroupName= nome_grupo, Description='sg jose', VpcId=vpcid)

  security_group_id = response['GroupId']

  data = cliente.authorize_security_group_ingress(
    GroupId = security_group_id,
    IpPermissions=[
      {'IpProtocol': 'tcp',
       'FromPort': 80,
       'ToPort': 80,
       'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
      {'IpProtocol': 'tcp',
       'FromPort': 22,
       'ToPort': 22,
       'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
      {'IpProtocol': 'tcp',
       'FromPort': 5432,
       'ToPort': 5432,
       'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
      {'IpProtocol': 'tcp',
       'FromPort': 8080,
       'ToPort': 8080,
       'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
    ])
  return(security_group_id)