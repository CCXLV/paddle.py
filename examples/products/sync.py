from paddle import Client, Environment

client = Client(
    api_key="API_KEY",
    environment=Environment.SANDBOX,
)

# Create a product
initial_product = client.products.create(
    name="Test Product",
    tax_category="standard",
    description="Test Description",
    image_url="https://example.com/image.png",
    custom_data={"key": "value"},
)
print(initial_product)

# List products
all_products = client.products.list()
print(all_products)

# Get a product
product = client.products.get(initial_product.data.id)
print(product)

# Update a product
updated_product = client.products.update(
    initial_product.data.id,
    name="Updated Product",
    description="Updated Description",
    image_url="https://example.com/updated-image.png",
    custom_data={"key": "updated-value"},
)
print(updated_product)
