from aws_cdk import (
    # Duration,
    Stack,
    aws_efs as efs,
    aws_ec2 as ec2,
    Fn,
    Tags

    # aws_sqs as sqs,
)
from constructs import Construct

class FileSystemStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpcid = Fn.import_value("KubeVPCID")
        sg = ec2.SecurityGroup(self,"EFSSg", vpc=vpc, description="EKS EFS Security Group",security_group_name="eks-efs")
        Tags.of(sg).add(key='cfn.eks-dev.stack', value='sg-stack')
        Tags.of(sg).add(key='Name', value='eks-efs')
        kube_fs = efs.FileSystem(self, "KubeFS", vpc=vpc, security_group=sg,performance_mode=efs.PerformanceMode.MAX_IO)
        Tags.of(kube_fs).add(key='efs.csi.aws.com/cluster', value='true')
        Tags.of(kube_fs).add(key='Name', value='KubeFS')