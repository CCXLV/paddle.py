from paddle import Client, Environment

client = Client(
    api_key="API_KEY",
    environment=Environment.SANDBOX,
)

# Get all customers
customers = client.customer.list()
print(customers)

# Create a customer
customer = client.customer.create(
    email="test@example.com",
    name="Test Customer",
)
print(customer)

# Get a customer
customer = client.customer.get("ctm_0123456789")
print(customer)

# Update a customer
updated_customer = client.customer.update(
    "ctm_0123456789",
    email="updated@example.com",
    name="Updated Customer",
)
print(updated_customer)

# List credit balances
credit_balances = client.customer.list_credit_balances("ctm_0123456789")
print(credit_balances)

# Generate auth token
auth_token = client.customer.generate_auth_token("ctm_0123456789")
print(auth_token)
