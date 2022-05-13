

class EMRClusterConfig:
    _CLUSTER_NAME = "test-transient-cluster"

    _TAGS = [
        {"Key": "Name", "Value": _CLUSTER_NAME},
        {"Key": "ClusterState", "Value": "Transient"},
        {"Key": "Environment", "Value": "Staging"},
        {"Key": "Service", "Value": "EMR Cluster"},
    ]

    _INSTANCES = {
        "Ec2SubnetId": "<PLACDHOLDER>",
        "EmrManagedMasterSecurityGroup": "<PLACDHOLDER>",
        "EmrManagedSlaveSecurityGroup": "<PLACDHOLDER>",
        "AdditionalMasterSecurityGroups": ["<PLACDHOLDER>", "<PLACDHOLDER>"],
        "AdditionalSlaveSecurityGroups": ["<PLACDHOLDER>", "<PLACDHOLDER>"],
        "ServiceAccessSecurityGroup": "<PLACDHOLDER>",
        "InstanceGroups": [
            {
                "Name": "Master",
                "Market": "SPOT",
                "InstanceRole": "MASTER",
                "InstanceType": "m1.medium",
                "InstanceCount": 1,
            }
        ],
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,
    }

    JOB_FLOW_OVERRIDES = {
        "Name": _CLUSTER_NAME,
        "ReleaseLabel": "emr-6.4.0",
        "Applications": [{"Name": "Spark"}],
        "LogUri": "s3://<PLACDHOLDER>/",
        "Instances": _INSTANCES,
        "JobFlowRole": "EMR_EC2_DefaultRole",
        "ServiceRole": "EMR_DefaultRole",
        "Tags": _TAGS,
    }


class SparkSteps:
    LOAD_RAW_DATA = [
        {
            "Name": "load_raw_data",
            "ActionOnFailure": "CONTINUE",
            "HadoopJarStep": {
                "Jar": "command-runner.jar",
                "Args": [
                    "spark-submit",
                    "--master",
                    "local",
                    "s3://<PLACEHOLDER>/load_raw_data.py",
                ],
            },
        }
    ]

    TRANSFORM = [
        {
            "Name": "transform",
            "ActionOnFailure": "CONTINUE",
            "HadoopJarStep": {
                "Jar": "command-runner.jar",
                "Args": [
                    "spark-submit",
                    "--master",
                    "local",
                    "s3://<PLACEHOLDER>/transform.py",
                ],
            },
        }
    ]
