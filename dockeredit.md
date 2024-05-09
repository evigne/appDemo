To insert values into a Dockerfile via Python, you can read the Dockerfile as a template, substitute placeholders with actual values, and then write the modified content back. Here’s an example approach using Python string formatting:

1. Create a Dockerfile template containing placeholders.
2. Use Python to replace the placeholders with the values you want.
3. Save the modified Dockerfile.

**Dockerfile Template Example (`Dockerfile.template`):**

```Dockerfile
FROM {base_image}
WORKDIR /app
COPY {source_dir} .
RUN pip install -r requirements.txt
CMD ["{entrypoint}"]
```

**Python Script to Modify the Dockerfile Template:**

```python
# Example data to insert into the Dockerfile
base_image = "python:3.10-slim"
source_dir = "./src"
entrypoint = "python app.py"

# Read the Dockerfile template
with open("Dockerfile.template", "r") as template_file:
    dockerfile_template = template_file.read()

# Replace placeholders with actual values
dockerfile_content = dockerfile_template.format(
    base_image=base_image,
    source_dir=source_dir,
    entrypoint=entrypoint
)

# Write the modified content into a new Dockerfile
with open("Dockerfile", "w") as dockerfile:
    dockerfile.write(dockerfile_content)

print("Dockerfile has been created with the specified values.")
```

### Key Steps in the Code:

1. **Template Creation:** The Dockerfile template (`Dockerfile.template`) uses placeholders in curly braces (e.g., `{base_image}`) for values that will be substituted.
   
2. **Python Formatting:** The `str.format()` method is used to substitute the placeholders with actual values provided as arguments.

3. **Output Generation:** The final Dockerfile is written out with substituted values.

This method ensures your Dockerfile remains consistent and readable while being dynamically configurable.