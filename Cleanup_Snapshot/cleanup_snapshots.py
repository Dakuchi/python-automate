import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2',region_name="ap-southeast-1")

volumes = ec2_client.describe_volumes(
	Filters=[
		{
			'Name' : 'tag:Name',
			'Values' : ['prod']
		}
	]
)
# list volumes with tag "prod"
print(volumes['Volumes'])

# list volumes
for volume in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
		{
			'Name' : 'volume-id',
			'Values' : ['prod']
		}
	]
)
    # sorted the snapshots by 'StartTime' from newest to oldest
    sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)
    print(sorted_by_date)

    for snap in sorted_by_date[2:]:
        # delete snapshots from 3rd element
        response = ec2_client.delete_snapshot(
            SnapshotId = snap['SnapshotId']
        )
        print(response)