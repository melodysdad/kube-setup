from aws_cdk import (
    # Duration,
    CfnOutput,
    Stack,
    aws_ec2 as ec2,

    # aws_sqs as sqs,
)

from constructs import Construct

class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = ec2.Vpc(self, "KubeVPC",
                      ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"))
        

