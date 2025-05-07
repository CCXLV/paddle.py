from paddle import Client, Environment

client = Client(
    api_key="API_KEY",
    environment=Environment.SANDBOX,
)

# Get all customers
customers = client.customers.list()
print(customers)

# Create a customer
customer = client.customers.create(
    email="test@example.com",
    name="Test Customer",
)
print(customer)

# Get a customer
customer = client.customers.get("ctm_0123456789")
print(customer)

# Update a customer
updated_customer = client.customers.update(
    "ctm_0123456789",
    email="updated@example.com",
    name="Updated Customer",
)
print(updated_customer)

# List credit balances
credit_balances = client.customers.list_credit_balances("ctm_0123456789")
print(credit_balances)

# Generate auth token
auth_token = client.customers.generate_auth_token("ctm_0123456789")
print(auth_token)

# Create portal session
portal_session = client.customers.create_portal_session(
    "ctm_0123456789", subscription_ids=["sub_0123456789"]
)
print(portal_session)
