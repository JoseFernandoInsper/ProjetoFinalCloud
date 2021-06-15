import sys
import boto3
from security_group import *
from instance import *
from botocore.exceptions import ClientError
import time


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
  ImagePRINT=[img["ImageId"]]
  print(ImagePRINT)
  print(img['ImageId'])
  return img['ImageId']
