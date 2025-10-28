# Shopify GraphQL Admin API - Comprehensive Analysis

**Source:** https://shopify.dev/docs/api/admin-graphql  
**Analysis Date:** 2025-10-25  
**Thoroughness Level:** Very Thorough

---

## Executive Summary

The Shopify GraphQL Admin API is a powerful, modern API that enables developers to build apps and integrations that extend and enhance the Shopify admin experience. It provides efficient, flexible data fetching capabilities with type-safe operations for managing all aspects of a Shopify store.

### Key Highlights
- **GraphQL-based**: Single endpoint with flexible query structure
- **Comprehensive Coverage**: Manages products, orders, customers, inventory, fulfillments, and more
- **Versioned API**: Stable releases with clear deprecation policies
- **Rich Type System**: Strongly-typed schema with introspection support
- **Efficient Data Fetching**: Request only the data you need, reducing over-fetching
- **Batch Operations**: Bulk queries and mutations for large-scale operations
- **Real-time Capabilities**: Webhook integration for event-driven workflows

---

## 1. API Overview

### 1.1 What is the Admin API?

The Shopify Admin API lets you build apps and integrations that extend and enhance the Shopify admin. It provides programmatic access to store data including:
- **Products & Collections**: Product catalog management
- **Orders & Fulfillment**: Order processing and shipping
- **Customers**: Customer data and segmentation
- **Inventory**: Stock management across locations
- **Discounts & Pricing**: Promotional campaigns
- **Store Settings**: Configuration and customization
- **Analytics**: Reporting and metrics

### 1.2 Why GraphQL?

GraphQL offers significant advantages over REST:
- **Single Endpoint**: All queries go to one endpoint
- **Precise Data Fetching**: Request exactly what you need
- **Reduced Network Overhead**: Fewer round trips
- **Strong Typing**: Self-documenting with introspection
- **Nested Relationships**: Fetch related data in one query
- **Versioning**: Backward-compatible evolution

---

## 2. Key Features

### 2.1 Core Capabilities

#### Flexible Querying
```graphql
# Fetch specific fields only
query {
  products(first: 10) {
    edges {
      node {
        id
        title
        variants(first: 5) {
          edges {
            node {
              price
              inventoryQuantity
            }
          }
        }
      }
    }
  }
}
```

#### Mutations for Data Modification
```graphql
mutation {
  productCreate(input: {
    title: "New Product"
    productType: "Apparel"
    vendor: "Acme Corp"
  }) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
```

#### Batch Operations
```graphql
mutation {
  bulkOperationRunQuery(
    query: """
      {
        products {
          edges {
            node {
              id
              title
            }
          }
        }
      }
    """
  ) {
    bulkOperation {
      id
      status
    }
    userErrors {
      field
      message
    }
  }
}
```

### 2.2 Advanced Features

#### Pagination with Cursor-based Navigation
```graphql
query {
  products(first: 50, after: "eyJsYXN0X2lkIjo...") {
    edges {
      cursor
      node {
        id
        title
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
    }
  }
}
```

#### Search and Filtering
```graphql
query {
  products(
    first: 20, 
    query: "product_type:Apparel AND tag:summer"
  ) {
    edges {
      node {
        id
        title
        tags
      }
    }
  }
}
```

#### Metafields for Custom Data
```graphql
mutation {
  productUpdate(input: {
    id: "gid://shopify/Product/123"
    metafields: [
      {
        namespace: "custom"
        key: "fabric_type"
        value: "cotton"
        type: "single_line_text_field"
      }
    ]
  }) {
    product {
      id
      metafields(first: 10) {
        edges {
          node {
            namespace
            key
            value
          }
        }
      }
    }
  }
}
```

---

## 3. Common Operations

### 3.1 Query Operations

#### Product Management
- **List Products**: `products` query with pagination
- **Get Product Details**: `product(id:)` with nested fields
- **Search Products**: Using query parameter with search syntax
- **Product Variants**: Nested variant queries

#### Order Management
- **List Orders**: `orders` query with date/status filters
- **Order Details**: `order(id:)` with line items, customer, shipping
- **Order Fulfillment**: `fulfillmentOrders` for fulfillment workflows
- **Order Transactions**: Payment and transaction history

#### Customer Operations
- **Customer List**: `customers` with segmentation
- **Customer Profile**: `customer(id:)` with orders and addresses
- **Customer Search**: Query-based customer lookup

#### Inventory Management
- **Inventory Levels**: `inventoryItems` across locations
- **Stock Adjustments**: Inventory quantity queries
- **Location Management**: `locations` query

### 3.2 Mutation Operations

#### Product Mutations
```graphql
# Create Product
productCreate(input: ProductInput!)

# Update Product
productUpdate(input: ProductInput!)

# Delete Product
productDelete(input: ProductDeleteInput!)

# Publish Product
productPublish(input: ProductPublishInput!)

# Create Variant
productVariantCreate(input: ProductVariantInput!)

# Bulk Product Updates
productVariantsBulkUpdate(productId: ID!, variants: [ProductVariantsBulkInput!]!)
```

#### Order Mutations
```graphql
# Create Draft Order
draftOrderCreate(input: DraftOrderInput!)

# Complete Draft Order
draftOrderComplete(id: ID!)

# Update Order
orderUpdate(input: OrderInput!)

# Cancel Order
orderCancel(orderId: ID!, reason: OrderCancelReason)

# Create Fulfillment
fulfillmentCreate(input: FulfillmentInput!)

# Add Order Note
orderUpdate(input: { id: ID!, note: String })
```

#### Customer Mutations
```graphql
# Create Customer
customerCreate(input: CustomerInput!)

# Update Customer
customerUpdate(input: CustomerInput!)

# Delete Customer
customerDelete(input: CustomerDeleteInput!)

# Add Customer Address
customerAddressCreate(customerId: ID!, address: MailingAddressInput!)
```

#### Inventory Mutations
```graphql
# Adjust Inventory
inventoryAdjustQuantity(input: InventoryAdjustQuantityInput!)

# Bulk Adjust Inventory
inventoryBulkAdjustQuantityAtLocation(inventoryItemAdjustments: [InventoryAdjustItemInput!]!, locationId: ID!)

# Move Inventory
inventoryMoveQuantity(input: InventoryMoveQuantityInput!)
```

### 3.3 Bulk Operations

For large-scale data operations:

```graphql
# Start Bulk Operation
mutation {
  bulkOperationRunQuery(
    query: """
      {
        products {
          edges {
            node {
              id
              title
              status
            }
          }
        }
      }
    """
  ) {
    bulkOperation {
      id
      status
    }
  }
}

# Check Bulk Operation Status
query {
  node(id: "gid://shopify/BulkOperation/123") {
    ... on BulkOperation {
      id
      status
      errorCode
      objectCount
      url
    }
  }
}
```

---

## 4. API Structure

### 4.1 Type System

#### Object Types
- **Product**: Core product data and relationships
- **Order**: Order information and fulfillment
- **Customer**: Customer profiles and metadata
- **Collection**: Product groupings
- **Fulfillment**: Shipping and tracking
- **InventoryItem**: Stock keeping units
- **Location**: Physical/virtual store locations
- **Shop**: Store-level settings

#### Interface Types
- **Node**: Global ID interface
- **HasMetafields**: Metafield support interface
- **HasPublishedTranslations**: Translation support

#### Scalar Types
- **ID**: Global unique identifier (GID format)
- **String**: Text values
- **Int**: Integer numbers
- **Float**: Decimal numbers
- **Boolean**: True/false
- **DateTime**: ISO 8601 timestamps
- **Money**: Currency amounts
- **URL**: Valid URLs
- **JSON**: Raw JSON data

### 4.2 Connection Pattern

All list queries use Relay-style connections:

```graphql
type ProductConnection {
  edges: [ProductEdge!]!
  pageInfo: PageInfo!
}

type ProductEdge {
  cursor: String!
  node: Product!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### 4.3 Error Handling

#### UserErrors
```graphql
type UserError {
  field: [String!]
  message: String!
}
```

#### System Errors
- **HTTP 429**: Rate limit exceeded
- **HTTP 500**: Server errors
- **HTTP 401**: Authentication failed
- **HTTP 403**: Insufficient permissions

---

## 5. Best Practices

### 5.1 Query Optimization

#### Request Only Needed Fields
```graphql
# Good - Specific fields
query {
  products(first: 10) {
    edges {
      node {
        id
        title
        status
      }
    }
  }
}

# Avoid - Over-fetching
query {
  products(first: 10) {
    edges {
      node {
        id
        title
        description
        vendor
        productType
        tags
        variants(first: 100) {
          edges {
            node {
              id
              price
              sku
              inventoryQuantity
            }
          }
        }
        images(first: 100) {
          edges {
            node {
              url
              altText
            }
          }
        }
      }
    }
  }
}
```

#### Use Pagination Wisely
- Fetch 50-100 items per page for optimal performance
- Use cursor-based pagination for consistency
- Store cursors for resumable operations

#### Batch Related Data
```graphql
# Good - Single query with nested data
query {
  order(id: "gid://shopify/Order/123") {
    id
    name
    customer {
      id
      email
    }
    lineItems(first: 50) {
      edges {
        node {
          title
          quantity
          variant {
            id
            price
          }
        }
      }
    }
  }
}

# Avoid - Multiple separate queries
query {
  order(id: "gid://shopify/Order/123") {
    id
    name
  }
}
# Then separate query for customer
# Then separate query for line items
```

### 5.2 Rate Limiting

#### Understand Rate Limits
- **REST-based**: 40 cost points per second (Basic), 80 (Advanced/Plus)
- **GraphQL Cost Calculation**: Based on query complexity
- **Bucket System**: Points refill over time
- **Throttle Header**: `X-Shopify-Shop-Api-Call-Limit`

#### Cost Calculation
```graphql
query {
  products(first: 10) {  # Cost: ~11 points (1 for query + 10 for items)
    edges {
      node {
        id
        title
        variants(first: 5) {  # Cost: ~5 points per product
          edges {
            node {
              price
            }
          }
        }
      }
    }
  }
}
# Total approximate cost: ~61 points
```

#### Rate Limit Management
```graphql
# Include query cost in response
query {
  products(first: 10) {
    edges {
      node {
        id
      }
    }
  }
}
# Check extensions.cost for actual cost
```

### 5.3 Authentication

#### App Authentication
```bash
# OAuth Access Token in Header
curl -X POST \
  https://your-shop.myshopify.com/admin/api/2024-10/graphql.json \
  -H 'Content-Type: application/json' \
  -H 'X-Shopify-Access-Token: YOUR_ACCESS_TOKEN' \
  -d '{"query": "{ shop { name } }"}'
```

#### API Versioning
- Use stable API versions (e.g., `2024-10`)
- Update to newer versions before deprecation
- Test with release candidate versions

### 5.4 Error Handling Best Practices

```graphql
mutation {
  productCreate(input: {
    title: "New Product"
  }) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
```

Always check:
1. **userErrors**: Business logic errors
2. **HTTP status codes**: System-level errors  
3. **extensions**: Additional metadata

### 5.5 Idempotency

Use idempotency keys for mutations:
```bash
curl -X POST \
  -H 'X-Shopify-Access-Token: TOKEN' \
  -H 'X-Request-Id: unique-request-id-123' \
  -d '{"query": "mutation { ... }"}'
```

---

## 6. Typical Use Cases

### 6.1 E-commerce App Integration

**Product Sync Application**
- Query products from external system
- Create/update products in Shopify
- Sync inventory levels across platforms
- Handle variant mappings

**Order Management System**
- Fetch new orders via webhooks
- Update fulfillment status
- Generate shipping labels
- Send tracking information

### 6.2 Analytics and Reporting

**Sales Dashboard**
- Query orders with date filters
- Aggregate revenue data
- Customer segmentation analysis
- Product performance metrics

### 6.3 Inventory Management

**Multi-location Inventory**
- Track stock across warehouses
- Automate reordering
- Inventory transfers
- Stock level alerts

### 6.4 Customer Relationship Management

**Customer Data Platform**
- Import customer data
- Segment customers by behavior
- Track order history
- Manage customer tags and metadata

### 6.5 Marketing Automation

**Discount Management**
- Create promotional campaigns
- Apply dynamic pricing rules
- Customer-specific discounts
- Bulk discount operations

---

## 7. API Versions and Deprecation

### 7.1 Version Format
- Format: `YYYY-MM` (e.g., `2024-10`)
- New versions quarterly
- Supported for 12 months minimum
- Deprecation announcements well in advance

### 7.2 Version Migration
```graphql
# Specify version in endpoint
POST /admin/api/2024-10/graphql.json

# Check for deprecated fields
query {
  product(id: "gid://shopify/Product/123") {
    title
    # Check API changelog for deprecated fields
  }
}
```

### 7.3 Staying Updated
- Monitor Shopify changelog
- Use latest stable version
- Test with release candidates
- Subscribe to deprecation notices

---

## 8. Tools and SDKs

### 8.1 Official SDKs

#### JavaScript/Node.js
```javascript
const Shopify = require('@shopify/shopify-api');

const client = new Shopify.Clients.Graphql(
  shop,
  accessToken
);

const data = await client.query({
  data: `{
    products(first: 10) {
      edges {
        node {
          id
          title
        }
      }
    }
  }`,
});
```

#### Ruby
```ruby
require 'shopify_api'

ShopifyAPI::Context.setup(
  api_key: "key",
  api_secret_key: "secret",
  scope: "read_products,write_orders",
  host: "shop.myshopify.com"
)

client = ShopifyAPI::Clients::Graphql::Admin.new(
  session: session
)

response = client.query(
  query: "{ products(first: 10) { edges { node { id title } } } }"
)
```

#### Python
```python
import shopify

shopify.Session.setup(
    api_key="key",
    secret="secret"
)

session = shopify.Session(
    "shop.myshopify.com",
    "2024-10",
    access_token
)

shopify.ShopifyResource.activate_session(session)

query = """
{
  products(first: 10) {
    edges {
      node {
        id
        title
      }
    }
  }
}
"""

result = shopify.GraphQL().execute(query)
```

### 8.2 Development Tools

#### GraphiQL Explorer
- Interactive API explorer
- Schema introspection
- Query building interface
- Available in Shopify Partners dashboard

#### Shopify CLI
```bash
# Install Shopify CLI
npm install -g @shopify/cli

# Create app
shopify app create

# Generate GraphQL queries
shopify app generate graphql-query

# Test API calls
shopify app graphql-query
```

### 8.3 Testing Tools

#### GraphQL Playground
- Test queries and mutations
- Save query collections
- Share with team members

#### Postman Collection
- Pre-built API collections
- Environment variables
- Automated testing

---

## 9. Security Considerations

### 9.1 Access Scopes

Define minimal required scopes:
```
read_products
write_products
read_orders
write_orders
read_customers
write_customers
read_inventory
write_inventory
```

### 9.2 Access Token Management
- Store tokens securely (encrypted at rest)
- Use environment variables
- Rotate tokens periodically
- Implement token refresh flow

### 9.3 Data Privacy
- Comply with GDPR/CCPA
- Implement data deletion on request
- Audit data access logs
- Minimize data collection

### 9.4 Webhook Security
```javascript
const crypto = require('crypto');

function verifyWebhook(body, hmacHeader, secret) {
  const hash = crypto
    .createHmac('sha256', secret)
    .update(body, 'utf8')
    .digest('base64');
    
  return hash === hmacHeader;
}
```

---

## 10. Performance Optimization

### 10.1 Query Efficiency

#### Use Aliases for Multiple Queries
```graphql
query {
  featured: products(first: 10, query: "tag:featured") {
    edges {
      node {
        id
        title
      }
    }
  }
  
  new: products(first: 10, query: "created_at:>2024-10-01") {
    edges {
      node {
        id
        title
      }
    }
  }
}
```

#### Fragment Reuse
```graphql
fragment ProductFields on Product {
  id
  title
  status
  vendor
  productType
}

query {
  products(first: 10) {
    edges {
      node {
        ...ProductFields
      }
    }
  }
}
```

### 10.2 Caching Strategies

#### Response Caching
- Cache frequently accessed data
- Use ETags for conditional requests
- Implement cache invalidation

#### Webhook-driven Updates
- Subscribe to relevant webhooks
- Update cache on data changes
- Reduce polling frequency

### 10.3 Bulk Operations Best Practices

```graphql
# For large datasets, use bulk operations
mutation {
  bulkOperationRunQuery(
    query: """
      {
        products {
          edges {
            node {
              id
              title
              variants {
                edges {
                  node {
                    id
                    inventoryQuantity
                  }
                }
              }
            }
          }
        }
      }
    """
  ) {
    bulkOperation {
      id
      status
    }
  }
}

# Poll for completion
query {
  currentBulkOperation {
    id
    status
    errorCode
    createdAt
    completedAt
    objectCount
    fileSize
    url
    partialDataUrl
  }
}
```

---

## 11. Common Patterns

### 11.1 Product Catalog Sync

```graphql
# 1. Fetch all products
query {
  products(first: 250) {
    edges {
      cursor
      node {
        id
        title
        status
        updatedAt
      }
    }
    pageInfo {
      hasNextPage
    }
  }
}

# 2. Update products based on external data
mutation UpdateProduct($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}

# 3. Create new products
mutation CreateProduct($input: ProductInput!) {
  productCreate(input: $input) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
```

### 11.2 Order Fulfillment Workflow

```graphql
# 1. Get unfulfilled orders
query {
  orders(
    first: 50,
    query: "fulfillment_status:unfulfilled"
  ) {
    edges {
      node {
        id
        name
        fulfillmentOrders(first: 10) {
          edges {
            node {
              id
              status
              lineItems(first: 50) {
                edges {
                  node {
                    id
                    remainingQuantity
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

# 2. Create fulfillment
mutation {
  fulfillmentCreateV2(
    fulfillment: {
      lineItemsByFulfillmentOrder: [
        {
          fulfillmentOrderId: "gid://shopify/FulfillmentOrder/123"
          fulfillmentOrderLineItems: [
            {
              id: "gid://shopify/FulfillmentOrderLineItem/456"
              quantity: 2
            }
          ]
        }
      ]
      trackingInfo: {
        company: "UPS"
        number: "1Z999AA10123456784"
        url: "https://www.ups.com/track?tracknum=1Z999AA10123456784"
      }
      notifyCustomer: true
    }
  ) {
    fulfillment {
      id
      status
    }
    userErrors {
      field
      message
    }
  }
}
```

### 11.3 Inventory Management

```graphql
# 1. Check inventory levels
query {
  location(id: "gid://shopify/Location/123") {
    id
    name
    inventoryLevels(first: 250) {
      edges {
        node {
          id
          available
          item {
            id
            sku
          }
        }
      }
    }
  }
}

# 2. Adjust inventory
mutation {
  inventoryAdjustQuantity(
    input: {
      inventoryLevelId: "gid://shopify/InventoryLevel/123?inventory_item_id=456"
      availableDelta: 10
    }
  ) {
    inventoryLevel {
      id
      available
    }
    userErrors {
      field
      message
    }
  }
}

# 3. Set inventory quantity
mutation {
  inventorySetQuantities(
    input: {
      reason: "correction"
      quantities: [
        {
          inventoryItemId: "gid://shopify/InventoryItem/789"
          locationId: "gid://shopify/Location/123"
          quantity: 100
        }
      ]
    }
  ) {
    inventoryAdjustmentGroup {
      createdAt
      reason
      changes {
        name
        delta
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

---

## 12. Troubleshooting

### 12.1 Common Errors

#### Authentication Errors
```json
{
  "errors": [
    {
      "message": "Access denied for field on Shop",
      "extensions": {
        "code": "ACCESS_DENIED",
        "typeName": "Shop"
      }
    }
  ]
}
```
**Solution**: Check access scopes and token validity

#### Rate Limit Errors
```json
{
  "errors": [
    {
      "message": "Throttled",
      "extensions": {
        "code": "THROTTLED"
      }
    }
  ]
}
```
**Solution**: Implement exponential backoff, reduce query complexity

#### Validation Errors
```json
{
  "data": {
    "productCreate": {
      "product": null,
      "userErrors": [
        {
          "field": ["title"],
          "message": "Title can't be blank"
        }
      ]
    }
  }
}
```
**Solution**: Validate input before submission

### 12.2 Debugging Techniques

#### Enable Query Logging
```javascript
const response = await client.query({
  data: query,
  extraHeaders: {
    'X-GraphQL-Cost-Include-Fields': 'true'
  }
});

console.log(response.extensions.cost);
```

#### Use GraphiQL for Testing
- Test queries interactively
- View schema documentation
- Check field deprecation warnings

#### Monitor API Calls
```javascript
// Log all requests
client.on('request', (req) => {
  console.log('Request:', req);
});

client.on('response', (res) => {
  console.log('Response:', res);
  console.log('Rate Limit:', res.headers['x-shopify-shop-api-call-limit']);
});
```

---

## 13. Resources and Further Learning

### 13.1 Official Documentation
- Shopify GraphQL Admin API Reference: https://shopify.dev/docs/api/admin-graphql
- GraphQL Learning: https://shopify.dev/docs/apps/build/graphql
- API Versioning: https://shopify.dev/docs/api/usage/versioning
- Rate Limits: https://shopify.dev/docs/api/usage/rate-limits

### 13.2 Developer Tools
- Shopify Partners Dashboard: https://partners.shopify.com
- GraphiQL App: https://shopify-graphiql-app.shopifycloud.com
- Shopify CLI: https://shopify.dev/docs/api/shopify-cli

### 13.3 Community Resources
- Shopify Community Forums: https://community.shopify.com
- Shopify Developer Slack: https://shopifydevs.slack.com
- Stack Overflow: Tag `shopify` + `graphql`

### 13.4 Example Applications
- Shopify App Templates: https://github.com/Shopify/shopify-app-template-node
- Sample Apps: https://github.com/Shopify/example-apps

---

## 14. Conclusion

The Shopify GraphQL Admin API provides a comprehensive, efficient, and developer-friendly way to interact with Shopify stores. By following best practices and leveraging the API's powerful features, developers can build robust, scalable applications that enhance the Shopify ecosystem.

### Key Takeaways:
1. **Start Simple**: Begin with basic queries and gradually add complexity
2. **Optimize Early**: Consider query costs and pagination from the start
3. **Handle Errors Gracefully**: Implement proper error handling and retry logic
4. **Stay Updated**: Follow API versioning and deprecation guidelines
5. **Use Official SDKs**: Leverage battle-tested libraries when possible
6. **Monitor Performance**: Track API usage and optimize bottlenecks
7. **Security First**: Protect access tokens and implement proper authentication
8. **Test Thoroughly**: Use GraphiQL and test environments before production

### Next Steps:
1. Review the API reference documentation
2. Set up a development store
3. Generate API credentials
4. Build a proof-of-concept integration
5. Implement production-ready error handling
6. Deploy and monitor in production

---

## Appendix A: Quick Reference

### A.1 Essential Queries

```graphql
# Shop Information
{ shop { name email } }

# Products
{ products(first: 10) { edges { node { id title } } } }

# Orders
{ orders(first: 10) { edges { node { id name } } } }

# Customers
{ customers(first: 10) { edges { node { id email } } } }

# Inventory
{ inventoryItems(first: 10) { edges { node { id sku } } } }
```

### A.2 Essential Mutations

```graphql
# Create Product
productCreate(input: {title: "Product"})

# Update Product
productUpdate(input: {id: "gid://shopify/Product/123", title: "Updated"})

# Create Order
draftOrderCreate(input: {lineItems: [{variantId: "gid://shopify/ProductVariant/123", quantity: 1}]})

# Fulfill Order
fulfillmentCreateV2(fulfillment: {...})

# Adjust Inventory
inventoryAdjustQuantity(input: {inventoryLevelId: "...", availableDelta: 10})
```

### A.3 Common Query Parameters

- `first: Int`: Limit results (max 250)
- `after: String`: Cursor for pagination
- `query: String`: Search/filter string
- `reverse: Boolean`: Reverse sort order
- `sortKey: String`: Sort field

### A.4 HTTP Headers

```
Content-Type: application/json
X-Shopify-Access-Token: YOUR_ACCESS_TOKEN
X-Shopify-Storefront-Access-Token: (for Storefront API)
X-Request-Id: unique-id-for-idempotency
X-Shopify-Api-Version: 2024-10
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-25  
**Maintained By:** Claude Code - API Research Team
