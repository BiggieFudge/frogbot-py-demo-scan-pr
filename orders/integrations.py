"""Downstream integration settings for the orders service.

NOTE: demo fixture for Frogbot secrets detection. All values below are randomly
generated and were never valid credentials anywhere.
"""

# Generic hardcoded credentials -> REQ.SECRET.GENERIC.CODE
password = "gaWWv7Z6nrpi9HN7XDzsRXlzgi2eQV8zxyuu"
api_key = "s0OWWZPMQXvWlNzaktjFIS3C3ZkpxLYakr9X"
client_secret = "SzQERRnoHSD22ARVWS1O6LiyGBcR4zzEcQg6"

# Credentials embedded in a connection URL -> REQ.SECRET.GENERIC.URL-TEXT
DATABASE_URL = "postgres://orders_admin:q6BxlxdUZukLepV7H4dCKi21JmHWDoU64Q8e@db.orders-internal:5432/orders"

# Bearer token -> REQ.SECRET.KEYS
CATALOG_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
