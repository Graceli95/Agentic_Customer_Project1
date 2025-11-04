# AWS Bedrock Setup Guide

**Phase 6: Multi-Provider LLMs - AWS Nova Lite Integration**

This guide walks you through setting up AWS Bedrock with Amazon Nova Lite for cost-effective supervisor routing.

---

## Overview

The supervisor agent now uses **AWS Nova Lite** for intelligent query routing:
- **Cost:** $0.06/1M input tokens (60% cheaper than GPT-4o-mini)
- **Speed:** ~200-400ms latency
- **Perfect for:** Classification and routing tasks
- **Fallback:** Automatically uses OpenAI GPT-4o-mini if Bedrock unavailable

---

## Prerequisites

1. **AWS Account** - [Sign up here](https://aws.amazon.com/) if you don't have one
2. **AWS CLI** - Install from [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
3. **Python 3.9+** with boto3 and langchain-aws installed ✅ (already done)

---

## Step 1: Create AWS IAM User

### 1.1 Create User

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Users** → **Create user**
3. User name: `bedrock-app-user`
4. Check **"Provide user access to the AWS Management Console"** (optional)
5. Click **Next**

### 1.2 Attach Permissions

1. Select **"Attach policies directly"**
2. Search for and select:
   - `AmazonBedrockFullAccess` (or create custom policy below)
3. Click **Next** → **Create user**

### 1.3 Custom IAM Policy (More Secure)

Instead of full access, create a minimal policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

### 1.4 Create Access Keys

1. Click on your new user
2. Go to **Security credentials** tab
3. Scroll to **Access keys**
4. Click **Create access key**
5. Purpose: **Application running outside AWS**
6. Click **Create**
7. **IMPORTANT:** Save these credentials securely!
   - Access Key ID: `AKIA...`
   - Secret Access Key: `...` (only shown once!)

---

## Step 2: Request Model Access

### 2.1 Access Bedrock Console

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Select region: **us-east-1** (recommended) or **us-west-2**

### 2.2 Request Nova Lite Access

1. In left sidebar, click **Model access**
2. Click **Manage model access** (top right)
3. Find **"Amazon Nova Lite"** in the list
4. Check the box next to it
5. Scroll down and click **Request model access**
6. Wait for approval (usually instant, sometimes up to 24 hours)

### 2.3 Verify Access

Once approved, you should see:
- ✅ **Access granted** status for Amazon Nova Lite

---

## Step 3: Configure Credentials

### 3.1 Using AWS CLI (Recommended)

```bash
aws configure
```

Enter when prompted:
```
AWS Access Key ID [None]: AKIA...
AWS Secret Access Key [None]: your-secret-key
Default region name [None]: us-east-1
Default output format [None]: json
```

### 3.2 Using Environment Variables

Add to your `backend/.env` file:

```bash
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your-secret-key-here
AWS_DEFAULT_REGION=us-east-1
```

### 3.3 Verify Configuration

Test your AWS setup:

```bash
# List available Bedrock models
aws bedrock list-foundation-models --region us-east-1 | grep -A 5 "nova-lite"

# Or using Python
python3 << EOF
import boto3
client = boto3.client('bedrock', region_name='us-east-1')
models = client.list_foundation_models()
nova_models = [m for m in models['modelSummaries'] if 'nova' in m['modelId'].lower()]
print(f"Found {len(nova_models)} Nova models")
for model in nova_models:
    print(f"  - {model['modelId']}")
EOF
```

Expected output:
```
Found 3 Nova models
  - us.amazon.nova-micro-v1:0
  - us.amazon.nova-lite-v1:0
  - us.amazon.nova-pro-v1:0
```

---

## Step 4: Test Integration

### 4.1 Start Backend

```bash
cd backend
source venv/bin/activate
python main.py
```

### 4.2 Check Logs

Look for one of these messages:

**✅ Success (AWS Bedrock):**
```
INFO: Attempting to create supervisor with AWS Nova Lite
INFO: ✅ Supervisor created successfully with AWS Nova Lite
```

**⚠️ Fallback (OpenAI):**
```
WARNING: AWS Bedrock unavailable, falling back to OpenAI: ...
INFO: Creating supervisor with OpenAI GPT-4o-mini (fallback)
INFO: ✅ Supervisor created successfully with OpenAI GPT-4o-mini (fallback)
```

### 4.3 Test Query

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need help with a billing issue",
    "session_id": "test-123"
  }'
```

Check logs to see which model handled the request.

---

## Step 5: Monitor Usage & Costs

### 5.1 AWS Bedrock Console

1. Go to [Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Click **Invocations** in left sidebar
3. View usage by model

### 5.2 CloudWatch Metrics

Monitor:
- Invocation count
- Token usage
- Latency
- Errors

### 5.3 Cost Explorer

1. Go to [AWS Cost Explorer](https://console.aws.amazon.com/cost-management/)
2. Filter by service: **Amazon Bedrock**
3. View daily/monthly costs

### 5.4 Expected Costs

**For 10,000 queries/month:**
- Supervisor (Nova Lite): ~$0.24/month
- Workers (GPT-4o-mini): ~$2.55/month
- **Total: ~$2.79/month**

---

## Troubleshooting

### Issue 1: "Access Denied" Error

**Symptom:**
```
ERROR: Could not connect to the endpoint URL
```

**Solutions:**
1. Verify IAM permissions include `bedrock:InvokeModel`
2. Check region is `us-east-1` or `us-west-2`
3. Ensure model access was approved
4. Verify credentials are correct

### Issue 2: "Model Not Found"

**Symptom:**
```
ERROR: Could not find model: us.amazon.nova-lite-v1:0
```

**Solutions:**
1. Request model access in Bedrock console
2. Wait for approval (check email)
3. Verify region supports Nova Lite
4. Try `amazon.nova-lite-v1:0` (without `us.` prefix)

### Issue 3: Falls Back to OpenAI

**Symptom:**
```
WARNING: AWS Bedrock unavailable, falling back to OpenAI
```

**Common Causes:**
1. AWS credentials not set in `.env`
2. Invalid/expired credentials
3. Wrong region (Nova Lite not available)
4. Model access not yet approved
5. Network/firewall blocking AWS

**Debug Steps:**
```bash
# Test AWS credentials
aws sts get-caller-identity

# Test Bedrock access
aws bedrock list-foundation-models --region us-east-1

# Check environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('AWS Key:', os.getenv('AWS_ACCESS_KEY_ID')[:10] + '...' if os.getenv('AWS_ACCESS_KEY_ID') else 'MISSING')"
```

### Issue 4: SSL Certificate Errors

**Symptom:**
```
SSLError: certificate verify failed
```

**Solution:**
```bash
# Update certificates (macOS)
/Applications/Python\ 3.13/Install\ Certificates.command

# Or use environment variable
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

### Issue 5: Rate Limiting

**Symptom:**
```
ERROR: ThrottlingException: Rate exceeded
```

**Solutions:**
1. Request quota increase in AWS console
2. Implement exponential backoff retry
3. Reduce concurrent requests
4. Contact AWS support for higher limits

---

## Model Comparison

| Model | Cost (Input) | Cost (Output) | Speed | Best For |
|-------|-------------|---------------|-------|----------|
| **Nova Lite** | $0.06/1M | $0.24/1M | ~300ms | Routing, classification |
| GPT-4o-mini | $0.15/1M | $0.60/1M | ~400ms | General tasks |
| Claude 3 Haiku | $0.25/1M | $1.25/1M | ~250ms | Fast inference |
| Nova Pro | $0.80/1M | $3.20/1M | ~500ms | Complex reasoning |

---

## Security Best Practices

1. **Never commit credentials** to Git
   - Use `.env` file (already gitignored)
   - Use AWS Secrets Manager for production

2. **Use IAM roles** for EC2/ECS deployments
   - No credentials needed in code
   - Automatic rotation

3. **Rotate access keys** regularly
   - Every 90 days minimum
   - Immediately if compromised

4. **Enable CloudTrail logging**
   - Track all Bedrock API calls
   - Detect suspicious activity

5. **Set spending alerts**
   - AWS Budgets: Set monthly limit
   - Email alerts at 80%, 100% threshold

---

## Alternative: Using OpenAI Only

If you prefer not to use AWS Bedrock, the system will automatically fall back to OpenAI GPT-4o-mini.

To disable Bedrock entirely:

**Option 1: Don't set AWS credentials**
- Leave `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` unset
- System will fall back to OpenAI automatically

**Option 2: Modify supervisor_agent.py**
```python
# Comment out the try block
# supervisor = create_agent(
#     model="bedrock:us.amazon.nova-lite-v1:0",
#     ...
# )

# Keep only the OpenAI version
supervisor = create_agent(
    model="openai:gpt-4o-mini",
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=checkpointer,
    name="supervisor_agent",
)
```

---

## Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon Nova Models](https://aws.amazon.com/bedrock/nova/)
- [LangChain AWS Integration](https://python.langchain.com/docs/integrations/platforms/aws)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Cost Optimization](https://aws.amazon.com/bedrock/pricing/)

---

## Summary

✅ **Completed Setup Steps:**
1. ✅ IAM user created with Bedrock permissions
2. ✅ Access keys generated
3. ✅ Model access requested and approved
4. ✅ Credentials configured in `.env`
5. ✅ Integration tested

**Your supervisor now uses AWS Nova Lite for cost-effective routing!**

**Cost Savings:** 60% cheaper than GPT-4o-mini ($0.06 vs $0.15/1M tokens)

---

**Need Help?** Check the troubleshooting section or open an issue on GitHub.

