# UI Extensions Reference

Comprehensive guide to building UI extensions for Shopify.

## Table of Contents
1. [Overview](#overview)
2. [Checkout UI Extensions](#checkout-ui-extensions)
3. [Admin UI Extensions](#admin-ui-extensions)
4. [POS UI Extensions](#pos-ui-extensions)
5. [Customer Account UI Extensions](#customer-account-ui-extensions)
6. [Post-Purchase Extensions](#post-purchase-extensions)
7. [Common Components](#common-components)
8. [Extension APIs](#extension-apis)
9. [Best Practices](#best-practices)

## Overview

UI Extensions allow you to customize and extend Shopify surfaces without modifying core code. Extensions render natively for optimal performance and use declarative component APIs.

**Key Benefits:**
- Native rendering (fast performance)
- Consistent UX across Shopify
- Automatic updates and maintenance
- Secure and sandboxed execution
- Mobile and desktop support

## Checkout UI Extensions

Customize the checkout and thank-you pages.

### Extension Points

**Static Targets (Fixed Placement):**
- `purchase.checkout.header.render-after` - Below header
- `purchase.checkout.contact.render-before` - Above contact info
- `purchase.checkout.shipping-option-list.render-after` - Below shipping methods
- `purchase.checkout.payment-method-list.render-after` - Below payment methods
- `purchase.checkout.footer.render-before` - Above footer
- `purchase.thank-you.header.render-after` - Thank you page header
- `purchase.thank-you.footer.render-before` - Thank you page footer

**Block Targets (Flexible Placement):**
- `purchase.checkout.block.render` - Merchant-controlled placement
- `purchase.thank-you.block.render` - Thank you page blocks

### Setup

**1. Generate Extension:**
```bash
shopify app generate extension --type checkout_ui_extension
```

**2. Configuration (`shopify.extension.toml`):**
```toml
api_version = "2025-01"

[[extensions]]
type = "ui_extension"
name = "gift-message"
handle = "gift-message"

[[extensions.targeting]]
target = "purchase.checkout.block.render"

[capabilities]
network_access = true
api_access = true
```

**3. Entry Point (`src/Checkout.jsx`):**
```javascript
import React, { useState } from 'react';
import {
  reactExtension,
  BlockStack,
  TextField,
  Checkbox,
  Banner,
  useApi
} from '@shopify/ui-extensions-react/checkout';

export default reactExtension(
  'purchase.checkout.block.render',
  () => <Extension />
);

function Extension() {
  const { extensionPoint } = useApi();
  const [message, setMessage] = useState('');
  const [isGift, setIsGift] = useState(false);

  return (
    <BlockStack spacing="loose">
      <Banner title="Gift Options" />
      <Checkbox
        checked={isGift}
        onChange={setIsGift}
      >
        This is a gift
      </Checkbox>
      {isGift && (
        <TextField
          label="Gift Message"
          value={message}
          onChange={setMessage}
          multiline={3}
        />
      )}
    </BlockStack>
  );
}
```

### Checkout Components

#### Layout
- `View` - Container component
- `BlockStack` - Vertical stacking
- `InlineStack` - Horizontal stacking
- `InlineLayout` - Responsive inline layout
- `BlockLayout` - Responsive block layout
- `Grid` - Grid layout
- `GridItem` - Grid cell
- `Divider` - Visual separator
- `ScrollView` - Scrollable container

#### Input
- `TextField` - Text input
- `Checkbox` - Boolean selection
- `Select` - Dropdown selection
- `DatePicker` - Date input
- `Form` - Form container

#### Display
- `Text` - Typography
- `Heading` - Section headers
- `Banner` - Important messages
- `Badge` - Status indicators
- `Image` - Images
- `Icon` - Icons
- `Link` - Hyperlinks
- `List` - Ordered/unordered lists
- `ListItem` - List items

#### Interactive
- `Button` - Primary actions
- `Pressable` - Custom clickable areas
- `Modal` - Overlay dialogs
- `Popover` - Contextual overlays

#### Loading
- `Spinner` - Loading indicator
- `SkeletonText` - Text placeholder
- `SkeletonImage` - Image placeholder

### Checkout APIs

#### useApi Hook
```javascript
import { useApi } from '@shopify/ui-extensions-react/checkout';

function Extension() {
  const {
    extensionPoint,    // Current extension point
    shop,             // Shop details
    storefront,       // Storefront API client
    i18n,             // Internationalization
    sessionToken      // Session token for auth
  } = useApi();
}
```

#### Cart Data
```javascript
import {
  useCartLines,
  useApplyCartLinesChange
} from '@shopify/ui-extensions-react/checkout';

function Extension() {
  const lines = useCartLines();
  const applyChange = useApplyCartLinesChange();

  async function updateQuantity(lineId, quantity) {
    await applyChange({
      type: 'updateCartLine',
      id: lineId,
      quantity: quantity
    });
  }

  return lines.map(line => (
    <Text key={line.id}>
      {line.merchandise.product.title} - Qty: {line.quantity}
    </Text>
  ));
}
```

#### Shipping Address
```javascript
import {
  useShippingAddress
} from '@shopify/ui-extensions-react/checkout';

function Extension() {
  const address = useShippingAddress();

  return (
    <Text>
      Shipping to: {address.city}, {address.countryCode}
    </Text>
  );
}
```

#### Metafields
```javascript
import { useMetafields } from '@shopify/ui-extensions-react/checkout';

function Extension() {
  const metafields = useMetafields();

  const customData = metafields.find(
    m => m.namespace === 'custom' && m.key === 'data'
  );

  return <Text>{customData?.value}</Text>;
}
```

#### Attributes
```javascript
import {
  useAttributes,
  useApplyAttributeChange
} from '@shopify/ui-extensions-react/checkout';

function Extension() {
  const attributes = useAttributes();
  const applyChange = useApplyAttributeChange();

  async function saveGiftMessage(message) {
    await applyChange({
      type: 'updateAttribute',
      key: 'gift_message',
      value: message
    });
  }
}
```

## Admin UI Extensions

Extend Shopify admin interface.

### Extension Types

#### 1. Admin Action
Custom actions on resource pages (products, orders, customers).

**Generate:**
```bash
shopify app generate extension --type admin_action
```

**Config:**
```toml
[[extensions.targeting]]
module = "Admin::Product::SubscriptionExtension"
target = "admin.product-details.action.render"
```

**Example:**
```javascript
import {
  reactExtension,
  AdminAction,
  Button
} from '@shopify/ui-extensions-react/admin';

export default reactExtension(
  'admin.product-details.action.render',
  () => <Extension />
);

function Extension() {
  async function handleExport() {
    // Custom export logic
    console.log('Exporting product...');
  }

  return (
    <AdminAction
      title="Export Product"
      primaryAction={
        <Button onPress={handleExport}>Export</Button>
      }
    />
  );
}
```

#### 2. Admin Block
Embedded content in admin pages.

**Targets:**
- `admin.product-details.block.render`
- `admin.order-details.block.render`
- `admin.customer-details.block.render`

**Example:**
```javascript
import {
  reactExtension,
  BlockStack,
  Text,
  Badge,
  useData
} from '@shopify/ui-extensions-react/admin';

export default reactExtension(
  'admin.product-details.block.render',
  () => <Extension />
);

function Extension() {
  const { data } = useData();
  const product = data.product;

  return (
    <BlockStack>
      <Text variant="headingMd">Custom Analytics</Text>
      <Text>Views: {product.viewCount || 0}</Text>
      <Badge tone="success">Popular</Badge>
    </BlockStack>
  );
}
```

### Admin Components

- `AdminAction` - Action container
- `AdminBlock` - Block container
- `BlockStack` - Vertical layout
- `InlineStack` - Horizontal layout
- `Button` - Actions
- `Text` - Typography
- `Badge` - Status
- `Banner` - Alerts
- `TextField` - Input
- `Select` - Dropdown
- `Checkbox` - Boolean input

## POS UI Extensions

Customize Point of Sale experience.

### Extension Types

#### 1. Smart Grid Tile
Quick access action tile.

**Generate:**
```bash
shopify app generate extension --type pos_ui_extension
```

**Example:**
```javascript
import {
  reactExtension,
  SmartGridTile,
  Text
} from '@shopify/ui-extensions-react/pos';

export default reactExtension(
  'pos.home.tile.render',
  () => <Extension />
);

function Extension() {
  function handlePress() {
    // Open custom workflow
  }

  return (
    <SmartGridTile
      title="Gift Cards"
      subtitle="Manage gift cards"
      onPress={handlePress}
    />
  );
}
```

#### 2. Modal Action
Full-screen modal for complex workflows.

**Example:**
```javascript
import {
  reactExtension,
  Screen,
  BlockStack,
  Button,
  TextField,
  useApi
} from '@shopify/ui-extensions-react/pos';

export default reactExtension(
  'pos.home.modal.render',
  () => <Extension />
);

function Extension() {
  const { navigation } = useApi();

  function handleSave() {
    // Save logic
    navigation.pop();
  }

  return (
    <Screen name="Gift Card" title="Gift Card Management">
      <BlockStack>
        <TextField label="Amount" />
        <TextField label="Recipient Email" />
        <Button onPress={handleSave}>Issue Gift Card</Button>
      </BlockStack>
    </Screen>
  );
}
```

### POS Components

- `Screen` - Full-screen container
- `SmartGridTile` - Grid tile
- `BlockStack` - Vertical layout
- `InlineStack` - Horizontal layout
- `Button` - Actions
- `TextField` - Input
- `List` - Lists
- `Text` - Typography

## Customer Account UI Extensions

Customize customer account pages.

### Targets

- `customer-account.order-status.block.render` - Order status page
- `customer-account.order-index.block.render` - Order list page
- `customer-account.profile.block.render` - Profile page

### Example

```javascript
import {
  reactExtension,
  BlockStack,
  Text,
  Button,
  useApi
} from '@shopify/ui-extensions-react/customer-account';

export default reactExtension(
  'customer-account.order-status.block.render',
  () => <Extension />
);

function Extension() {
  const { order } = useApi();

  function handleReturn() {
    // Initiate return process
  }

  return (
    <BlockStack>
      <Text variant="headingMd">Need to return?</Text>
      <Text>Start a return for order {order.name}</Text>
      <Button onPress={handleReturn}>Start Return</Button>
    </BlockStack>
  );
}
```

## Post-Purchase Extensions

Upsell offers on thank-you page.

### Target

`purchase.thank-you.block.render`

### Example

```javascript
import {
  reactExtension,
  BlockStack,
  Text,
  Button,
  Image,
  useApi,
  useCartLines
} from '@shopify/ui-extensions-react/checkout';

export default reactExtension(
  'purchase.thank-you.block.render',
  () => <Extension />
);

function Extension() {
  const { applyCartLinesChange } = useApi();
  const lines = useCartLines();

  async function addUpsellProduct() {
    await applyCartLinesChange({
      type: 'addCartLine',
      merchandiseId: 'gid://shopify/ProductVariant/123',
      quantity: 1
    });
  }

  return (
    <BlockStack spacing="loose">
      <Text variant="headingMd">Complete Your Order</Text>
      <Image source="https://cdn.shopify.com/..." />
      <Text>Add this matching accessory for 20% off!</Text>
      <Button onPress={addUpsellProduct}>Add to Order</Button>
    </BlockStack>
  );
}
```

## Common Components

### BlockStack

Vertical stacking with spacing control.

```javascript
<BlockStack spacing="loose">
  <Text>Item 1</Text>
  <Text>Item 2</Text>
  <Text>Item 3</Text>
</BlockStack>
```

**Props:**
- `spacing`: `"none"` | `"extraTight"` | `"tight"` | `"base"` | `"loose"` | `"extraLoose"`
- `alignment`: `"leading"` | `"center"` | `"trailing"`

### InlineStack

Horizontal stacking.

```javascript
<InlineStack spacing="base" alignment="center">
  <Button>Cancel</Button>
  <Button kind="primary">Save</Button>
</InlineStack>
```

### TextField

Text input field.

```javascript
<TextField
  label="Email Address"
  value={email}
  onChange={setEmail}
  type="email"
  required
  error={emailError}
/>
```

**Props:**
- `label`: Label text
- `value`: Current value
- `onChange`: Change handler
- `type`: `"text"` | `"email"` | `"number"` | `"tel"` | `"url"`
- `multiline`: Number of rows
- `required`: Required field
- `disabled`: Disabled state
- `error`: Error message

### Button

Action button.

```javascript
<Button
  kind="primary"
  onPress={handleSubmit}
  disabled={!isValid}
  loading={isSubmitting}
>
  Submit Order
</Button>
```

**Props:**
- `kind`: `"primary"` | `"secondary"` | `"plain"`
- `onPress`: Click handler
- `disabled`: Disabled state
- `loading`: Loading state

### Banner

Message banner.

```javascript
<Banner status="warning" title="Important">
  Your order will be delayed due to weather conditions.
</Banner>
```

**Props:**
- `status`: `"info"` | `"success"` | `"warning"` | `"critical"`
- `title`: Banner title

### Checkbox

Boolean input.

```javascript
<Checkbox
  checked={agreedToTerms}
  onChange={setAgreedToTerms}
>
  I agree to the terms and conditions
</Checkbox>
```

### Modal

Overlay dialog.

```javascript
<Modal
  open={isOpen}
  onClose={handleClose}
  title="Confirmation"
>
  <BlockStack>
    <Text>Are you sure?</Text>
    <InlineStack>
      <Button onPress={handleClose}>Cancel</Button>
      <Button kind="primary" onPress={handleConfirm}>Confirm</Button>
    </InlineStack>
  </BlockStack>
</Modal>
```

## Extension APIs

### Network Requests

Extensions can make network requests to your app backend.

```javascript
import { useApi } from '@shopify/ui-extensions-react/checkout';

function Extension() {
  const { sessionToken } = useApi();

  async function fetchData() {
    const token = await sessionToken.get();

    const response = await fetch('https://your-app.com/api/data', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    return await response.json();
  }
}
```

### Storefront API

Query storefront data.

```javascript
import { useApi } from '@shopify/ui-extensions-react/checkout';

function Extension() {
  const { storefront } = useApi();

  async function fetchProducts() {
    const { data } = await storefront.query(`
      query {
        products(first: 10) {
          edges {
            node {
              id
              title
              priceRange {
                minVariantPrice {
                  amount
                }
              }
            }
          }
        }
      }
    `);

    return data.products.edges;
  }
}
```

### Analytics

Track custom events.

```javascript
import { useApi } from '@shopify/ui-extensions-react/checkout';

function Extension() {
  const { analytics } = useApi();

  function trackEvent() {
    analytics.publish('custom_event', {
      customProperty: 'value'
    });
  }
}
```

## Best Practices

### Performance

1. **Lazy Load Data:**
```javascript
import { useEffect, useState } from 'react';

function Extension() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData().then(setData);
  }, []);

  if (!data) return <Spinner />;
  return <Display data={data} />;
}
```

2. **Memoize Expensive Computations:**
```javascript
import { useMemo } from 'react';

function Extension() {
  const lines = useCartLines();

  const total = useMemo(() => {
    return lines.reduce((sum, line) => {
      return sum + (parseFloat(line.cost.totalAmount.amount) * line.quantity);
    }, 0);
  }, [lines]);
}
```

### User Experience

1. **Provide Loading States:**
```javascript
{isLoading ? <Spinner /> : <Content />}
```

2. **Show Error Messages:**
```javascript
{error && <Banner status="critical">{error}</Banner>}
```

3. **Validate Input:**
```javascript
<TextField
  label="Email"
  value={email}
  onChange={setEmail}
  error={!isValidEmail(email) ? 'Invalid email' : undefined}
/>
```

### Security

1. **Verify Session Tokens:**
```javascript
const token = await sessionToken.get();
// Always send token to your backend for verification
```

2. **Sanitize User Input:**
```javascript
const sanitized = input.trim().replace(/[<>]/g, '');
```

3. **Use HTTPS:**
All network requests must use HTTPS.

## Testing

### Local Testing

1. **Start dev server:**
```bash
shopify app dev
```

2. **Install on development store**

3. **Navigate to checkout/admin page**

4. **Verify extension appears and functions**

### Manual Testing Checklist

- [ ] Extension loads correctly
- [ ] All components render properly
- [ ] Form validation works
- [ ] Network requests succeed
- [ ] Error states display correctly
- [ ] Loading states show appropriately
- [ ] Mobile responsive
- [ ] Desktop layout correct
- [ ] Accessibility (keyboard navigation, screen readers)

## Deployment

1. **Build extension:**
```bash
shopify extension build
```

2. **Deploy app:**
```bash
shopify app deploy
```

3. **Test in production store**

4. **Monitor for errors**

## Official Resources

- **Checkout Extensions:** https://shopify.dev/docs/api/checkout-extensions
- **Admin Extensions:** https://shopify.dev/docs/apps/admin/extensions
- **POS Extensions:** https://shopify.dev/docs/apps/pos/extensions
- **Component Reference:** https://shopify.dev/docs/api/checkout-ui-extensions/components
- **Best Practices:** https://shopify.dev/docs/apps/best-practices/performance
