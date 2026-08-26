import boto3
import json
import sys

request = sys.argv[1]

ecs = boto3.client("ecs", region_name="us-east-2")

response = ecs.run_task(
    cluster="dependable-hamster-ie-the-workflow-engine",
    taskDefinition="workflow-engine-task-family",  # uses latest revision (:4)
    launchType="FARGATE",
    networkConfiguration={
        "awsvpcConfiguration": {
            "subnets": ["subnet-02fe14dc25e12338e"],
            "assignPublicIp": "ENABLED"
        }
    },
    overrides={
        "containerOverrides": [{
            "name": "workflow_engine",
            "environment": [
                {"name": "WORKFLOW_REQUEST", "value": request}
            ]
        }]
    }
)

task_arn = response["tasks"][0]["taskArn"]

# python3 client.py '{"workflow_id":"WORKFLOW_ID","blocks":[{"name":"test_long_block","command":{"source_bucket":"s3://amzn-s3-log-bucket-laby-test513270157", "destination":"s3://amzn-s3-log-bucket-laby-output125351"}}]}'

