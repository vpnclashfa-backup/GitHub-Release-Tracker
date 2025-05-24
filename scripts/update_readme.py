import re
import os

# --- Configuration ---
TABLE_FILE = 'releases_content.md'
README_FILE = 'README.md'
START_MARKER = ''
END_MARKER = ''
# -------------------

def update_readme():
    """Reads the generated table and updates the README.md file."""
    print(f"Starting README update...")
    try:
        # Read the generated table content
        print(f"Reading table from {TABLE_FILE}...")
        with open(TABLE_FILE, 'r', encoding='utf-8') as f:
            table_content = f.read()

        # Read the current README content
        print(f"Reading {README_FILE}...")
        with open(README_FILE, 'r', encoding='utf-8') as f:
            readme_content = f.read()

        # Check for markers
        if START_MARKER not in readme_content or END_MARKER not in readme_content:
            print(f"Error: Markers {START_MARKER} and {END_MARKER} not found in {README_FILE}.")
            exit(1)

        # Replace content between markers
        print("Replacing content between markers...")
        new_readme = re.sub(
            rf'{START_MARKER}(.*?){END_MARKER}',
            f'{START_MARKER}\n{table_content}\n{END_MARKER}',
            readme_content,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Write the updated content back to README
        print(f"Writing updated content to {README_FILE}...")
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(new_readme)

        print(f"✅ {README_FILE} updated successfully.")

    except FileNotFoundError:
        print(f"Error: {README_FILE} or {TABLE_FILE} not found.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
    finally:
        # Clean up the temporary table file
        if os.path.exists(TABLE_FILE):
            print(f"Cleaning up {TABLE_FILE}...")
            os.remove(TABLE_FILE)

if __name__ == "__main__":
    update_readme()
