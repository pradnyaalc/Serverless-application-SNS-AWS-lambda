# Serverless-application-SNS-AWS-lambda

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- hello_world - Code for the application's Lambda function.
- template.yaml - A template that defines the application's AWS resources.

The application reads the data from the IOT devices into two different SNS topics.
This data consists of the module id of the device and the cumulative count of the number of messages received from the time the device was reset. 
One SNS topic produces data regurlarly while the other produces data weekly.
The data from these two topics are merged using AWS lambda and Redis Cache cluster to determine the success rate of the messages received. 

The application uses several AWS resources, including Lambda functions, SNS Topic and Redis Cluster. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates the application code.

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get started.

* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Pre-requisites
* Already existing VPC with public and private subnet
* Already existing S3 bucket 

## Clone the application and enter the directory
```bash
git clone https://github.com/pradnyaalc/Serverless-application-SNS-AWS-lambda.git
cd Serverless-application-SNS-AWS-lambda
```

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build your application for the first time, run the following in your shell:

```bash
sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

```bash
cd hello_world
pip install -r requirements.txt -t .
```
The above will ensure all the dependencies are packaged inside the folder


```bash
cd ..
sam package --template-file template.yaml --s3-bucket YOUR-S3-BUCKET --output-template-file packaged.yaml
sam deploy --template-file ./packaged.yaml --stack-name example-lambda-sns --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
```

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.

## Push Messages to the SNS topic

A weekly 'diagnostic' event is pushed to sns-topic-week in the following format

```
{
	"moduleid": <string>,
	"timestamp": <uint64_t>
	"attempts": <uint32_t>
}
```
Where:
* **moduleid**: unique identifier of a module
* **timestamp**: a unix timestamp (1/1/1970)
* **attempts**: the cumulative count of attempted message transmissions since the module
was reset

The event generated for every message received from an IoT device is pushed to sns-topic-iot in the following format

```
{
	"moduleid": <string>,
	"timestamp": <uint64_t>
	"tx_attempts": <uint32_t>
}
```
Where:
* **moduleid** is the unique identifier of a module
* **tx_attempts** is the cumulative count since the module was reset

## Monitoring
Push the records in the SNS topic and monitor using CloudWatch logs generated for each lambda function

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name example-lambda-sns
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
