To add new key-value pairs to a `.env` file and update existing ones using Python, you can use the `python-dotenv` library, which makes it easy to load, edit, and save `.env` files. If you don't have the `python-dotenv` library installed, you can install it using pip:

```bash
pip install python-dotenv
```

Here’s how you can add new keys and update existing ones in your `.env` file:

1. **Load the `.env` file**: Read the existing key-value pairs.
2. **Update/Add the key-value pairs**: Modify the existing entries and add new ones as needed.
3. **Save the changes back to the `.env` file**: Write the updated key-value pairs back.

Here's a Python script that demonstrates this process:

```python
from dotenv import dotenv_values, set_key
import os

# Path to your .env file
env_path = 'path1/.env'

# Load existing .env file into a dictionary
config = dotenv_values(env_path)

# Define new or updated key-value pairs
updates = {
    'NEW_KEY1': 'NewValue1',
    'NEW_KEY2': 'NewValue2',
    'EXISTING_KEY1': 'UpdatedValue1',
    'EXISTING_KEY2': 'UpdatedValue2'
}

# Update the .env file with new and updated values
for key, value in updates.items():
    set_key(env_path, key, value)

print("Updated .env file:")
# Print the updated .env file contents
with open(env_path, 'r') as file:
    print(file.read())
```

This script will:
- Load the current contents of `path1/.env`.
- Update the values of `EXISTING_KEY1` and `EXISTING_KEY2` and add `NEW_KEY1` and `NEW_KEY2`.
- Save the changes back to the `.env` file.

Make sure to adjust the `env_path` and `updates` dictionary to match your specific needs.


###### >

To modify and update `.env` files using Python, you can use the `python-dotenv` library, which simplifies the handling of environment files. If you don't have this library installed yet, you can install it via pip:

```bash
pip install python-dotenv
```

Below is a Python script that demonstrates how to add new key-value pairs and update existing ones in `.env` files located at `path1/.env` and `mypath/.env`:

```python
from dotenv import load_dotenv, dotenv_values, set_key
import os

# Function to update or add key-value pairs to a .env file
def update_env_file(path, updates):
    # Load current environment variables from file
    env_values = dotenv_values(path)
    
    # Update with new values or add if key does not exist
    for key, value in updates.items():
        env_values[key] = value
        set_key(path, key, value)
        
    print(f"Updated {path}:")
    print(env_values)

# Load existing values to be updated from mypath/.env
source_path = 'mypath/.env'
load_dotenv(source_path)
value_to_update1 = os.getenv('KEY_TO_UPDATE1')
value_to_update2 = os.getenv('KEY_TO_UPDATE2')

# Values to update in path1/.env
updates_path1 = {
    'NEW_KEY1': 'NewValue1',
    'NEW_KEY2': 'NewValue2',
    'EXISTING_KEY1': value_to_update1,
    'EXISTING_KEY2': value_to_update2
}

# Path to the target .env file
target_path = 'path1/.env'

# Update the target .env file
update_env_file(target_path, updates_path1)
```

This script does the following:
1. Loads the existing `.env` values from `mypath/.env`.
2. Retrieves the values that need to be updated.
3. Defines new key-value pairs and the values that need updating in `path1/.env`.
4. Calls a function to update these values in `path1/.env`.

Make sure you replace `'KEY_TO_UPDATE1'` and `'KEY_TO_UPDATE2'` with the actual keys you intend to update, and adjust the file paths to match your project structure.
