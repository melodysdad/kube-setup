from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_eks as eks,
    lambda_layer_kubectl_v27,
    aws_efs as efs,
    aws_ec2 as ec2,
    aws_iam as iam,
    
    # aws_sqs as sqs,
)
import yaml

from constructs import Construct


class KubeSetupStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        file_system: efs.FileSystem,
        vpc: ec2.Vpc,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        masterRole = iam.Role(self, "KubeRole", assumed_by=iam.CompositePrincipal(
            iam.ServicePrincipal(service="eks.amazonaws.com"),
            iam.AnyPrincipal()
        ))
        masterRole.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )
        kubectl_layer = lambda_layer_kubectl_v27.KubectlV27Layer(self, "KubeLayer")
        cluster = eks.FargateCluster(
            self,
            "KubeCluster",
            version=eks.KubernetesVersion.V1_27,
            masters_role=masterRole,
            cluster_name="KubeCluster",
            output_cluster_name=True,
            kubectl_layer=kubectl_layer,
            vpc=vpc,
        )
        cluster.add_manifest(
            "DevOpsNS",
            {"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": "devops"}},
        )
        selector = eks.Selector(namespace="devops")
        cluster.add_fargate_profile(id="DevOpsFGProfile", selectors=[selector])
        storage_class_manifest = {
            "apiVersion": "storage.k8s.io/v1",
            "kind": "StorageClass",
            "metadata": {"name": "efs-sc"},
            "provisioner": "efs.csi.aws.com",
            "parameters": {
                "provisioningMode": "efs-ap",
                "fileSystemId": file_system.file_system_id,
                "directoryPerms": "700"
            }
        }
        cluster.add_manifest("EfsStorageClass", storage_class_manifest)

        # ymlstring = open('kubemanifests/volume.yml','r').read()
        # volumemanifests = list(yaml.load_all(ymlstring,Loader=yaml.Loader))
        # i=0
        # for manifest in volumemanifests:
        #     cluster.add_manifest(f"DevOpsVolume{i}",manifest)
        #     i+=1
