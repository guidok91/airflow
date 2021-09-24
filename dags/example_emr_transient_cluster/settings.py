

class EMRClusterConfig:
    _TAGS = [
        {"Key": "ClusterState", "Value": "Transient"},
        {"Key": "Environment", "Value": "Staging"},
        {"Key": "Group", "Value": "Experimentation EMR"},
        {"Key": "Name", "Value": "test-guido-transient-cluster"},
        {"Key": "Service", "Value": "EMR Cluster"},
        {"Key": "Squad", "Value": "Experimentation Core"},
        {"Key": "Tribe", "Value": "AdTech"},
    ]

    _INSTANCES = {
        "Ec2SubnetId": "subnet-0242145451d96403c",
        "EmrManagedMasterSecurityGroup": "sg-946f6ef2",
        "EmrManagedSlaveSecurityGroup": "sg-956f6ef3",
        "AdditionalMasterSecurityGroups": ["sg-8128cfe6", "sg-a7f3acdd"],
        "AdditionalSlaveSecurityGroups": ["sg-8128cfe6", "sg-a7f3acdd"],
        "ServiceAccessSecurityGroup": "sg-99d230e2",
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
        "Name": "test-guido-transient-cluster",
        "ReleaseLabel": "emr-6.4.0",
        "Applications": [{"Name": "Spark"}],
        "LogUri": "s3://hf-bi-emr-staging-logs/",
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
                    "s3://experimentation-core-ddi/binary-repository/test-guido-transient-emr-clusters/load_raw_data.py",
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
                    "s3://experimentation-core-ddi/binary-repository/test-guido-transient-emr-clusters/transform.py",
                ],
            },
        }
    ]
