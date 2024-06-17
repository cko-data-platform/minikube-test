# Data Platform: Terraform Task

## Prerequisites

- Ensure docker is running locally.

- Run `docker-compose up --build`. All being well, you should get an output similar to this:
```
[+] Running 2/0
 ✔ Container localstack-main   Created
 ✔ Container tflocal           Created
 ...
 Ready.
```

- Open a new terminal, navigate to this directory (`terraform`) and execute the following to exec into the tflocal container:
```
docker-compose exec tflocal /bin/sh
```

## The task

1. Apply the terraform (use the command `tflocal` instead of `terraform`). You'll notice an error. Please fix the issue and then re-apply.

2. You should now have a lambda in your localstack environment. It can be executed using the following command:
```
awslocal lambda invoke --function-name image_processing_lambda output.txt
```
Check the content of the output.txt file to debug the lambda and fix any issues accordingly.
If you wish to add steps to the code to allow for logging/troubleshooting between invocations, you can view subsequent Cloudwatch logs with the following:
```
awslocal logs filter-log-events --log-group-name /aws/lambda/image_processing_lambda --query 'events[*].[timestamp,mess
age]' --output json --start-time $(date -u +%s) --region us-east-1
```