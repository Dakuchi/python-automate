import boto3

# add prod tag to ec2 in Tokyo region
ec2_client_tokyo = boto3.client('ec2',region_name="ap-northeast-1")
ec2_resource_tokyo = boto3.resource('ec2',region_name="ap-northeast-1")

# store the instance id to list
instances_id_tokyo = []
reservation_tokyo = ec2_client_tokyo.describe_instances()['Reservations']
for res in reservation_tokyo:
    instances = res['Instances']
    for ins in instances:
        instances_id_tokyo.append(ins['InstanceId'])

response = ec2_resource_tokyo.create_tags(
    Resources = instances_id_tokyo,
    Tags = [
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)

# add dev tag to ec2 in Singapore region

ec2_client_singapore = boto3.client('ec2',region_name="ap-southeast-1")
ec2_resource_singapore = boto3.resource('ec2',region_name="ap-southeast-1")

# store the instance id to list
instances_id_singapore = []
reservation_singapore = ec2_client_singapore.describe_instances()['Reservations']
for res in reservation_singapore:
    instances = res['Instances']
    for ins in instances:
        instances_id_singapore.append(ins['InstanceId'])

response = ec2_resource_singapore.create_tags(
    Resources = instances_id_singapore,
    Tags = [
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)