import boto3

ec2 = boto3.resource('ec2')

create_instance = ec2.create_instances(
  ImageId='ami-0dd9f0e7df0f0a138',
  InstanceType = 't2.micro',
  MaxCount='1',
  MinCount='1',
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

)