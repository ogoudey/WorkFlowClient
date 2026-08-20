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
