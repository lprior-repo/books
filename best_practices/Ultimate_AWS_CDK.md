# Ultimate AWS CDK for Infrastructure Automation

**Author:** Anish Kumar
**Topic tags:** `#architecture` `#cloud` `#aws`
**Language focus:** TypeScript (with Python/Java/C# equivalents referenced)
**Sources:** `markdown_output/Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar/Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md` · `summaries/Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md`

## TL;DR

This book positions AWS CDK as the AWS-native, language-first evolution of CloudFormation, teaching constructs (L1/L2/L3), multi-stack projects, CDK Pipelines, IAM hardening with `cdk-nag`, and a real testing pyramid (assertions, snapshots, E2E). Use it when you're AWS-centric and want IDE autocomplete, unit tests for infrastructure, and full software-engineering discipline on top of CloudFormation's deployment guarantees.

---

## Best Practices by Topic

### DevOps Automation Drives IaC Adoption

**Principle:** IaC is the artifact; DevOps automation is the operating model that treats infrastructure with the same rigor as application code.

**Do:**
- Use version control, peer review, and automated testing for infrastructure changes.
- Codify deployments as code so every promotion is reproducible and reversible.
- Treat releases as a service to developers — measured by lead time for change, not ticket count.

**Don't:**
- Run a ticket-driven manual provisioning process alongside CDK; you will end up with two sources of truth.
- Treat IaC as a documentation exercise — it must be the live system of record.

*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Chapter 1: Introduction to AWS CDK and DevOps Automation"*

---

### AWS CDK vs CloudFormation vs Terraform vs Pulumi

**Principle:** Pick the tool whose language model matches your team and whose cloud scope matches your architecture.

**Decision matrix (the book frames it):**
- AWS-only + programming-language team → CDK is the natural fit.
- Multi-cloud or HCL-fluent team → Terraform.
- Multi-cloud + general-purpose-language team → Pulumi.
- Pure JSON/YAML templates without programmatic logic → CloudFormation.

**Do:**
- Recognize that CDK synthesizes to CloudFormation; you can migrate incrementally.
- Use CloudFormation's deployment semantics (change sets, drift detection) under the hood.
- Pick on language ergonomics and tooling, not ideological preferences.

**Don't:**
- Mix CloudFormation templates and CDK code in one stack — pick one path per stack.

*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Comparing AWS CDK with Other IaC Tools"*

---

### Project Layout and CDK Bootstrap

**Principle:** `cdk init` scaffolds the bin/lib/test convention; `cdk bootstrap` creates the asset staging bucket + IAM roles that CDK needs for every deploy.

**Code:**
```bash
mkdir my-first-cdk-app
cd my-first-cdk-app
cdk init app --language typescript

cdk bootstrap    # one-time setup per account/region
cdk synth        # generate CloudFormation template
cdk deploy       # deploy to AWS
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Creating Your First CDK Application" / "Bootstrapping Your CDK Project"*

---

### The First Stack: TypeScript Convention

**Principle:** Every stack extends `cdk.Stack`; resources are children of `this` and pass through `super(scope, id, props)`.

**Code:**
```typescript
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class MyFirstCdkAppStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    new s3.Bucket(this, 'MyFirstBucket', { versioned: true });
  }
}
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Writing Your First CDK Stack"*

---

### Construct Levels — L1, L2, L3

**Principle:** L1 = CloudFormation passthrough, L2 = opinionated with defaults, L3 = multi-resource patterns. Reach for L2/L3 unless you need raw control.

**Code:**
```typescript
// L1: 1:1 CFN resource
new CfnBucket(this, 'MyL1Bucket', { bucketName: 'my-l1-bucket' });

// L2: opinionated defaults, best practices baked in
new Bucket(this, 'MyL2Bucket', {
  bucketName: 'my-l2-bucket',
  versioned: true,
  encryption: BucketEncryption.S3_MANAGED,
});

// L3: pattern that bundles multiple resources
new LambdaRestApi(this, 'MyApi', {
  handler: myFunction,
  // bundles Lambda + API Gateway
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Understanding AWS CDK Construct Levels"*

---

### Stack Fundamentals and Cross-Stack References

**Principle:** Stacks are the deployment unit; they support `addDependency()` for ordering and shared outputs for coupling.

**Do:**
- Treat a stack as the lifecycle boundary — anything in it deploys together.
- Pass resources across stacks through SSM Parameter Store for loose coupling; pass directly via class properties for tight coupling.

**Don't:**
- Encode circular dependencies; CDK will reject them.
- Embed unrelated lifecycles in the same stack.

**Code:**
```typescript
// Producing stack (NetworkStack)
new ssm.StringParameter(this, 'VpcIdParameter', {
  parameterName: '/myapp/vpc-id',
  stringValue: vpc.vpcId,
});

// Consuming stack (ComputeStack)
const vpcId = ssm.StringParameter.valueForStringParameter(this, '/myapp/vpc-id');
const vpc = ec2.Vpc.fromLookup(this, 'ImportedVpc', { vpcId });
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Referencing Resources Across Stacks"*

---

### Multi-Stack Apps: Composition and Boundaries

**Principle:** A CDK App is the root container; stacks become the deployment and ownership units. Group by responsibility, not by resource type.

**Do:**
- One stack per ownership boundary (network, compute, data, frontend).
- Use explicit `addDependency()` for sequencing where CloudFormation cannot infer it.
- Treat multi-stack boundaries as refactor seams — keep them intentional.

**Don't:**
- Reorganize a multi-stack project without revisiting sequencing and outputs.

**Code:**
```typescript
// Stack 1: NetworkStack - defines the VPC
export class NetworkStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc;
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    this.vpc = new ec2.Vpc(this, 'MyVpc', {
      ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
      maxAzs: 3,
    });
  }
}

// Stack 2: ComputeStack - uses the VPC from NetworkStack
export class ComputeStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: cdk.StackProps, vpc: ec2.Vpc) {
    super(scope, id, props);
    new ec2.Instance(this, 'MyInstance', {
      vpc,
      instanceType: new ec2.InstanceType('t3.micro'),
      machineImage: new ec2.AmazonLinuxImage(),
    });
  }
}
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Multi-Stack Apps"*

---

### Environments — Account and Region Scoping

**Principle:** Pin every stack to an `env` (account + region) and use context variables for the things that vary by environment.

**Code:**
```typescript
const app = new cdk.App();
new MyStack(app, 'MyDevStack',  { env: { account: '123456789012', region: 'us-west-2' } });
new MyStack(app, 'MyProdStack', { env: { account: '123456789012', region: 'us-east-1' } });
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Defining Environments"*

---

### Stage-Specific Configurations

**Principle:** Drive environment differences through `process.env`, context variables, or `Stage` constructs — never duplicate stacks.

**Code:**
```typescript
new s3.Bucket(this, 'MyBucket', {
  versioned: process.env.STAGE === 'prod',
  removalPolicy: process.env.STAGE === 'prod'
    ? cdk.RemovalPolicy.RETAIN
    : cdk.RemovalPolicy.DESTROY,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Setting Up Stage-Specific Configurations"*

---

### Resource Identifiers and Logical IDs

**Principle:** CDK auto-generates logical IDs from construct paths with a hash suffix; custom names must be unique within account/region.

**Do:**
- Append `-dev`, `-prod` to environment-specific custom names to avoid collisions.
- Let CDK synthesize default names unless a stable identifier is required.

**Don't:**
- Hard-code physical names that prevent recreation across regions.

**Code:**
```typescript
// Default: auto-named, region-scoped
new s3.Bucket(this, 'MyBucket', { versioned: true });
// Logical ID becomes MyBucketD3F2F16F

// Custom: account/region-scoped for predictability
new s3.Bucket(this, 'MyBucket', {
  bucketName: 'my-bucket-' + this.account,
  versioned: true,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Working with Resource Identifiers"*

---

### CDK Parameters vs Context Variables

**Principle:** Parameters are deployed-time values, context variables are synthesis-time values.

**Do:**
- Use parameters for environment-specific values that vary per account.
- Use context variables for build-time decisions and lookups.
- Move secrets to Secrets Manager; never pass them as parameters.

**Code:**
```typescript
const vpcCidr = new cdk.CfnParameter(this, 'VpcCidr', {
  type: 'String',
  default: '10.0.0.0/16',
});

new ec2.Vpc(this, 'MyVpc', { cidr: vpcCidr.valueAsString });

// CLI override at deploy:
// cdk deploy --parameters VpcCidr=192.168.0.0/16
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Using CDK Parameters"*

---

### Secrets via Secrets Manager (Never Plaintext)

**Principle:** Reference secrets via `Secret.fromSecretNameV2()`; never inline them.

**Code:**
```typescript
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
const dbPassword = secretsmanager.Secret.fromSecretNameV2(this, 'DBPassword', 'my-db-password');

new rds.DatabaseInstance(this, 'MyDatabase', {
  engine: rds.DatabaseInstanceEngine.POSTGRES,
  credentials: rds.Credentials.fromSecret(dbPassword),
  vpc,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Best Practices for Parameter Management"*

---

### Context Variables and Best Practices

**Principle:** Context variables evaluate at synthesis — ideal for region-specific lookups but don't commit sensitive ones.

**Code:**
```json
// cdk.json
{
  "context": {
    "stage": "prod",
    "bucketName": "my-production-bucket",
    "instanceType": "t3.micro"
  }
}
```

```typescript
const instanceType = this.node.tryGetContext('instanceType') || 't2.micro';
new ec2.Instance(this, 'MyInstance', {
  instanceType: new ec2.InstanceType(instanceType),
  machineImage: new ec2.AmazonLinuxImage(),
  vpc,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Using Context to Influence Deployments"*

---

### Environment-Specific Context Selection

**Principle:** Drive stack selection from a context variable so the same codebase yields dev or prod stacks.

**Code:**
```typescript
const environment = app.node.tryGetContext('env');
if (environment === 'prod') {
  new MyProductionStack(app, 'ProdStack');
} else {
  new MyDevelopmentStack(app, 'DevStack');
}
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Example of Environment-Specific Context Management"*

---

### Asset Publishing and Bundling

**Principle:** Use `lambda.Code.fromAsset(path, { bundling: { ... } })` to compile/upload your function code; CDK will manage S3 staging transparently.

**Code:**
```typescript
const myFunction = new lambda.Function(this, 'MyFunction', {
  runtime: lambda.Runtime.NODEJS_14_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset(path.join(__dirname, 'lambda-fn'), {
    bundling: {
      image: lambda.Runtime.NODEJS_14_X.bundlingImage,
      command: ['bash', '-c', 'npm install && npm run build'],
    },
  }),
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Managing Asset Bundles and Files"*

---

### Docker Image Assets for ECS

**Principle:** `ContainerImage.fromAsset()` builds, pushes to ECR, and references the image — all in one construct.

**Code:**
```typescript
const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef');
taskDefinition.addContainer('MyContainer', {
  image: ecs.ContainerImage.fromAsset(path.join(__dirname, 'docker')),
  memoryLimitMiB: 512,
  cpu: 256,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Asset Deployment and Access in AWS"*

---

### Static Site Deployment via S3

**Principle:** Use `s3deploy.BucketDeployment` to upload local files with the right IAM grants baked in.

**Code:**
```typescript
const bucket = new s3.Bucket(this, 'MyBucket');
new s3deploy.BucketDeployment(this, 'DeployWebsite', {
  sources: [s3deploy.Source.asset('./website')],
  destinationBucket: bucket,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Asset Deployment and Access in AWS"*

---

### Feature Flags in CDK

**Principle:** Drive infra-level feature toggles from `tryGetContext`; the construct either exists or doesn't.

**Code:**
```typescript
const enableNewFeature = this.node.tryGetContext('enableNewFeature');
if (enableNewFeature === true) {
  new SomeNewFeatureConstruct(this, 'NewFeature');
} else {
  this.node.addWarning('New Feature is disabled');
}
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Understanding Feature Flags"*

---

### Asset Security — Encryption and Access

**Principle:** Use encryption defaults on every storage construct; restrict S3 grants to specific Lambdas, not wildcard principals.

**Code:**
```typescript
const bucket = new s3.Bucket(this, 'MySecureBucket', {
  encryption: s3.BucketEncryption.S3_MANAGED,
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
});

const role = new iam.Role(this, 'LambdaExecutionRole', {
  assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
  managedPolicies: [
    iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
  ],
});
bucket.grantRead(role);
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Security Aspects of Asset Management"*

---

### VPC Design and CIDR Planning

**Principle:** Allocate a /16 with private ranges, split across public/private/isolated subnets; deploy NAT Gateways per AZ for HA.

**Code:**
```typescript
const vpc = new ec2.Vpc(this, 'MyVPC', {
  ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
  maxAzs: 2,
  natGateways: 2,
  subnetConfiguration: [
    { cidrMask: 24, name: 'Public',   subnetType: ec2.SubnetType.PUBLIC },
    { cidrMask: 24, name: 'Private',  subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
    { cidrMask: 28, name: 'Isolated', subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
  ],
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Designing a Virtual Private Cloud (VPC)" / "Configuring NAT Gateways and Internet Gateways"*

---

### Security Groups and NACLs (Defense in Depth)

**Principle:** Layer Security Groups (stateful, instance-level) and NACLs (stateless, subnet-level). Group rules by application role.

**Code:**
```typescript
const albSG = new ec2.SecurityGroup(this, 'LoadBalancerSG', { vpc });
const appSG = new ec2.SecurityGroup(this, 'AppServerSG',     { vpc });
const dbSG  = new ec2.SecurityGroup(this, 'DbServerSG',      { vpc });

albSG.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'Allow HTTP from internet');
appSG.addIngressRule(albSG, ec2.Port.tcp(80), 'Allow HTTP from load balancer');
dbSG.addIngressRule(appSG, ec2.Port.tcp(3306), 'Allow MySQL from app servers');

const nacl = new ec2.NetworkAcl(this, 'PublicSubnetNACL', {
  vpc,
  subnetSelection: { subnets: vpc.publicSubnets },
});
nacl.addEntry('AllowInboundHTTP', {
  cidr: ec2.AclCidr.anyIpv4(),
  ruleNumber: 100,
  traffic: ec2.AclTraffic.tcpPort(80),
  direction: ec2.TrafficDirection.INGRESS,
  ruleAction: ec2.Action.ALLOW,
});
nacl.addEntry('DenyAllInbound', {
  cidr: ec2.AclCidr.anyIpv4(),
  ruleNumber: 200,
  traffic: ec2.AclTraffic.allTraffic(),
  direction: ec2.TrafficDirection.INGRESS,
  ruleAction: ec2.Action.DENY,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Grouping Security Rules Based on Roles" / "Implementing Network Access Control Lists"*

---

### Cross-Stack Communication via SSM Parameter Store

**Principle:** Use SSM String Parameter Store as the lightweight cross-stack bus; avoids tight coupling and is re-deployable without CFN exports.

**Code:**
```typescript
// NetworkStack produces
new ssm.StringParameter(this, 'VpcIdParameter', {
  parameterName: '/myapp/vpc-id',
  stringValue: vpc.vpcId,
});

// ComputeStack consumes
const vpcId = ssm.StringParameter.valueForStringParameter(this, '/myapp/vpc-id');
const vpc   = ec2.Vpc.fromLookup(this, 'ImportedVpc', { vpcId });
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Using AWS SSM Parameter Store for Cross-Stack Communication"*

---

### EC2 vs Lambda Decision

**Principle:** Lambda for event-driven, sporadic workloads; EC2 for predictable long-running processes with controlled environments.

**Trade-offs (book's framing):**
- Lambda is pay-per-request, has cold starts, scales automatically.
- EC2 is hourly-billed, has predictable performance, requires manual scaling via ASG.
- For hybrid patterns, use ECS/Fargate as the middle ground.

*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Deciding Between EC2 and Lambda"*

---

### RDS vs DynamoDB Decision

**Principle:** RDS for relational/transactional with ACID and SQL; DynamoDB for non-relational, horizontal scale, and event-driven patterns.

**Do:**
- Design DynamoDB partition keys with high cardinality.
- Use RDS Multi-AZ for failover; read replicas for scale-out reads.

**Code (high-level reference):**
```typescript
new rds.DatabaseInstance(this, 'MyDatabase', {
  engine: rds.DatabaseInstanceEngine.POSTGRES,
  vpc,
  multiAZ: true,
  storageEncrypted: true,
  credentials: rds.Credentials.fromSecret(dbSecret),
});

new dynamodb.Table(this, 'MyTable', {
  partitionKey: { name: 'UserID', type: dynamodb.AttributeType.STRING },
  billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
  stream: dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Choosing Between RDS and DynamoDB"*

---

### Deployment Strategies: Blue-Green, Canary, Rolling

**Principle:** L2 patterns (CodeDeploy + Lambda alias or ECS service) bake in blue/green and canary by setting a deployment config.

**Code:**
```typescript
// Lambda blue/green via CodeDeploy with 10% / 5min canary
const deploymentGroup = new codedeploy.LambdaDeploymentGroup(this, 'BlueGreenDeployment', {
  alias: lambdaAlias,
  deploymentConfig: codedeploy.LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES,
});

// ECS canary via CodeDeploy
const ecsService = new ecsPatterns.ApplicationLoadBalancedFargateService(this, 'EcsService', {
  cluster,
  taskDefinition,
});
new codedeploy.EcsDeploymentGroup(this, 'CanaryDeployment', {
  service: ecsService.service,
  deploymentConfig: codedeploy.EcsDeploymentConfig.CANARY_10PERCENT_15MINUTES,
  application: new codedeploy.EcsApplication(this, 'EcsApplication'),
  loadBalancer: ecsService.loadBalancer,
  targetGroups: [ecsService.targetGroup],
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Blue/Green and Canary Deployments"*

---

### CDK Pipelines — Self-Mutating Source-to-Prod

**Principle:** Use `aws-cdk-lib/pipelines.CodePipeline` for self-mutating pipelines; they detect changes to themselves and re-deploy before application stages.

**Code:**
```typescript
import * as cdkp from 'aws-cdk-lib/pipelines';

const pipeline = new cdkp.CodePipeline(this, 'Pipeline', {
  pipelineName: 'MyAppPipeline',
  synth: new cdkp.ShellStep('Synth', {
    input: cdkp.CodePipelineSource.gitHub('my-org/my-repo', 'main'),
    commands: ['npm ci', 'npm run build', 'npx cdk synth'],
  }),
});

// Dev — automatic
pipeline.addStage(new MyApplicationStage(this, 'Dev', {
  env: { account: devAccountId, region: 'us-west-2' },
}));

// Prod — manual approval
const prodStage = pipeline.addStage(new MyApplicationStage(app, 'Prod', {
  env: { account: prodAccountId, region: 'us-east-1' },
}));
prodStage.addPre(new cdkp.ManualApprovalStep('ApproveProductionDeployment'));
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Designing a Standard CI/CD Pipeline" / "Creating Self-Mutating Pipelines"*

---

### Multi-Account Cross-Account Role Assumption

**Principle:** Use a deployment role in the target account with strict conditions; the source account role assumes it.

**Code:**
```typescript
const deployRole = new iam.Role(this, 'CrossAccountDeployRole', {
  assumedBy: new iam.AccountPrincipal('123456789012'),
  roleName: 'MyCrossAccountRole',
  managedPolicies: [
    iam.ManagedPolicy.fromAwsManagedPolicyName('AdministratorAccess'),
  ],
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Cross-Account Role Assumption in AWS for Deployment"*

---

### Pipeline Stage Dependencies via `addPre`

**Principle:** When one microservice depends on another, gate the dependent stage with `addPre(dependencyStage)` to enforce sequencing in the pipeline.

**Code:**
```typescript
const authStage    = new AuthServiceStage(this, 'AuthService', { env: { account: '123456789012', region: 'us-east-1' } });
const orderStage   = new OrderServiceStage(this, 'OrderService', { env: { account: '123456789012', region: 'us-east-1' } });
const authInPipeline    = pipeline.addStage(authStage);
const orderInPipeline   = pipeline.addStage(orderStage);
orderInPipeline.addPre(authInPipeline); // AuthService before OrderService
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Orchestrating Dependencies Between Services in Different Environments"*

---

### Smoke Tests as a Pipeline Stage

**Principle:** Wire `codebuild.PipelineProject` smoke tests as a stage so functional validation gates higher environments.

**Code:**
```typescript
const smokeTestProject = new codebuild.PipelineProject(this, 'SmokeTests', {
  buildSpec: codebuild.BuildSpec.fromObject({
    version: '0.2',
    phases: {
      install: { commands: ['npm install'] },
      build:   { commands: ['npm run smoke-test'] },
    },
  }),
});

pipeline.addStage({
  stageName: 'Test',
  actions: [
    new codepipeline_actions.CodeBuildAction({
      actionName: 'SmokeTests',
      project: smokeTestProject,
      input: sourceOutput,
    }),
  ],
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Incorporating Automated Smoke and Performance Testing"*

---

### Principle of Least Privilege for CDK Bootstrap

**Principle:** Customize the bootstrap role instead of attaching AdministratorAccess.

**Do:**
- Scope the bootstrap role to the services the pipeline actually deploys.
- Restrict the staging bucket to specific VPCs or IP ranges.

**Code:**
```bash
# Bad: over-broad
cdk bootstrap --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess
```

```typescript
// Better: scoped IAM role with explicit policies
const pipelineRole = new iam.Role(this, 'PipelineRole', {
  assumedBy: new iam.ServicePrincipal('codepipeline.amazonaws.com'),
});
pipelineRole.addToPolicy(new iam.PolicyStatement({
  actions: ['cloudformation:CreateStack', 'cloudformation:UpdateStack',
            's3:GetObject', 's3:PutObject'],
  resources: [
    'arn:aws:cloudformation:us-west-2:123456789012:stack/*',
    'arn:aws:s3:::my-artifacts-bucket/*',
  ],
}));
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Leveraging CDK Bootstrap Permissions" / "Securing CI/CD Pipelines for CDK Deployments"*

---

### Least-Privilege IAM Policies — Concrete Patterns

**Principle:** Start with no permissions; add only what the workload needs.

**Code:**
```typescript
// Lambda role: s3 GetObject on a single bucket
const myRole = new iam.Role(this, 'MyFunctionRole', {
  assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
});
myRole.addToPolicy(new iam.PolicyStatement({
  actions: ['s3:GetObject'],
  resources: ['arn:aws:s3:::my-bucket/*'],
}));

// Resource policy: restrict S3 access to one account
bucket.addToResourcePolicy(new iam.PolicyStatement({
  actions: ['s3:GetObject'],
  resources: [`${bucket.bucketArn}/*`],
  principals: [new iam.AccountPrincipal('123456789012')],
}));

// Time-based access policy
const timeBasedPolicy = new iam.PolicyStatement({
  actions: ['ec2:StartInstances', 'ec2:StopInstances'],
  resources: ['*'],
  conditions: {
    DateGreaterThan: { 'aws:CurrentTime': '2024-09-01T00:00:00Z' },
    DateLessThan:    { 'aws:CurrentTime': '2024-09-30T23:59:59Z' },
  },
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Writing Secure IAM Policies in CDK" / "Advanced Conditional IAM Policies"*

---

### Cross-Account Deployment Roles

**Principle:** Source account assumes a scoped role in each target account; never share long-lived keys.

**Code:**
```typescript
const deploymentRole = new iam.Role(this, 'CrossAccountDeploymentRole', {
  assumedBy: new iam.AccountPrincipal('123456789012'), // source account ID
  roleName: 'DeploymentRole',
});
deploymentRole.addToPolicy(new iam.PolicyStatement({
  actions: ['cloudformation:CreateStack', 'cloudformation:UpdateStack', 's3:GetObject'],
  resources: [
    'arn:aws:cloudformation:us-west-2:987654321098:stack/*',
    'arn:aws:s3:::target-account-bucket/*',
  ],
}));
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Cross-Account Deployment Security"*

---

### Encrypted Context Values via Secrets Manager

**Principle:** Pull secrets into the stack via `Secret.fromSecretNameV2`; never store them in `cdk.json`.

**Code:**
```typescript
const secret = secretsmanager.Secret.fromSecretNameV2(this, 'MyApiSecret', 'prod/api-secret');
new rds.DatabaseInstance(this, 'MyDatabase', {
  engine: rds.DatabaseInstanceEngine.postgres({ version: rds.PostgresEngineVersion.VER_13_3 }),
  credentials: rds.Credentials.fromSecret(secret),
  vpc,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Automating Secure Context Values with AWS Secrets Manager"*

---

### Multi-Region Buckets via Context

**Principle:** Compose region name into resource identifiers so the same construct deploys per region cleanly.

**Code:**
```typescript
const region = this.node.tryGetContext('region') || process.env.CDK_DEFAULT_REGION;
new s3.Bucket(this, 'MyRegionalBucket', {
  bucketName: `my-bucket-${region}`,
  removalPolicy: cdk.RemovalPolicy.DESTROY,
  autoDeleteObjects: true,
  encryption: s3.BucketEncryption.S3_MANAGED,
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Handling Multi-Region Contexts"*

---

### cdk-nag — Automated Security Auditing

**Principle:** Add `Aspects.of(app).add(new AwsSolutionsChecks({ verbose: true }))`; gate CI on zero violations.

**Code:**
```typescript
import { AwsSolutionsChecks } from 'cdk-nag';
import { Annotations, Aspects } from 'aws-cdk-lib';

const app = cdk.App();
Aspects.of(app).add(new AwsSolutionsChecks({ verbose: true }));
```

**Suppressing false positives requires justification:**
```typescript
import { NagSuppressions } from 'cdk-nag';
NagSuppressions.addResourceSuppressions(myBucket, [{
  id: 'AwsSolutions-S1',
  reason: 'This bucket hosts a public website; public read is intentional.',
}]);
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Applying cdk-nag Rules to Your CDK Applications" / "Analyzing and Resolving cdk-nag Warnings"*

---

### Unit Testing with `@aws-cdk/assertions`

**Principle:** Unit tests for CDK verify synthesized CloudFormation templates; they are fast, deterministic, and form the bulk of the suite.

**Code:**
```typescript
import { Template } from 'aws-cdk-lib/assertions';

test('S3 bucket has versioning enabled', () => {
  const app = new cdk.App();
  const stack = new MyStack(app, 'TestStack');
  const template = Template.fromStack(stack);
  template.hasResourceProperties('AWS::S3::Bucket', {
    VersioningConfiguration: { Status: 'Enabled' },
  });
  template.resourceCountIs('AWS::S3::Bucket', 1);
});
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Unit Testing CDK Constructs"*

---

### Snapshot Tests and E2E Tests

**Principle:** Use snapshot tests to detect unintended template drift; use E2E tests for real-world behavior in a dedicated account with automated cleanup.

**Do:**
- Keep snapshots in version control.
- Re-accept snapshots only when the change is intentional and reviewed.
- Run E2E in isolated accounts; tear down resources after each run.

**Don't:**
- Update snapshots to silence a failure — they're a regression detector.

*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Snapshot Testing" / "End-to-End (E2E) Testing"*

---

### CI Integration for CDK Tests

**Principle:** Wire Jest + assertions into GitHub Actions (or your CI of choice); test every commit, gate every deploy.

**Code:**
```yaml
name: CDK Test
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with: { node-version: '14' }
      - run: npm install
      - run: npm test
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "External Tools: AWS SAM and Jest" / "CI/CD Pipeline Integration"*

---

### Debugging CDK Applications

**Principle:** Use the construct tree (`node.path`, `node.children`), `cdk diff`, and CloudFormation console events to triage failures.

**Do:**
- Run `cdk ls` to see the deployed topology.
- Use `cdk diff` before `cdk deploy` to confirm intent.
- Inspect CloudFormation stack events for the actual error message.
- Enable verbose mode for nuanced deploy traces.

**Common errors:**
- Insufficient IAM permissions
- Resource limit exceeded
- Circular dependencies between stacks
- Invalid resource configurations
- Naming conflicts

*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Debugging Techniques for CDK Applications"*

---

### Reusable Construct Design Principles

**Principle:** Single responsibility, configurable via props with sensible defaults, outputs as public properties, validated inputs, documented via JSDoc.

**Code:**
```typescript
// VpcConstruct — single responsibility
export class VpcConstruct extends Construct {
  public readonly vpc: ec2.Vpc;
  constructor(scope: Construct, id: string, props: { cidr: string; maxAzs?: number }) {
    super(scope, id);
    if (!/^\d+\.\d+\.\d+\.\d+\/\d+$/.test(props.cidr)) {
      throw new Error(`Invalid CIDR: ${props.cidr}`);
    }
    this.vpc = new ec2.Vpc(this, 'Vpc', {
      ipAddresses: ec2.IpAddresses.cidr(props.cidr),
      maxAzs: props.maxAzs ?? 2,
    });
  }
}
```
*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Developing Reusable Constructs"*

---

### Publishing Constructs as a Library

**Principle:** Use SemVer, peer-dependencies on `aws-cdk-lib`, comprehensive tests, and deprecation warnings for breaking changes.

**Do:**
- Track major versions when construct APIs change.
- Mark a construct `@deprecated` before removal in a release.
- Use `jsii` to multi-publish across languages.

**Don't:**
- Couple construct libraries to specific stack implementations.

*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Versioning and Best Practices for Reusability"*

---

### Choosing L2 vs L3 Patterns

**Principle:** Use L3 when its opinion matches your needs; drop to L2 when you need full control over the underlying resources.

**Example walkthrough (L3 — `ApplicationLoadBalancedFargateService`):**
A single L3 construct creates:
1. ECS cluster
2. Fargate task definition
3. Application Load Balancer with health checks
4. Target group routing to containers
5. CloudWatch log groups
6. IAM roles for task execution

*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "When to Use L3 vs. L2 Constructs"*

---

### Custom Resources for Non-Native Actions

**Principle:** Use `CustomResource` when you need lifecycle hooks (Create/Update/Delete) for actions CloudFormation doesn't natively support (e.g. third-party DNS registration, seeding databases).

**Do:**
- Wrap the Lambda handler with `cr.Provider` for SDK calls.
- Keep custom resource work idempotent and small.

**Don't:**
- Bundle complex application logic into a custom resource.

*Ref: Ultimate_AWS_CDK_for_Infrastructure_Automation_-_Anish_Kumar.md — "Creating and Using Custom Resources"*

---

## Anti-Patterns & Common Mistakes

- **CDK + ad-hoc CloudFormation in the same stack:** two sources of truth → *fix:* pick one path per stack.
- **AdministratorAccess on the bootstrap / pipeline role:** privilege creep → *fix:* scope to specific services with `cdk-nag` enforcing.
- **Inline plaintext secrets in `cdk.json`:** leaked at synthesis → *fix:* use `Secret.fromSecretNameV2()` and pass via context-aware references.
- **Stack pair with circular dependency:** rejected by CDK → *fix:* move shared resources into a separate "foundations" stack both depend on.
- **Wildcard IAM `s3:*` or `resources: ['*']`:** privilege explosion → *fix:* enumerate ARNs and actions.
- **L3 pattern that fights the opinion:** silent weirdness → *fix:* drop to L2/L1 for the specific resources that need it.
- **Snapshot tests "fixed" by updating snapshots:** regression detector silenced → *fix:* treat snapshot churn as a code review event.
- **Self-mutating pipeline with infinite mutation loop:** pipeline thrashes → *fix:* limit mutations to critical stages; gate with explicit versioning.
- **Hard-coded account/region in `cdk synth`:** non-portable → *fix:* pass `env` via stack props; use context for region-specific lookups.
- **Manual resource creation outside CDK:** drift and rework → *fix:* reverse-engineer into IaC; import via CloudFormation `CDKMetadata` and the resource import tool.
- **BucketDeployment with no lifecycle rule:** ever-growing bucket → *fix:* add version expiration or use ECR lifecycle rules for images.

## Decision Heuristics / Checklists

- *Picking an IaC tool?* AWS-only + software team → CDK; multi-cloud → Terraform; HCL-fluent → Terraform; multi-cloud + general languages → Pulumi.
- *Construct level?* Default to L2; reach for L3 when its opinion matches; L1 when you need raw control.
- *Stack boundary?* One per ownership/lifecycle boundary; avoid splitting by resource type.
- *Cross-stack reference?* Default to SSM Parameter Store; pass via props only when co-deployed.
- *Sensitive value?* Secrets Manager; pass via context only when wrapped with a SecureString fetch.
- *IAM policy?* Start with no permissions; add one statement at a time; audit with `cdk-nag`.
- *Test coverage?* Unit + snapshot for every construct; integration for cross-stack; E2E for critical paths.
- *Pipeline strategy?* CDK Pipelines; add manual approval before prod; tag waves for parallel deploys.
- *Deployment strategy?* Lambda/ECS canary for low-risk microservices; blue/green for HA workloads; rolling for stateless fleets.
- *Feature flag in CDK?* `tryGetContext(...)` plus an `if` block that conditionally adds the construct.
- *Multi-region?* Compose region into identifiers; parameterize buckets, lambdas, and routes.

## Key Takeaways

1. **CDK synthesizes to CloudFormation.** You inherit CloudFormation's deployment guarantees while gaining language-first authoring.
2. **L2/L3 constructs encode AWS best practices by default.** Use them first; they are tested, opinionated, and reduce mistakes.
3. **Stack boundaries are refactor seams.** Group by ownership and lifecycle, not by resource type.
4. **Every secret belongs in Secrets Manager.** Reference via `Secret.fromSecretNameV2`; never embed in `cdk.json`.
5. **Bootstrap and pipeline roles need scoped permissions.** Avoid AdministratorAccess; let `cdk-nag` enforce the ceiling.
6. **Unit tests for IaC are non-negotiable.** Use `@aws-cdk/assertions`; form the bulk of the suite with fast unit tests, supplement with E2E.
7. **Self-mutating pipelines require guardrails.** Pair with explicit versioning; never let minor changes trigger deployment churn.
8. **Cross-stack boundaries deserve their own bus.** Prefer SSM Parameter Store; use CFN exports only when co-deployed.
9. **CI/CD validation IS security validation.** Wire `cdk-nag` and `cdk diff` checks into every merge.
10. **Code = documentation.** A typed, doc-commented, tested construct library is the highest-leverage infrastructure document you will ever produce.

## Cross-References

- Related: [[../Terraform_at_Scale.md]] — CDK delegates state to CloudFormation; Terraform owns its own state. Different state-management discipline.
- Related: [[../ansible_for_devops.md]] — Ansible is imperative-YAML configuration, not IaC. Use for runtime configuration that lives above the cloud-control plane.
- Topic index: [[../INDEX.md]]
