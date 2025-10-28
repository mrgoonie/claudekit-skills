# GraphQL Admin API Reference

Comprehensive guide to Shopify's GraphQL Admin API for building apps and integrations.

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Structure](#api-structure)
4. [Common Resources](#common-resources)
5. [Queries](#queries)
6. [Mutations](#mutations)
7. [Bulk Operations](#bulk-operations)
8. [Pagination](#pagination)
9. [Rate Limiting](#rate-limiting)
10. [Error Handling](#error-handling)
11. [Best Practices](#best-practices)

## Overview

The GraphQL Admin API is Shopify's recommended API for all new development. It provides efficient, type-safe access to store data with flexible querying capabilities.

**Key Advantages:**
- Request only the data you need (no over-fetching)
- Fetch related resources in a single request (no under-fetching)
- Strong typing with introspection
- Predictable responses
- Future-proof with evolving schema

**Endpoint:**
```
POST https://{shop-name}.myshopify.com/admin/api/2025-01/graphql.json
```

## Authentication

### Access Token Header
```javascript
{
  'X-Shopify-Access-Token': 'your-access-token',
  'Content-Type': 'application/json'
}
```

### Request Format
```javascript
fetch(`https://${shop}.myshopify.com/admin/api/2025-01/graphql.json`, {
  method: 'POST',
  headers: {
    'X-Shopify-Access-Token': accessToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: '...',
    variables: { ... }
  })
})
```

## API Structure

### Schema Exploration
Use GraphiQL in Shopify admin (Settings → Apps and sales channels → Develop apps → API credentials → Admin API → Explore with GraphiQL)

### Query Structure
```graphql
query QueryName($variable: Type!) {
  resource(first: 10, query: $variable) {
    edges {
      node {
        id
        field1
        field2
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Mutation Structure
```graphql
mutation MutationName($input: ResourceInput!) {
  resourceCreate(input: $input) {
    resource {
      id
      field
    }
    userErrors {
      field
      message
    }
  }
}
```

## Common Resources

### Products
Manage product catalog and inventory.

**Fields:**
- `id` - Global ID (gid://shopify/Product/123)
- `title` - Product name
- `handle` - URL-friendly identifier
- `description` - Product description (HTML)
- `productType` - Product category
- `vendor` - Product brand/supplier
- `tags` - Search/filter tags
- `status` - ACTIVE, ARCHIVED, DRAFT
- `variants` - Product variations (size, color, etc.)
- `images` - Product images
- `priceRangeV2` - Min/max pricing
- `totalInventory` - Total stock across locations

### Orders
Access and manage customer orders.

**Fields:**
- `id` - Global ID
- `name` - Order number (#1001)
- `createdAt` - Order timestamp
- `customer` - Customer details
- `lineItems` - Ordered products
- `totalPriceSet` - Order total with currency
- `displayFinancialStatus` - PAID, PENDING, REFUNDED
- `displayFulfillmentStatus` - FULFILLED, UNFULFILLED, PARTIAL
- `shippingAddress` - Delivery address
- `billingAddress` - Billing address

### Customers
Manage customer accounts and data.

**Fields:**
- `id` - Global ID
- `email` - Customer email
- `firstName`, `lastName` - Customer name
- `phone` - Contact number
- `addresses` - Saved addresses
- `orders` - Order history
- `lifetimeDuration` - Account age
- `amountSpent` - Total purchases
- `tags` - Customer segmentation

### Inventory
Track product stock across locations.

**Resources:**
- `InventoryLevel` - Stock at specific location
- `InventoryItem` - Inventory entity for variant
- `Location` - Store/warehouse location

## Queries

### Fetch Products
```graphql
query GetProducts($first: Int!, $query: String) {
  products(first: $first, query: $query) {
    edges {
      node {
        id
        title
        handle
        status
        productType
        vendor
        priceRangeV2 {
          minVariantPrice {
            amount
            currencyCode
          }
        }
        variants(first: 5) {
          edges {
            node {
              id
              title
              price
              sku
              inventoryQuantity
            }
          }
        }
        images(first: 1) {
          edges {
            node {
              url
              altText
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

**Variables:**
```json
{
  "first": 10,
  "query": "status:active product_type:Clothing"
}
```

### Fetch Single Product
```graphql
query GetProduct($id: ID!) {
  product(id: $id) {
    id
    title
    description
    variants(first: 10) {
      edges {
        node {
          id
          title
          price
          compareAtPrice
          sku
          barcode
          inventoryQuantity
          weight
          weightUnit
        }
      }
    }
  }
}
```

### Fetch Orders
```graphql
query GetOrders($first: Int!, $query: String) {
  orders(first: $first, query: $query) {
    edges {
      node {
        id
        name
        createdAt
        displayFinancialStatus
        displayFulfillmentStatus
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        customer {
          id
          email
          firstName
          lastName
        }
        lineItems(first: 10) {
          edges {
            node {
              id
              title
              quantity
              originalUnitPriceSet {
                shopMoney {
                  amount
                  currencyCode
                }
              }
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Fetch Customers
```graphql
query GetCustomers($first: Int!, $query: String) {
  customers(first: $first, query: $query) {
    edges {
      node {
        id
        email
        firstName
        lastName
        phone
        ordersCount
        amountSpent {
          amount
          currencyCode
        }
        tags
        addresses {
          address1
          city
          province
          country
          zip
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Fetch Inventory Levels
```graphql
query GetInventoryLevels($first: Int!, $inventoryItemId: ID!) {
  inventoryItem(id: $inventoryItemId) {
    id
    sku
    inventoryLevels(first: $first) {
      edges {
        node {
          id
          available
          location {
            id
            name
          }
        }
      }
    }
  }
}
```

## Mutations

### Create Product
```graphql
mutation CreateProduct($input: ProductInput!) {
  productCreate(input: $input) {
    product {
      id
      title
      handle
      status
    }
    userErrors {
      field
      message
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "title": "New Product",
    "productType": "Clothing",
    "vendor": "Brand Name",
    "status": "ACTIVE",
    "variants": [
      {
        "price": "29.99",
        "sku": "SKU-001",
        "inventoryPolicy": "DENY",
        "inventoryQuantity": 100
      }
    ]
  }
}
```

### Update Product
```graphql
mutation UpdateProduct($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      title
      status
    }
    userErrors {
      field
      message
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "id": "gid://shopify/Product/123",
    "title": "Updated Product Title",
    "status": "ACTIVE"
  }
}
```

### Delete Product
```graphql
mutation DeleteProduct($input: ProductDeleteInput!) {
  productDelete(input: $input) {
    deletedProductId
    userErrors {
      field
      message
    }
  }
}
```

### Create Order
```graphql
mutation CreateOrder($input: DraftOrderInput!) {
  draftOrderCreate(input: $input) {
    draftOrder {
      id
      name
      totalPrice
    }
    userErrors {
      field
      message
    }
  }
}
```

### Update Inventory
```graphql
mutation UpdateInventory($input: InventoryAdjustQuantitiesInput!) {
  inventoryAdjustQuantities(input: $input) {
    inventoryAdjustmentGroup {
      id
      reason
    }
    userErrors {
      field
      message
    }
  }
}
```

### Create Customer
```graphql
mutation CreateCustomer($input: CustomerInput!) {
  customerCreate(input: $input) {
    customer {
      id
      email
      firstName
      lastName
    }
    userErrors {
      field
      message
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "email": "customer@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "phone": "+1234567890",
    "acceptsMarketing": true
  }
}
```

## Bulk Operations

For processing large datasets efficiently.

### Start Bulk Query
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
            variants {
              edges {
                node {
                  id
                  price
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
    userErrors {
      field
      message
    }
  }
}
```

### Check Bulk Operation Status
```graphql
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
  }
}
```

**Status Values:**
- `CREATED` - Operation created
- `RUNNING` - Processing
- `COMPLETED` - Finished successfully
- `FAILED` - Error occurred

## Pagination

GraphQL uses cursor-based pagination.

### Forward Pagination
```graphql
query {
  products(first: 10, after: "cursor_value") {
    edges {
      cursor
      node {
        id
        title
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Backward Pagination
```graphql
query {
  products(last: 10, before: "cursor_value") {
    edges {
      cursor
      node {
        id
        title
      }
    }
    pageInfo {
      hasPreviousPage
      startCursor
    }
  }
}
```

### Pagination Pattern
```javascript
let hasNextPage = true;
let cursor = null;
const allProducts = [];

while (hasNextPage) {
  const response = await fetchProducts(cursor);
  allProducts.push(...response.data.products.edges);

  hasNextPage = response.data.products.pageInfo.hasNextPage;
  cursor = response.data.products.pageInfo.endCursor;
}
```

## Rate Limiting

GraphQL uses cost-based rate limiting.

### Query Cost
Each query has a calculated cost based on:
- Number of fields requested
- Number of connections traversed
- Depth of nested queries

**Cost Limits:**
- Available points: 2000
- Restore rate: 100 points/second
- Maximum query cost: 2000 points

### Check Query Cost
```graphql
query {
  products(first: 10) {
    edges {
      node {
        id
        title
      }
    }
  }
}

# Response includes:
{
  "extensions": {
    "cost": {
      "requestedQueryCost": 12,
      "actualQueryCost": 12,
      "throttleStatus": {
        "maximumAvailable": 2000,
        "currentlyAvailable": 1988,
        "restoreRate": 100
      }
    }
  }
}
```

### Handle Rate Limits
```javascript
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function makeRequest(query) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({ query })
  });

  const data = await response.json();

  if (data.errors?.some(e => e.message.includes('Throttled'))) {
    await delay(1000); // Wait 1 second
    return makeRequest(query); // Retry
  }

  return data;
}
```

## Error Handling

### UserErrors vs System Errors

**UserErrors:** Business logic validation failures (returned in response data)
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

**System Errors:** Technical failures (returned in errors array)
```json
{
  "errors": [
    {
      "message": "Field 'invalid' doesn't exist on type 'Product'",
      "locations": [{"line": 3, "column": 5}]
    }
  ]
}
```

### Error Handling Pattern
```javascript
async function createProduct(input) {
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        query: CREATE_PRODUCT_MUTATION,
        variables: { input }
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    // Check for GraphQL errors
    if (data.errors) {
      console.error('GraphQL errors:', data.errors);
      throw new Error('GraphQL query failed');
    }

    // Check for user errors
    if (data.data.productCreate.userErrors.length > 0) {
      console.error('Validation errors:', data.data.productCreate.userErrors);
      return { success: false, errors: data.data.productCreate.userErrors };
    }

    return { success: true, product: data.data.productCreate.product };

  } catch (error) {
    console.error('Request failed:', error);
    throw error;
  }
}
```

## Best Practices

### 1. Request Only What You Need
```graphql
# ❌ Bad: Requesting unnecessary fields
query {
  products(first: 10) {
    edges {
      node {
        id
        title
        description
        descriptionHtml
        productType
        vendor
        tags
        # ... many more fields
      }
    }
  }
}

# ✅ Good: Request only required fields
query {
  products(first: 10) {
    edges {
      node {
        id
        title
        priceRangeV2 {
          minVariantPrice {
            amount
          }
        }
      }
    }
  }
}
```

### 2. Use Fragments for Reusable Fields
```graphql
fragment ProductFields on Product {
  id
  title
  handle
  priceRangeV2 {
    minVariantPrice {
      amount
      currencyCode
    }
  }
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

### 3. Use Variables for Dynamic Queries
```graphql
# ✅ Good: Using variables
query GetProduct($id: ID!) {
  product(id: $id) {
    title
  }
}

# ❌ Bad: Hardcoded values
query {
  product(id: "gid://shopify/Product/123") {
    title
  }
}
```

### 4. Implement Exponential Backoff
```javascript
async function fetchWithBackoff(query, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ query })
      });

      if (response.status === 429) {
        const waitTime = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s
        await delay(waitTime);
        continue;
      }

      return await response.json();

    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
    }
  }
}
```

### 5. Use Bulk Operations for Large Datasets
For datasets > 1000 records, use bulk operations instead of pagination.

### 6. Cache Responses
Cache API responses when appropriate to reduce API calls:
```javascript
const cache = new Map();

async function fetchProductWithCache(id) {
  if (cache.has(id)) {
    return cache.get(id);
  }

  const product = await fetchProduct(id);
  cache.set(id, product);

  // Expire after 5 minutes
  setTimeout(() => cache.delete(id), 5 * 60 * 1000);

  return product;
}
```

### 7. Monitor API Usage
Track query costs and adjust as needed:
```javascript
function logQueryCost(response) {
  const cost = response.extensions?.cost;
  if (cost) {
    console.log(`Query cost: ${cost.actualQueryCost}/${cost.throttleStatus.maximumAvailable}`);
  }
}
```

## API Versioning

Shopify uses quarterly versioning (YYYY-MM):
- Current stable: 2025-01
- Each version supported for 12 months
- Test breaking changes before version updates
- Use specific version in endpoint URL

## Official Resources

- **GraphQL API Reference:** https://shopify.dev/docs/api/admin-graphql
- **GraphiQL Explorer:** Admin → Settings → Apps and sales channels → Develop apps
- **API Changelog:** https://shopify.dev/changelog
- **Rate Limiting:** https://shopify.dev/docs/api/usage/rate-limits
