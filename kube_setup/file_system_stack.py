from aws_cdk import (
    # Duration,
    Stack,
    aws_efs as efs,
    aws_ec2 as ec2,
    Fn

    # aws_sqs as sqs,
)
from constructs import Construct

class FileSystemStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpcid = Fn.import_value("KubeVPCID")
        efs.FileSystem(self, "KubeFS", vpc=vpc)