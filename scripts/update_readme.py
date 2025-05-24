import re
import os

# --- Configuration ---
TABLE_FILE = 'releases_content.md'
README_FILE = 'README.md'
START_MARKER = ''
END_MARKER = ''
# -------------------

def update_readme_line_by_line():
    """Reads the generated table and updates the README.md file line by line."""
    print(f"Starting README update (line-by-line method)...")
    try:
        # Read the generated table content
        print(f"Reading table from {TABLE_FILE}...")
        with open(TABLE_FILE, 'r', encoding='utf-8') as f:
            table_content = f.read().strip()

        # Read the current README lines
        print(f"Reading {README_FILE}...")
        with open(README_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        in_block = False
        block_written = False

        for line in lines:
            # Strip leading/trailing whitespace to handle potential variations
            stripped_line = line.strip()

            if stripped_line == START_MARKER:
                if not block_written:
                    # Found the start, write the new block
                    new_lines.append(START_MARKER + '\n')
                    new_lines.append(table_content + '\n')
                    new_lines.append(END_MARKER + '\n')
                    block_written = True
                in_block = True
            elif stripped_line == END_MARKER:
                # Found the end, stop ignoring lines
                in_block = False
            elif not in_block:
                # If not inside the block, keep the line
                new_lines.append(line)

        # Check if we actually found the block and wrote it
        if not block_written:
            print(f"Error: {START_MARKER} not found. Could not insert table.")
            exit(1)

        # Write the updated content back to README
        print(f"Writing updated content to {README_FILE}...")
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

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
    update_readme_line_by_line()
