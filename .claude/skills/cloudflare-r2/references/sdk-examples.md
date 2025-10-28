# Cloudflare R2 SDK Examples

Comprehensive examples for all supported SDKs and tools.

## Table of Contents
- AWS CLI
- AWS SDK JavaScript v3
- AWS SDK Python (Boto3)
- AWS SDK Go v2
- AWS SDK Java
- AWS SDK .NET
- AWS SDK PHP
- AWS SDK Ruby
- AWS SDK Rust
- Rclone
- Terraform

## Prerequisites

All SDKs require:
- **Access Key ID** and **Secret Access Key** from Cloudflare dashboard
- **Account ID** from Cloudflare dashboard
- **Endpoint:** `https://<account-id>.r2.cloudflarestorage.com`
- **Region:** `auto` (or specific: `wnam`, `enam`, `weur`, `eeur`, `apac`)

---

## AWS CLI

**Installation:** https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

### Configuration

```bash
aws configure
# AWS Access Key ID: <your-access-key-id>
# AWS Secret Access Key: <your-secret-access-key>
# Default region name: auto
# Default output format: json
```

### Common Operations

**List buckets:**
```bash
aws s3api list-buckets \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
```

**Create bucket:**
```bash
aws s3api create-bucket \
  --bucket my-bucket \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
```

**Upload file:**
```bash
aws s3 cp file.txt s3://my-bucket/ \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
```

**Upload with metadata:**
```bash
aws s3 cp file.txt s3://my-bucket/ \
  --metadata '{"author":"John","version":"1.0"}' \
  --content-type "text/plain" \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
```

**Download file:**
```bash
aws s3 cp s3://my-bucket/file.txt ./downloaded.txt \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
```

**List objects:**
```bash
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --prefix uploads/ \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
```

**Delete object:**
```bash
aws s3 rm s3://my-bucket/file.txt \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
```

**Generate presigned URL (read):**
```bash
aws s3 presign s3://my-bucket/file.txt \
  --expires-in 3600 \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
```

**Sync directory:**
```bash
aws s3 sync ./local-dir s3://my-bucket/remote-dir/ \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
```

**Multipart upload (automatic for large files):**
```bash
aws s3 cp large-file.mp4 s3://my-bucket/ \
  --endpoint-url https://<accountid>.r2.cloudflarestorage.com
# AWS CLI automatically uses multipart for files >8MB
```

### Shell Alias (Convenience)

```bash
# Add to ~/.bashrc or ~/.zshrc
alias r2='aws s3 --endpoint-url https://<accountid>.r2.cloudflarestorage.com'

# Usage
r2 ls s3://my-bucket/
r2 cp file.txt s3://my-bucket/
```

---

## AWS SDK JavaScript v3 (Node.js)

**Installation:**
```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

### Configuration

```javascript
import { S3Client } from "@aws-sdk/client-s3";

const ACCOUNT_ID = process.env.R2_ACCOUNT_ID;
const ACCESS_KEY_ID = process.env.R2_ACCESS_KEY_ID;
const SECRET_ACCESS_KEY = process.env.R2_SECRET_ACCESS_KEY;

const s3 = new S3Client({
  region: "auto",
  endpoint: `https://${ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: ACCESS_KEY_ID,
    secretAccessKey: SECRET_ACCESS_KEY,
  },
});
```

### Common Operations

**List buckets:**
```javascript
import { ListBucketsCommand } from "@aws-sdk/client-s3";

const { Buckets } = await s3.send(new ListBucketsCommand({}));
console.log(Buckets);
```

**Create bucket:**
```javascript
import { CreateBucketCommand } from "@aws-sdk/client-s3";

await s3.send(new CreateBucketCommand({
  Bucket: "my-bucket",
}));
```

**Upload object:**
```javascript
import { PutObjectCommand } from "@aws-sdk/client-s3";
import fs from "fs";

const fileContent = fs.readFileSync("./file.txt");

await s3.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "uploads/file.txt",
  Body: fileContent,
  ContentType: "text/plain",
  Metadata: {
    author: "John Doe",
    version: "1.0",
  },
}));
```

**Upload with custom metadata:**
```javascript
await s3.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "photo.jpg",
  Body: imageBuffer,
  ContentType: "image/jpeg",
  CacheControl: "public, max-age=31536000",
  Metadata: {
    uploadedBy: userId,
    uploadDate: new Date().toISOString(),
  },
}));
```

**Download object:**
```javascript
import { GetObjectCommand } from "@aws-sdk/client-s3";

const { Body, ContentType } = await s3.send(new GetObjectCommand({
  Bucket: "my-bucket",
  Key: "file.txt",
}));

// Convert stream to string
const text = await Body.transformToString();
console.log(text);
```

**Stream download to file:**
```javascript
import { pipeline } from "stream/promises";
import { createWriteStream } from "fs";

const { Body } = await s3.send(new GetObjectCommand({
  Bucket: "my-bucket",
  Key: "large-file.mp4",
}));

await pipeline(Body, createWriteStream("./downloaded.mp4"));
```

**List objects:**
```javascript
import { ListObjectsV2Command } from "@aws-sdk/client-s3";

const { Contents } = await s3.send(new ListObjectsV2Command({
  Bucket: "my-bucket",
  Prefix: "uploads/",
  MaxKeys: 100,
}));

for (const object of Contents) {
  console.log(object.Key, object.Size);
}
```

**Paginated listing:**
```javascript
let ContinuationToken;

do {
  const response = await s3.send(new ListObjectsV2Command({
    Bucket: "my-bucket",
    ContinuationToken,
  }));

  for (const obj of response.Contents) {
    console.log(obj.Key);
  }

  ContinuationToken = response.NextContinuationToken;
} while (ContinuationToken);
```

**Delete object:**
```javascript
import { DeleteObjectCommand } from "@aws-sdk/client-s3";

await s3.send(new DeleteObjectCommand({
  Bucket: "my-bucket",
  Key: "file.txt",
}));
```

**Delete multiple objects:**
```javascript
import { DeleteObjectsCommand } from "@aws-sdk/client-s3";

await s3.send(new DeleteObjectsCommand({
  Bucket: "my-bucket",
  Delete: {
    Objects: [
      { Key: "file1.txt" },
      { Key: "file2.txt" },
      { Key: "file3.txt" },
    ],
  },
}));
```

**Generate presigned URL (read):**
```javascript
import { GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const url = await getSignedUrl(
  s3,
  new GetObjectCommand({
    Bucket: "my-bucket",
    Key: "file.txt",
  }),
  { expiresIn: 3600 }  // 1 hour
);

console.log("Download URL:", url);
```

**Generate presigned URL (write):**
```javascript
import { PutObjectCommand } from "@aws-sdk/client-s3";

const uploadUrl = await getSignedUrl(
  s3,
  new PutObjectCommand({
    Bucket: "my-bucket",
    Key: "user-upload.jpg",
    ContentType: "image/jpeg",
  }),
  { expiresIn: 1800 }  // 30 minutes
);

// Client uploads via PUT
// fetch(uploadUrl, { method: 'PUT', body: fileData });
```

**Multipart upload:**
```javascript
import {
  CreateMultipartUploadCommand,
  UploadPartCommand,
  CompleteMultipartUploadCommand,
} from "@aws-sdk/client-s3";

// 1. Create multipart upload
const { UploadId } = await s3.send(new CreateMultipartUploadCommand({
  Bucket: "my-bucket",
  Key: "large-file.mp4",
  ContentType: "video/mp4",
}));

// 2. Upload parts (5MB - 5GB each)
const part1 = await s3.send(new UploadPartCommand({
  Bucket: "my-bucket",
  Key: "large-file.mp4",
  UploadId,
  PartNumber: 1,
  Body: chunk1,
}));

const part2 = await s3.send(new UploadPartCommand({
  Bucket: "my-bucket",
  Key: "large-file.mp4",
  UploadId,
  PartNumber: 2,
  Body: chunk2,
}));

// 3. Complete upload
await s3.send(new CompleteMultipartUploadCommand({
  Bucket: "my-bucket",
  Key: "large-file.mp4",
  UploadId,
  MultipartUpload: {
    Parts: [
      { PartNumber: 1, ETag: part1.ETag },
      { PartNumber: 2, ETag: part2.ETag },
    ],
  },
}));
```

---

## AWS SDK Python (Boto3)

**Installation:**
```bash
pip install boto3
```

### Configuration

**Method 1: Explicit credentials**
```python
import boto3

ACCOUNT_ID = "your-account-id"
ACCESS_KEY_ID = "your-access-key-id"
SECRET_ACCESS_KEY = "your-secret-access-key"

s3 = boto3.client(
    service_name="s3",
    endpoint_url=f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name="auto",
)
```

**Method 2: Environment variables**
```python
import boto3
import os

# Set: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
)
```

**Method 3: Resource interface**
```python
s3_resource = boto3.resource(
    "s3",
    endpoint_url=f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
)
```

### Common Operations

**List buckets:**
```python
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])
```

**Create bucket:**
```python
s3.create_bucket(Bucket="my-bucket")
```

**Upload file:**
```python
s3.upload_file("local-file.txt", "my-bucket", "remote-file.txt")
```

**Upload from bytes:**
```python
import io

file_content = b"Hello, World!"
s3.upload_fileobj(
    io.BytesIO(file_content),
    "my-bucket",
    "file.txt",
    ExtraArgs={"ContentType": "text/plain"}
)
```

**Upload with metadata:**
```python
s3.put_object(
    Bucket="my-bucket",
    Key="photo.jpg",
    Body=image_data,
    ContentType="image/jpeg",
    Metadata={
        "author": "John Doe",
        "upload-date": "2024-01-15",
    },
    CacheControl="public, max-age=31536000",
)
```

**Download file:**
```python
s3.download_file("my-bucket", "file.txt", "./local-file.txt")
```

**Download to memory:**
```python
import io

buffer = io.BytesIO()
s3.download_fileobj("my-bucket", "file.txt", buffer)
content = buffer.getvalue()
```

**Get object info:**
```python
response = s3.head_object(Bucket="my-bucket", Key="file.txt")
print(f"Size: {response['ContentLength']} bytes")
print(f"Type: {response['ContentType']}")
print(f"Metadata: {response.get('Metadata', {})}")
```

**List objects:**
```python
response = s3.list_objects_v2(Bucket="my-bucket", Prefix="uploads/")
for obj in response.get("Contents", []):
    print(f"{obj['Key']}: {obj['Size']} bytes")
```

**Paginated listing:**
```python
paginator = s3.get_paginator("list_objects_v2")
pages = paginator.paginate(Bucket="my-bucket", Prefix="logs/")

for page in pages:
    for obj in page.get("Contents", []):
        print(obj["Key"])
```

**Delete object:**
```python
s3.delete_object(Bucket="my-bucket", Key="file.txt")
```

**Delete multiple objects:**
```python
s3.delete_objects(
    Bucket="my-bucket",
    Delete={
        "Objects": [
            {"Key": "file1.txt"},
            {"Key": "file2.txt"},
            {"Key": "file3.txt"},
        ]
    }
)
```

**Generate presigned URL:**
```python
url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": "my-bucket", "Key": "file.txt"},
    ExpiresIn=3600,  # 1 hour
)
print(f"Download URL: {url}")
```

**Multipart upload (automatic):**
```python
# Boto3 automatically uses multipart for large files
s3.upload_file(
    "large-video.mp4",
    "my-bucket",
    "videos/video.mp4",
    Config=boto3.s3.transfer.TransferConfig(
        multipart_threshold=100 * 1024 * 1024,  # 100MB
        multipart_chunksize=100 * 1024 * 1024,  # 100MB chunks
    )
)
```

**Manual multipart upload:**
```python
# 1. Create multipart upload
mpu = s3.create_multipart_upload(
    Bucket="my-bucket",
    Key="large-file.mp4",
    ContentType="video/mp4",
)
upload_id = mpu["UploadId"]

# 2. Upload parts
parts = []
for i, chunk in enumerate(file_chunks, start=1):
    part = s3.upload_part(
        Bucket="my-bucket",
        Key="large-file.mp4",
        UploadId=upload_id,
        PartNumber=i,
        Body=chunk,
    )
    parts.append({"PartNumber": i, "ETag": part["ETag"]})

# 3. Complete upload
s3.complete_multipart_upload(
    Bucket="my-bucket",
    Key="large-file.mp4",
    UploadId=upload_id,
    MultipartUpload={"Parts": parts},
)
```

---

## AWS SDK Go v2

**Installation:**
```bash
go get github.com/aws/aws-sdk-go-v2/aws
go get github.com/aws/aws-sdk-go-v2/config
go get github.com/aws/aws-sdk-go-v2/credentials
go get github.com/aws/aws-sdk-go-v2/service/s3
```

### Configuration

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/aws/aws-sdk-go-v2/aws"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/credentials"
    "github.com/aws/aws-sdk-go-v2/service/s3"
)

func createClient() (*s3.Client, error) {
    accountID := os.Getenv("R2_ACCOUNT_ID")
    accessKeyID := os.Getenv("R2_ACCESS_KEY_ID")
    secretAccessKey := os.Getenv("R2_SECRET_ACCESS_KEY")

    cfg, err := config.LoadDefaultConfig(context.TODO(),
        config.WithCredentialsProvider(
            credentials.NewStaticCredentialsProvider(
                accessKeyID,
                secretAccessKey,
                "",
            ),
        ),
        config.WithRegion("auto"),
    )
    if err != nil {
        return nil, err
    }

    client := s3.NewFromConfig(cfg, func(o *s3.Options) {
        o.BaseEndpoint = aws.String(
            fmt.Sprintf("https://%s.r2.cloudflarestorage.com", accountID),
        )
    })

    return client, nil
}
```

### Common Operations

**List buckets:**
```go
output, err := client.ListBuckets(context.TODO(), &s3.ListBucketsInput{})
if err != nil {
    log.Fatal(err)
}

for _, bucket := range output.Buckets {
    fmt.Println(*bucket.Name)
}
```

**Upload object:**
```go
file, err := os.Open("file.txt")
if err != nil {
    log.Fatal(err)
}
defer file.Close()

_, err = client.PutObject(context.TODO(), &s3.PutObjectInput{
    Bucket:      aws.String("my-bucket"),
    Key:         aws.String("uploads/file.txt"),
    Body:        file,
    ContentType: aws.String("text/plain"),
})
```

**Download object:**
```go
output, err := client.GetObject(context.TODO(), &s3.GetObjectInput{
    Bucket: aws.String("my-bucket"),
    Key:    aws.String("file.txt"),
})
if err != nil {
    log.Fatal(err)
}
defer output.Body.Close()

data, err := io.ReadAll(output.Body)
fmt.Println(string(data))
```

**List objects:**
```go
output, err := client.ListObjectsV2(context.TODO(), &s3.ListObjectsV2Input{
    Bucket: aws.String("my-bucket"),
    Prefix: aws.String("uploads/"),
})

for _, object := range output.Contents {
    fmt.Printf("%s: %d bytes\n", *object.Key, object.Size)
}
```

**Generate presigned URL:**
```go
import "github.com/aws/aws-sdk-go-v2/service/s3"

presignClient := s3.NewPresignClient(client)

presignResult, err := presignClient.PresignPutObject(context.TODO(),
    &s3.PutObjectInput{
        Bucket: aws.String("my-bucket"),
        Key:    aws.String("upload.txt"),
    },
    s3.WithPresignExpires(time.Hour),
)

fmt.Printf("Upload URL: %s\n", presignResult.URL)
```

---

## Rclone

**Installation:** https://rclone.org/install/

### Configuration

**Interactive:**
```bash
rclone config
# n (new remote)
# name: r2
# Storage: Amazon S3 Compliant
# Provider: Cloudflare R2
# Enter credentials
```

**Manual (`~/.config/rclone/rclone.conf`):**
```ini
[r2]
type = s3
provider = Cloudflare
access_key_id = your-access-key-id
secret_access_key = your-secret-access-key
endpoint = https://your-account-id.r2.cloudflarestorage.com
acl = private
```

**For object-level tokens:**
```ini
[r2]
type = s3
provider = Cloudflare
access_key_id = your-access-key-id
secret_access_key = your-secret-access-key
endpoint = https://your-account-id.r2.cloudflarestorage.com
no_check_bucket = true
```

### Common Operations

**List buckets:**
```bash
rclone lsd r2:
```

**List objects:**
```bash
rclone ls r2:my-bucket
rclone tree r2:my-bucket
```

**Upload file:**
```bash
rclone copy file.txt r2:my-bucket/uploads/
```

**Upload directory:**
```bash
rclone copy ./local-dir r2:my-bucket/remote-dir/ --progress
```

**Upload large files (optimized):**
```bash
rclone copy large-video.mp4 r2:my-bucket/ \
  --s3-upload-cutoff=100M \
  --s3-chunk-size=100M \
  --progress
```

**Download file:**
```bash
rclone copy r2:my-bucket/file.txt ./
```

**Sync directories:**
```bash
# Local to R2
rclone sync ./local-dir r2:my-bucket/backup/

# R2 to local
rclone sync r2:my-bucket/backup/ ./local-dir
```

**Delete file:**
```bash
rclone delete r2:my-bucket/file.txt
```

**Generate presigned URL:**
```bash
rclone link r2:my-bucket/file.txt --expire 3600
```

**Check differences:**
```bash
rclone check ./local-dir r2:my-bucket/remote-dir/
```

**Mount R2 as filesystem (Linux/macOS):**
```bash
rclone mount r2:my-bucket /mnt/r2 --daemon
```

### Performance Tuning

```bash
rclone copy large-files/ r2:my-bucket/ \
  --transfers=16 \
  --checkers=32 \
  --s3-chunk-size=100M \
  --s3-upload-cutoff=100M \
  --progress
```

- `--transfers`: Parallel file uploads
- `--checkers`: Parallel existence checks
- `--s3-chunk-size`: Multipart chunk size
- `--s3-upload-cutoff`: Multipart threshold

---

## Terraform

**Installation:** https://www.terraform.io/downloads

### Cloudflare Provider (Bucket Management)

**main.tf:**
```hcl
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

variable "cloudflare_api_token" {
  type      = string
  sensitive = true
}

variable "account_id" {
  type = string
}

resource "cloudflare_r2_bucket" "main" {
  account_id = var.account_id
  name       = "my-terraform-bucket"
  location   = "WNAM"  # WNAM, ENAM, WEUR, EEUR, APAC
}

output "bucket_name" {
  value = cloudflare_r2_bucket.main.name
}
```

**terraform.tfvars:**
```hcl
cloudflare_api_token = "your-cloudflare-api-token"
account_id           = "your-account-id"
```

**Commands:**
```bash
terraform init
terraform plan
terraform apply
terraform destroy
```

### AWS Provider (CORS, Lifecycle, Objects)

For CORS and lifecycle configuration, use AWS provider:

**main.tf:**
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = "auto"
  access_key = var.r2_access_key_id
  secret_key = var.r2_secret_access_key

  skip_credentials_validation = true
  skip_region_validation      = true
  skip_requesting_account_id  = true

  endpoints {
    s3 = "https://${var.account_id}.r2.cloudflarestorage.com"
  }
}

resource "aws_s3_bucket_cors_configuration" "main" {
  bucket = "my-bucket"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST"]
    allowed_origins = ["https://example.com"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3600
  }
}
```

---

## SDK Comparison

| SDK | Language | Presigned URLs | Multipart | Auto Multipart |
|-----|----------|----------------|-----------|----------------|
| AWS CLI | Shell | Yes (read) | Manual | Yes (>8MB) |
| JS v3 | JavaScript | Yes (both) | Manual | No |
| Boto3 | Python | Yes | Manual | Yes (configurable) |
| Go v2 | Go | Yes | Manual | No |
| Rclone | CLI | Yes (read) | Yes | Yes (configurable) |
| Terraform | HCL | N/A | N/A | N/A |

## Best Practices

1. **Use environment variables** for credentials
2. **Enable multipart** for files >100MB
3. **Implement retry logic** with exponential backoff
4. **Stream large files** instead of buffering
5. **Validate checksums** for critical uploads
6. **Use Rclone** for bulk operations
7. **Set reasonable timeouts** for SDK clients
8. **Handle errors gracefully** with proper logging
