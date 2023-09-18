from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_eks as eks,
    lambda_layer_kubectl_v27,
    
    # aws_sqs as sqs,
)
import yaml

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
        mapping = eks
        cluster.add_manifest("DevOpsNS",{"apiVersion":"v1",
                                                               "kind":"Namespace",
                                                               "metadata":{"name":"devops"}})
        selector = eks.Selector(namespace="devops")
        cluster.add_fargate_profile(id="DevOpsFGProfile",selectors=[selector])
        # ymlstring = open('kubemanifests/volume.yml','r').read()
        # volumemanifests = list(yaml.load_all(ymlstring,Loader=yaml.Loader))
        # i=0
        # for manifest in volumemanifests: 
        #     cluster.add_manifest(f"DevOpsVolume{i}",manifest)
        #     i+=1
