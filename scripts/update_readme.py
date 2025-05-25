import re
import os

# --- Configuration ---
TABLE_FILE = 'releases_content.md'
README_FILE = 'README.md'
START_MARKER = ''
END_MARKER = ''
# -------------------

def update_readme_with_regex():
    """Reads the generated table and updates the README.md file using regex
       to replace content between markers, preventing repetition."""
    print(f"Starting README update using regex...")
    try:
        # Read the generated table content
        print(f"Reading table from {TABLE_FILE}...")
        with open(TABLE_FILE, 'r', encoding='utf-8') as f:
            table_content = f.read().strip()

        # Read the current README content
        print(f"Reading {README_FILE}...")
        with open(README_FILE, 'r', encoding='utf-8') as f:
            readme_content = f.read()

        # Escape markers for regex, just in case (though unlikely needed for comments)
        start = re.escape(START_MARKER)
        end = re.escape(END_MARKER)

        # Build the regex to find content between markers (inclusive)
        # Use re.DOTALL (s) to make '.' match newlines
        pattern = re.compile(f"({start})(.*?)({end})", re.DOTALL)

        # Check if the pattern exists at least once
        if not pattern.search(readme_content):
            print(f"Error: Markers '{START_MARKER}' and '{END_MARKER}' not found or not in correct order in {README_FILE}.")
            print("Cannot update README. Please ensure the markers exist and are correctly placed.")
            exit(1)

        # Define the new block content, including markers
        replacement = f"{START_MARKER}\n{table_content}\n{END_MARKER}"

        # Use re.sub to replace the *first occurrence* of the block.
        # This prevents issues if multiple blocks accidentally exist.
        new_readme_content, num_replacements = pattern.subn(replacement, readme_content, count=1)

        if num_replacements == 0:
            print(f"Error: Could not perform replacement. Markers might be present but pattern failed.")
            exit(1)
        elif num_replacements > 1:
            # This shouldn't happen with count=1, but as a safeguard.
            print(f"Warning: Replaced more than one block. Check your README for duplicate markers.")


        # Write the updated content back to README
        print(f"Writing updated content to {README_FILE}...")
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(new_readme_content)

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

# Ensure the main function is called
if __name__ == "__main__":
    update_readme_with_regex()