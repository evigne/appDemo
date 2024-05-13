import click

def edit_env_file():
    # Specify the path to the file
    file_path = 'myfiles/.env'
    
    # Read the initial content of the file
    try:
        with open(file_path, 'r') as file:
            original_content = file.read()
    except FileNotFoundError:
        original_content = ""  # If the file does not exist, start with empty content

    # Open the default system editor to edit the content
    edited_content = click.edit(original_content)

    # Check if the content was changed
    if edited_content is not None and edited_content != original_content:
        # Write the edited content back to the file
        with open(file_path, 'w') as file:
            file.write(edited_content)
        print("File updated.")
    else:
        print("No changes made.")

if __name__ == "__main__":
    edit_env_file()