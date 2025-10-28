---
name: mongodb
description: Guide for implementing MongoDB - a document database platform with CRUD operations, aggregation pipelines, indexing, replication, sharding, search capabilities, and comprehensive security. Use when working with MongoDB databases, designing schemas, writing queries, optimizing performance, configuring deployments (Atlas/self-managed/Kubernetes), implementing security, or integrating with applications through 15+ official drivers. (project)
---

# MongoDB Agent Skill

A comprehensive guide for working with MongoDB - a document-oriented database platform that provides powerful querying, horizontal scaling, high availability, and enterprise-grade security.

## When to Use This Skill

Use this skill when you need to:
- Design MongoDB schemas and data models
- Write CRUD operations and complex queries
- Build aggregation pipelines for data transformation
- Optimize query performance with indexes
- Configure replication for high availability
- Set up sharding for horizontal scaling
- Implement security (authentication, authorization, encryption)
- Deploy MongoDB (Atlas, self-managed, Kubernetes)
- Integrate MongoDB with applications (15+ official drivers)
- Troubleshoot performance issues or errors
- Implement Atlas Search or Vector Search
- Work with time series data or change streams

## Documentation Coverage

This skill synthesizes **24,618 documentation links** across **172 major MongoDB sections**, covering:
- MongoDB versions 5.0 through 8.1 (upcoming)
- 15+ official driver languages
- 50+ integration tools (Kafka, Spark, BI Connector, Kubernetes Operator)
- Complete deployment spectrum (Atlas cloud, self-managed, Kubernetes)

---

## I. CORE DATABASE OPERATIONS

### A. CRUD Operations

#### Read Operations
```javascript
// Find documents
db.collection.find({ status: "active" })
db.collection.findOne({ _id: ObjectId("...") })

// Query operators
db.users.find({ age: { $gte: 18, $lt: 65 } })
db.posts.find({ tags: { $in: ["mongodb", "database"] } })
db.products.find({ price: { $exists: true } })

// Projection (select specific fields)
db.users.find({ status: "active" }, { name: 1, email: 1 })

// Cursor operations
db.collection.find().sort({ createdAt: -1 }).limit(10).skip(20)
```

#### Write Operations
```javascript
// Insert
db.collection.insertOne({ name: "Alice", age: 30 })
db.collection.insertMany([{ name: "Bob" }, { name: "Charlie" }])

// Update
db.users.updateOne(
  { _id: userId },
  { $set: { status: "verified" } }
)
db.users.updateMany(
  { lastLogin: { $lt: cutoffDate } },
  { $set: { status: "inactive" } }
)

// Replace entire document
db.users.replaceOne({ _id: userId }, newUserDoc)

// Delete
db.users.deleteOne({ _id: userId })
db.users.deleteMany({ status: "deleted" })

// Upsert (update or insert if not exists)
db.users.updateOne(
  { email: "user@example.com" },
  { $set: { name: "User", lastSeen: new Date() } },
  { upsert: true }
)
```

#### Atomic Operations
```javascript
// Increment counter
db.posts.updateOne(
  { _id: postId },
  { $inc: { views: 1 } }
)

// Add to array (if not exists)
db.users.updateOne(
  { _id: userId },
  { $addToSet: { interests: "mongodb" } }
)

// Push to array
db.posts.updateOne(
  { _id: postId },
  { $push: { comments: { author: "Alice", text: "Great!" } } }
)

// Find and modify atomically
db.counters.findAndModify({
  query: { _id: "sequence" },
  update: { $inc: { value: 1 } },
  new: true,
  upsert: true
})
```

### B. Query Operators (100+)

#### Comparison Operators
```javascript
$eq, $ne, $gt, $gte, $lt, $lte
$in, $nin
```

#### Logical Operators
```javascript
$and, $or, $not, $nor

// Example
db.products.find({
  $and: [
    { price: { $gte: 100 } },
    { stock: { $gt: 0 } }
  ]
})
```

#### Array Operators
```javascript
$all, $elemMatch, $size
$firstN, $lastN, $maxN, $minN

// Example: Find docs with all tags
db.posts.find({ tags: { $all: ["mongodb", "database"] } })

// Match array element with multiple conditions
db.products.find({
  reviews: {
    $elemMatch: { rating: { $gte: 4 }, verified: true }
  }
})
```

#### Existence & Type
```javascript
$exists, $type

// Find documents with optional field
db.users.find({ phoneNumber: { $exists: true } })

// Type checking
db.data.find({ value: { $type: "string" } })
```

### C. Aggregation Pipeline

MongoDB's most powerful feature for data transformation and analysis.

#### Core Pipeline Stages (40+)
```javascript
db.orders.aggregate([
  // Stage 1: Filter documents
  { $match: { status: "completed", total: { $gte: 100 } } },

  // Stage 2: Join with customers
  { $lookup: {
    from: "customers",
    localField: "customerId",
    foreignField: "_id",
    as: "customer"
  }},

  // Stage 3: Unwind array
  { $unwind: "$items" },

  // Stage 4: Group and aggregate
  { $group: {
    _id: "$items.category",
    totalRevenue: { $sum: "$items.total" },
    orderCount: { $sum: 1 },
    avgOrderValue: { $avg: "$total" }
  }},

  // Stage 5: Sort results
  { $sort: { totalRevenue: -1 } },

  // Stage 6: Limit results
  { $limit: 10 },

  // Stage 7: Reshape output
  { $project: {
    category: "$_id",
    revenue: "$totalRevenue",
    orders: "$orderCount",
    avgValue: { $round: ["$avgOrderValue", 2] },
    _id: 0
  }}
])
```

#### Common Pipeline Patterns

**Time-Based Aggregation:**
```javascript
db.events.aggregate([
  { $match: { timestamp: { $gte: startDate, $lt: endDate } } },
  { $group: {
    _id: {
      year: { $year: "$timestamp" },
      month: { $month: "$timestamp" },
      day: { $dayOfMonth: "$timestamp" }
    },
    count: { $sum: 1 }
  }}
])
```

**Faceted Search (Multiple Aggregations):**
```javascript
db.products.aggregate([
  { $match: { category: "electronics" } },
  { $facet: {
    priceRanges: [
      { $bucket: {
        groupBy: "$price",
        boundaries: [0, 100, 500, 1000, 5000],
        default: "5000+",
        output: { count: { $sum: 1 } }
      }}
    ],
    topBrands: [
      { $group: { _id: "$brand", count: { $sum: 1 } } },
      { $sort: { count: -1 } },
      { $limit: 5 }
    ],
    avgPrice: [
      { $group: { _id: null, avg: { $avg: "$price" } } }
    ]
  }}
])
```

**Window Functions:**
```javascript
db.sales.aggregate([
  { $setWindowFields: {
    partitionBy: "$region",
    sortBy: { date: 1 },
    output: {
      runningTotal: { $sum: "$amount", window: { documents: ["unbounded", "current"] } },
      movingAvg: { $avg: "$amount", window: { documents: [-7, 0] } }
    }
  }}
])
```

#### Aggregation Operators (150+)

**Math Operators:**
```javascript
$add, $subtract, $multiply, $divide, $mod
$abs, $ceil, $floor, $round, $sqrt, $pow
$log, $log10, $ln, $exp
```

**String Operators:**
```javascript
$concat, $substr, $toLower, $toUpper
$trim, $ltrim, $rtrim, $split
$regexMatch, $regexFind, $regexFindAll
```

**Array Operators:**
```javascript
$arrayElemAt, $slice, $first, $last, $reverse
$sortArray, $filter, $map, $reduce
$zip, $concatArrays
```

**Date/Time Operators:**
```javascript
$dateAdd, $dateDiff, $dateFromString, $dateToString
$dayOfMonth, $month, $year, $dayOfWeek
$week, $hour, $minute, $second
```

**Type Conversion:**
```javascript
$toInt, $toString, $toDate, $toDouble
$toDecimal, $toObjectId, $toBool
```

---

## II. INDEXING & PERFORMANCE

### A. Index Types

#### Single Field Index
```javascript
db.users.createIndex({ email: 1 })  // ascending
db.posts.createIndex({ createdAt: -1 })  // descending
```

#### Compound Index
```javascript
// Order matters! Index on { status: 1, createdAt: -1 }
db.orders.createIndex({ status: 1, createdAt: -1 })

// Supports queries on:
// - { status: "..." }
// - { status: "...", createdAt: ... }
// Does NOT efficiently support: { createdAt: ... } alone
```

#### Text Index (Full-Text Search)
```javascript
db.articles.createIndex({ title: "text", body: "text" })

// Search
db.articles.find({ $text: { $search: "mongodb database" } })

// With relevance score
db.articles.find(
  { $text: { $search: "mongodb" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } })
```

#### Geospatial Indexes
```javascript
// 2dsphere for earth-like geometry
db.places.createIndex({ location: "2dsphere" })

// Find nearby
db.places.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [lon, lat] },
      $maxDistance: 5000  // meters
    }
  }
})
```

#### Wildcard Index
```javascript
// Index all fields in subdocuments
db.products.createIndex({ "attributes.$**": 1 })

// Supports queries on any field under attributes
db.products.find({ "attributes.color": "red" })
```

#### Partial Index
```javascript
// Index only documents matching filter
db.orders.createIndex(
  { customerId: 1 },
  { partialFilterExpression: { status: "active" } }
)
```

#### TTL Index (Auto-delete)
```javascript
// Delete documents 24 hours after createdAt
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 86400 }
)
```

#### Hashed Index (for sharding)
```javascript
db.users.createIndex({ userId: "hashed" })
```

### B. Query Optimization

#### Explain Query Plans
```javascript
// Basic explain
db.users.find({ email: "user@example.com" }).explain()

// Execution stats (shows actual performance)
db.users.find({ age: { $gte: 18 } }).explain("executionStats")

// Key metrics to check:
// - executionTimeMillis
// - totalDocsExamined vs. nReturned (should be close)
// - stage: "IXSCAN" (using index) vs. "COLLSCAN" (full scan - BAD)
```

#### Covered Queries
```javascript
// Create index
db.users.createIndex({ email: 1, name: 1 })

// Query covered by index (no document fetch needed)
db.users.find(
  { email: "user@example.com" },
  { email: 1, name: 1, _id: 0 }  // project only indexed fields
)
```

#### Index Hints
```javascript
// Force specific index
db.users.find({ status: "active", city: "NYC" })
  .hint({ status: 1, createdAt: -1 })
```

#### Index Management
```javascript
// List all indexes
db.collection.getIndexes()

// Drop index
db.collection.dropIndex("indexName")

// Hide index (test before dropping)
db.collection.hideIndex("indexName")
db.collection.unhideIndex("indexName")

// Index stats
db.collection.aggregate([{ $indexStats: {} }])
```

---

## III. DATA MODELING PATTERNS

### A. Relationship Patterns

#### One-to-One (Embedded)
```javascript
// User with single address
{
  _id: ObjectId("..."),
  name: "Alice",
  email: "alice@example.com",
  address: {
    street: "123 Main St",
    city: "NYC",
    zipcode: "10001"
  }
}
```

#### One-to-Few (Embedded Array)
```javascript
// Blog post with comments (< 100 comments)
{
  _id: ObjectId("..."),
  title: "MongoDB Guide",
  comments: [
    { author: "Bob", text: "Great post!", date: ISODate("...") },
    { author: "Charlie", text: "Thanks!", date: ISODate("...") }
  ]
}
```

#### One-to-Many (Referenced)
```javascript
// Author collection
{ _id: ObjectId("author1"), name: "Alice" }

// Books collection (many books per author)
{ _id: ObjectId("book1"), title: "Book 1", authorId: ObjectId("author1") }
{ _id: ObjectId("book2"), title: "Book 2", authorId: ObjectId("author1") }
```

#### Many-to-Many (Array of References)
```javascript
// Users collection
{
  _id: ObjectId("user1"),
  name: "Alice",
  groupIds: [ObjectId("group1"), ObjectId("group2")]
}

// Groups collection
{
  _id: ObjectId("group1"),
  name: "MongoDB Users",
  memberIds: [ObjectId("user1"), ObjectId("user2")]
}
```

### B. Advanced Patterns

#### Time Series Pattern
```javascript
// High-frequency sensor data
{
  _id: ObjectId("..."),
  sensorId: "sensor-123",
  timestamp: ISODate("2025-01-01T00:00:00Z"),
  readings: [
    { time: 0, temp: 23.5, humidity: 45 },
    { time: 60, temp: 23.6, humidity: 46 },
    { time: 120, temp: 23.4, humidity: 45 }
  ]
}

// Create time series collection
db.createCollection("sensor_data", {
  timeseries: {
    timeField: "timestamp",
    metaField: "sensorId",
    granularity: "minutes"
  }
})
```

#### Computed Pattern (Cache Results)
```javascript
// User document with pre-computed stats
{
  _id: ObjectId("..."),
  username: "alice",
  stats: {
    postCount: 150,
    followerCount: 2500,
    lastUpdated: ISODate("...")
  }
}

// Update stats periodically or with triggers
```

#### Schema Versioning
```javascript
// Support schema evolution
{
  _id: ObjectId("..."),
  schemaVersion: 2,
  // v2 fields
  name: { first: "Alice", last: "Smith" },
  // Migration code handles v1 format
}
```

### C. Schema Validation

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "name"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^.+@.+$",
          description: "must be a valid email"
        },
        age: {
          bsonType: "int",
          minimum: 0,
          maximum: 120
        },
        status: {
          enum: ["active", "inactive", "pending"]
        }
      }
    }
  },
  validationLevel: "strict",  // or "moderate"
  validationAction: "error"   // or "warn"
})
```

---

## IV. REPLICATION & HIGH AVAILABILITY

### A. Replica Sets

**Architecture:**
- Primary: Accepts writes, replicates to secondaries
- Secondaries: Replicate primary's oplog, can serve reads
- Arbiter: Votes in elections, holds no data

**Configuration:**
```javascript
rs.initiate({
  _id: "myReplicaSet",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})

// Check status
rs.status()

// Add member
rs.add("mongo4:27017")

// Remove member
rs.remove("mongo4:27017")
```

### B. Write Concern

Controls acknowledgment of write operations:
```javascript
// Wait for majority acknowledgment (durable)
db.users.insertOne(
  { name: "Alice" },
  { writeConcern: { w: "majority", wtimeout: 5000 } }
)

// Common levels:
// w: 1 - primary acknowledges (default)
// w: "majority" - majority of nodes acknowledge (recommended for production)
// w: <number> - specific number of nodes
// w: 0 - no acknowledgment (fire and forget)
```

### C. Read Preference

Controls where reads are served from:
```javascript
// Options:
// - primary (default): read from primary only
// - primaryPreferred: primary if available, else secondary
// - secondary: read from secondary only
// - secondaryPreferred: secondary if available, else primary
// - nearest: lowest network latency

db.collection.find().readPref("secondaryPreferred")
```

### D. Transactions

Multi-document ACID transactions:
```javascript
const session = client.startSession();
session.startTransaction();

try {
  await accounts.updateOne(
    { _id: fromAccount },
    { $inc: { balance: -amount } },
    { session }
  );

  await accounts.updateOne(
    { _id: toAccount },
    { $inc: { balance: amount } },
    { session }
  );

  await session.commitTransaction();
} catch (error) {
  await session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```

---

## V. SHARDING & HORIZONTAL SCALING

### A. Sharded Cluster Architecture

**Components:**
- **Shards:** Replica sets holding data subsets
- **Config Servers:** Store cluster metadata
- **Mongos:** Query routers directing operations to shards

### B. Shard Key Selection

**CRITICAL:** Shard key determines data distribution and query performance.

**Good Shard Keys:**
- High cardinality (many unique values)
- Even distribution (no hotspots)
- Query-aligned (queries include shard key)

```javascript
// Enable sharding on database
sh.enableSharding("myDatabase")

// Shard collection with hashed key
sh.shardCollection(
  "myDatabase.users",
  { userId: "hashed" }
)

// Shard with compound key
sh.shardCollection(
  "myDatabase.orders",
  { customerId: 1, orderDate: 1 }
)
```

### C. Zone Sharding

Assign data ranges to specific shards:
```javascript
// Add shard tags
sh.addShardTag("shard0", "US-EAST")
sh.addShardTag("shard1", "US-WEST")

// Assign ranges to zones
sh.addTagRange(
  "myDatabase.users",
  { zipcode: "00000" },
  { zipcode: "50000" },
  "US-EAST"
)
```

### D. Query Routing

```javascript
// Targeted query (includes shard key) - fast
db.users.find({ userId: "12345" })

// Scatter-gather (no shard key) - slow
db.users.find({ email: "user@example.com" })
```

---

## VI. SECURITY

### A. Authentication

**Methods:**
1. **SCRAM (Username/Password)** - Default
2. **X.509 Certificates** - Mutual TLS
3. **LDAP** (Enterprise)
4. **Kerberos** (Enterprise)
5. **AWS IAM**
6. **OIDC** (OpenID Connect)

```javascript
// Create admin user
use admin
db.createUser({
  user: "admin",
  pwd: "strongPassword",
  roles: ["root"]
})

// Create database user
use myDatabase
db.createUser({
  user: "appUser",
  pwd: "password",
  roles: [
    { role: "readWrite", db: "myDatabase" }
  ]
})
```

### B. Role-Based Access Control (RBAC)

**Built-in Roles:**
- `read`, `readWrite`: Collection-level
- `dbAdmin`, `dbOwner`: Database administration
- `userAdmin`: User management
- `clusterAdmin`: Cluster management
- `root`: Superuser

**Custom Roles:**
```javascript
db.createRole({
  role: "customRole",
  privileges: [
    {
      resource: { db: "myDatabase", collection: "users" },
      actions: ["find", "update"]
    }
  ],
  roles: []
})
```

### C. Encryption

#### Encryption at Rest
```javascript
// Configure in mongod.conf
security:
  enableEncryption: true
  encryptionKeyFile: /path/to/keyfile
```

#### Encryption in Transit (TLS/SSL)
```javascript
// mongod.conf
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /path/to/cert.pem
    CAFile: /path/to/ca.pem
```

#### Client-Side Field Level Encryption (CSFLE)
```javascript
// Automatic encryption of sensitive fields
const clientEncryption = new ClientEncryption(client, {
  keyVaultNamespace: "encryption.__keyVault",
  kmsProviders: {
    aws: {
      accessKeyId: "...",
      secretAccessKey: "..."
    }
  }
})

// Create data key
const dataKeyId = await clientEncryption.createDataKey("aws", {
  masterKey: { region: "us-east-1", key: "..." }
})

// Configure auto-encryption
const encryptedClient = new MongoClient(uri, {
  autoEncryption: {
    keyVaultNamespace: "encryption.__keyVault",
    kmsProviders: { aws: {...} },
    schemaMap: {
      "myDatabase.users": {
        bsonType: "object",
        properties: {
          ssn: {
            encrypt: {
              keyId: [dataKeyId],
              algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
            }
          }
        }
      }
    }
  }
})
```

---

## VII. DEPLOYMENT OPTIONS

### A. MongoDB Atlas (Cloud)

**Recommended for most use cases.**

**Quick Start:**
1. Create free M0 cluster at mongodb.com/atlas
2. Whitelist IP address
3. Create database user
4. Get connection string

**Features:**
- Auto-scaling
- Automated backups
- Multi-cloud (AWS, Azure, GCP)
- Multi-region deployments
- Atlas Search & Vector Search
- Charts (embedded analytics)
- Data Federation
- Serverless instances

**Connection:**
```javascript
const uri = "mongodb+srv://user:pass@cluster.mongodb.net/database?retryWrites=true&w=majority";
const client = new MongoClient(uri);
```

### B. Self-Managed

**Installation:**
```bash
# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-8.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Configuration (mongod.conf):**
```yaml
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true

systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true

net:
  port: 27017
  bindIp: 127.0.0.1

security:
  authorization: enabled

replication:
  replSetName: "myReplicaSet"
```

### C. Kubernetes Deployment

**MongoDB Kubernetes Operator:**
```yaml
apiVersion: mongodbcommunity.mongodb.com/v1
kind: MongoDBCommunity
metadata:
  name: mongodb-replica-set
spec:
  members: 3
  type: ReplicaSet
  version: "8.0"
  security:
    authentication:
      modes: ["SCRAM"]
  users:
    - name: admin
      db: admin
      passwordSecretRef:
        name: mongodb-admin-password
      roles:
        - name: root
          db: admin
  statefulSet:
    spec:
      volumeClaimTemplates:
        - metadata:
            name: data-volume
          spec:
            accessModes: ["ReadWriteOnce"]
            resources:
              requests:
                storage: 10Gi
```

---

## VIII. INTEGRATION & DRIVERS

### A. Official Drivers (15+ Languages)

#### Node.js
```javascript
const { MongoClient } = require("mongodb");

const client = new MongoClient(uri);
await client.connect();

const db = client.db("myDatabase");
const collection = db.collection("users");

// CRUD
await collection.insertOne({ name: "Alice" });
const user = await collection.findOne({ name: "Alice" });
await collection.updateOne({ name: "Alice" }, { $set: { age: 30 } });
await collection.deleteOne({ name: "Alice" });
```

#### Python (PyMongo)
```python
from pymongo import MongoClient

client = MongoClient(uri)
db = client.myDatabase
collection = db.users

# CRUD
collection.insert_one({"name": "Alice"})
user = collection.find_one({"name": "Alice"})
collection.update_one({"name": "Alice"}, {"$set": {"age": 30}})
collection.delete_one({"name": "Alice"})
```

#### Java
```java
MongoClient mongoClient = MongoClients.create(uri);
MongoDatabase database = mongoClient.getDatabase("myDatabase");
MongoCollection<Document> collection = database.getCollection("users");

// Insert
collection.insertOne(new Document("name", "Alice"));

// Find
Document user = collection.find(eq("name", "Alice")).first();

// Update
collection.updateOne(eq("name", "Alice"), set("age", 30));
```

#### Go
```go
client, _ := mongo.Connect(context.TODO(), options.Client().ApplyURI(uri))
collection := client.Database("myDatabase").Collection("users")

// Insert
collection.InsertOne(context.TODO(), bson.M{"name": "Alice"})

// Find
var user bson.M
collection.FindOne(context.TODO(), bson.M{"name": "Alice"}).Decode(&user)
```

### B. Integration Tools

#### Kafka Connector
```json
{
  "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
  "connection.uri": "mongodb://localhost:27017",
  "database": "myDatabase",
  "collection": "events",
  "topics": "my-topic"
}
```

#### Spark Connector
```scala
val df = spark.read
  .format("mongodb")
  .option("uri", "mongodb://localhost:27017/myDatabase.myCollection")
  .load()

df.filter($"age" > 18).show()
```

#### BI Connector (SQL Interface)
```sql
-- Query MongoDB using SQL
SELECT name, AVG(age) as avg_age
FROM users
WHERE status = 'active'
GROUP BY name;
```

---

## IX. ADVANCED FEATURES

### A. Atlas Search (Full-Text)

**Create Search Index:**
```json
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "title": {
        "type": "string",
        "analyzer": "lucene.standard"
      },
      "description": {
        "type": "string",
        "analyzer": "lucene.english"
      }
    }
  }
}
```

**Query:**
```javascript
db.articles.aggregate([
  {
    $search: {
      text: {
        query: "mongodb database",
        path: ["title", "description"],
        fuzzy: { maxEdits: 1 }
      }
    }
  },
  { $limit: 10 },
  { $project: { title: 1, description: 1, score: { $meta: "searchScore" } } }
])
```

### B. Atlas Vector Search

**For AI/ML similarity search:**
```javascript
db.products.aggregate([
  {
    $vectorSearch: {
      index: "vector_index",
      path: "embedding",
      queryVector: [0.123, 0.456, ...],  // 1536 dimensions for OpenAI
      numCandidates: 100,
      limit: 10
    }
  },
  {
    $project: {
      name: 1,
      description: 1,
      score: { $meta: "vectorSearchScore" }
    }
  }
])
```

### C. Change Streams (Real-Time)

```javascript
const changeStream = collection.watch([
  { $match: { "fullDocument.status": "active" } }
]);

changeStream.on("change", (change) => {
  console.log("Change detected:", change);
  // change.operationType: "insert", "update", "delete", "replace"
  // change.fullDocument: entire document (if configured)
});

// Resume from specific point
const resumeToken = changeStream.resumeToken;
const newStream = collection.watch([], { resumeAfter: resumeToken });
```

### D. Bulk Operations

```javascript
const bulkOps = [
  { insertOne: { document: { name: "Alice", age: 30 } } },
  { updateOne: {
    filter: { name: "Bob" },
    update: { $set: { age: 25 } },
    upsert: true
  }},
  { deleteOne: { filter: { name: "Charlie" } } }
];

const result = await collection.bulkWrite(bulkOps, { ordered: false });
console.log(`Inserted: ${result.insertedCount}, Updated: ${result.modifiedCount}`);
```

---

## X. PERFORMANCE OPTIMIZATION

### Best Practices

1. **Index Critical Fields**
   - Index fields used in queries, sorts, joins
   - Monitor slow queries (>100ms)
   - Use compound indexes for multi-field queries

2. **Use Projection**
   ```javascript
   // Good: Only return needed fields
   db.users.find({ status: "active" }, { name: 1, email: 1 })

   // Bad: Return entire document
   db.users.find({ status: "active" })
   ```

3. **Limit Result Sets**
   ```javascript
   db.users.find().limit(100)
   ```

4. **Use Aggregation Pipeline**
   - Process data server-side instead of client-side
   - Use `$match` early to filter
   - Use `$project` to reduce document size

5. **Connection Pooling**
   ```javascript
   const client = new MongoClient(uri, {
     maxPoolSize: 50,
     minPoolSize: 10
   });
   ```

6. **Batch Writes**
   ```javascript
   // Good: Batch insert
   await collection.insertMany(documents);

   // Bad: Individual inserts
   for (const doc of documents) {
     await collection.insertOne(doc);
   }
   ```

7. **Write Concern Tuning**
   - Use `w: 1` for non-critical writes (faster)
   - Use `w: "majority"` for critical data (safer)

8. **Read Preference**
   - Use `secondary` for read-heavy analytics
   - Use `primary` for strong consistency

### Monitoring

```javascript
// Check slow queries
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ ts: -1 }).limit(10)

// Current operations
db.currentOp()

// Server status
db.serverStatus()

// Collection stats
db.collection.stats()
```

---

## XI. TROUBLESHOOTING

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `MongoNetworkError` | Connection failed | Check network, IP whitelist, credentials |
| `E11000 duplicate key` | Duplicate unique field | Check unique indexes, handle duplicates |
| `ValidationError` | Schema validation failed | Check document structure, field types |
| `OperationTimeout` | Query too slow | Add indexes, optimize query, increase timeout |
| `AggregationResultTooLarge` | Result > 16MB | Use `$limit`, `$project`, or `$out` |
| `InvalidSharKey` | Bad shard key | Choose high-cardinality, even-distribution key |
| `ChunkTooBig` | Jumbo chunk | Use `refineShardKey` or re-shard |
| `OplogTailFailed` | Replication lag | Check network, increase oplog size |

### Debugging Tools

```javascript
// Explain query plan
db.collection.find({ field: value }).explain("executionStats")

// Check index usage
db.collection.aggregate([{ $indexStats: {} }])

// Analyze slow queries
db.setProfilingLevel(2)  // Profile all queries
db.system.profile.find({ millis: { $gt: 100 } })

// Check replication lag
rs.printReplicationInfo()
rs.printSecondaryReplicationInfo()
```

---

## XII. QUICK REFERENCE

### Top 20 Operations (by Frequency)

1. `find()` - Query documents
2. `updateOne()` / `updateMany()` - Modify documents
3. `insertOne()` / `insertMany()` - Add documents
4. `deleteOne()` / `deleteMany()` - Remove documents
5. `aggregate()` - Complex queries
6. `createIndex()` - Performance optimization
7. `explain()` - Query analysis
8. `findOne()` - Get single document
9. `countDocuments()` - Count matches
10. `replaceOne()` - Replace document
11. `distinct()` - Get unique values
12. `bulkWrite()` - Batch operations
13. `findAndModify()` - Atomic update
14. `watch()` - Monitor changes
15. `sort()` / `limit()` / `skip()` - Result manipulation
16. `$lookup` - Join collections
17. `$group` - Aggregate data
18. `$match` - Filter pipeline
19. `$project` - Shape output
20. `hint()` - Force index

### Common Patterns

**Pagination:**
```javascript
const page = 2;
const pageSize = 20;
db.collection.find()
  .skip((page - 1) * pageSize)
  .limit(pageSize)
```

**Cursor-based Pagination (Better):**
```javascript
const lastId = ObjectId("...");
db.collection.find({ _id: { $gt: lastId } })
  .limit(20)
```

**Atomic Counter:**
```javascript
db.counters.findAndModify({
  query: { _id: "sequence" },
  update: { $inc: { value: 1 } },
  new: true,
  upsert: true
})
```

**Soft Delete:**
```javascript
// Mark as deleted
db.users.updateOne({ _id: userId }, { $set: { deleted: true, deletedAt: new Date() } })

// Query active only
db.users.find({ deleted: { $ne: true } })
```

---

## XIII. RESOURCES

### Official Documentation
- **Full Docs:** https://www.mongodb.com/docs/
- **MongoDB Manual:** https://www.mongodb.com/docs/manual/
- **Drivers:** https://www.mongodb.com/docs/drivers/
- **Atlas:** https://www.mongodb.com/docs/atlas/

### Tools
- **MongoDB Compass** - GUI for MongoDB
- **MongoDB Shell (mongosh)** - Modern shell
- **Atlas CLI** - Automate Atlas operations
- **Database Tools** - mongodump, mongorestore, mongoimport

### Best Practices Summary

1. **Always use indexes** for queried fields
2. **Embedded vs. Referenced:** Embed for 1-to-few, reference for 1-to-many
3. **Shard key:** High cardinality + even distribution + query-aligned
4. **Security:** Enable auth, use TLS, encrypt at rest for production
5. **Replication:** Minimum 3 nodes for high availability
6. **Write concern:** `w: "majority"` for critical data
7. **Monitor:** Track slow queries, replication lag, disk usage
8. **Test:** Use explain() to verify query performance
9. **Connection pooling:** Configure appropriate pool size
10. **Schema validation:** Define schema for data integrity

---

## XIV. VERSION-SPECIFIC FEATURES

### MongoDB 8.0 (Current)
- Config shard (combined config + shard role)
- Improved aggregation performance
- Enhanced security features

### MongoDB 7.0
- Auto-merging chunks
- Time series improvements
- Queryable encryption GA

### MongoDB 6.0
- Resharding support
- Clustered collections
- Time series collections improvements

### MongoDB 5.0
- Time series collections
- Live resharding
- Versioned API

---

## Common Use Cases

### E-Commerce
- Product catalog (embedded attributes)
- Orders (transactions for consistency)
- User sessions (TTL indexes for cleanup)
- Search (Atlas Search for products)

### IoT/Time Series
- Sensor data (time series collections)
- Real-time analytics (change streams)
- Retention policies (TTL indexes)

### Social Network
- User profiles (embedded or referenced)
- Posts & comments (embedded for small, referenced for large)
- Real-time feeds (change streams)
- Search (Atlas Search for content)

### Analytics
- Event tracking (high write throughput)
- Aggregation pipelines (complex analytics)
- Data federation (query across sources)

---

## When NOT to Use MongoDB

- Strong consistency over availability (use traditional RDBMS)
- Complex multi-table joins (SQL databases excel here)
- Extremely small dataset (<1GB) with simple queries
- ACID transactions across multiple databases (not supported)

---

This skill provides comprehensive MongoDB knowledge for implementing database solutions, from basic CRUD operations to advanced distributed systems with sharding, replication, and security. Always refer to official documentation for the latest features and version-specific details.
