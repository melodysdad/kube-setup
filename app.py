#!/usr/bin/env python3
import os

import aws_cdk as cdk

from kube_setup.kube_setup_stack import KubeSetupStack
from kube_setup.network_stack import NetworkStack
from kube_setup.file_system_stack import FileSystemStack

app = cdk.App()
KubeSetupStack(app, "KubeSetupStack")
network_stack = NetworkStack(app, "NetworkStack")
FileSystemStack(app, "FileSystemStack", network_stack.vpc)
app.synth()
