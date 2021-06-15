import sys
import boto3
from security_group import *
from instance import *
from image import *
from loadBalance import *
from AutoScaling import *
from botocore.exceptions import ClientError
import time


delete_AS(clientAutoScalling,'JoseAutoS')
delete_ASL(clientAutoScalling, 'LoucherAS')
delete_instancia(ec2client_ohio, 'instDB')
delete_instancia(ec2client_virginia, 'JoseVirginia')
delete_LB(elbLoadBalance, 'JoseLoadBalance')
time.sleep(60)
delete(ec2client_virginia, "sgJoseNV")
delete(ec2client_ohio, "sgJoseOH")

sgverginia = criarsg(ec2client_virginia, "sgJoseNV")
sgohio = criarsg(ec2client_ohio, "sgJoseOH")
print("grupos de segurança criados.............")
ohio(sgohio)

time.sleep(30)

ohioip = definirIp(ec2client_ohio, 'instDB')

VirginiaInst(ohioip, sgverginia)
virId = definirId(ec2client_virginia, 'JoseVirginia')

del_img('joseORM')
img = criar_img(virId, 'joseORM')
delete_instancia(ec2client_virginia, 'JoseVirginia')  


time.sleep(30)

criar_LB(elbLoadBalance, 'JoseLoadBalance', sgverginia)

criar_ASL(clientAutoScalling, 'LoucherAS', img, sgverginia)

criar_AS(clientAutoScalling, 'JoseAutoS', 'LoucherAS')
print('processo finalizado ...............')
