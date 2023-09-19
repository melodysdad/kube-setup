#!/usr/bin/env python3
import os

import aws_cdk as cdk

from kube_setup.kube_setup_stack import KubeSetupStack
from kube_setup.network_stack import NetworkStack
from kube_setup.file_system_stack import FileSystemStack

app = cdk.App()
network_stack = NetworkStack(app, "NetworkStack")
file_system_stack = FileSystemStack(app, "FileSystemStack", network_stack.vpc)
KubeSetupStack(app, "KubeSetupStack", file_system=file_system_stack.kube_fs,vpc=network_stack.vpc)
app.synth()
