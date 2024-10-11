import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2',region_name="ap-southeast-1")
ec2_resource = boto3.resource('ec2',region_name="ap-southeast-1")

instance_id = "i-047b338564b2bd890"

# list all volumes attach to instance
volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name' : 'attachment.instance-id',
            'Values' : [instance_id]
        }
    ]
)
instance_volumes = volumes['Volumes'][0]
print(instance_volumes)

# list all snapshots of the instance
snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
		{
			'Name' : 'volume-id',
			'Values' : [instance_volumes['VolumeId']]
		}
	]
)

# get the latest snapshot of instance
latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]
print(latest_snapshot['StartTime'])

# create new volume from latest snapshot
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone='ap-southeast-1a',
    TagSpecifications=[
        {
            'ResourceType' : 'volume',
            'Tags': [
                {
                    'Key' : 'Name',
                    'Value' : 'prod'
                }
            ]
        }
    ]
) 

# check state of volume til it available
while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)
    if vol.state == 'available':     
        # attach new volume to EC2 instance
        ec2_resource.Instance(instance_id).attach_volume(
        VolumeId=new_volume['VolumeId'],
        Device='/dev/xvdb' # cannot use same name with attaching volume device
        )
        break
