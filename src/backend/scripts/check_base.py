import sys
import os

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Now perform the import as absolute imports
from app.db.database import Base  # Import the Base object from your app
from app.models.user_models import User  # Import the User model

# Print the tables registered with Base
print("Tables registered with Base:")
print(Base.metadata.tables)
