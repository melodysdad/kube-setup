from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_eks as eks,
    lambda_layer_kubectl_v27,
    
    # aws_sqs as sqs,
)

from constructs import Construct


class KubeSetupStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        masterRole = iam.Role(self, "KubeRole", assumed_by=iam.AccountRootPrincipal())
        kubectl_layer = lambda_layer_kubectl_v27.KubectlV27Layer(self,"KubeLayer")
        cluster = eks.FargateCluster(
            self,
            "KubeCluster",
            version=eks.KubernetesVersion.V1_27,
            masters_role=masterRole,
            cluster_name="KubeCluster",
            output_cluster_name=True,
            kubectl_layer=kubectl_layer
            
        )
