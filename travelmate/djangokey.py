# generate_secret_key.py
from django.core.management.utils import get_random_secret_key

# Generate a secure random key
secret_key = get_random_secret_key()

# Print it so you can see it
print("Generated SECRET_KEY:", secret_key)

# Optionally, write/update it in your .env file
with open(".env", "a") as f:  # "a" appends, use "w" to overwrite
    f.write(f"\nDJANGO_SECRET_KEY={secret_key}\n")

print("✅ Secret key has been written to .env")
