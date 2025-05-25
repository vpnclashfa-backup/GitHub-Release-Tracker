import re
import os

# --- Configuration ---
TABLE_FILE = 'releases_content.md'
README_FILE = 'README.md'
# --- *** این خطوط تغییر کرده اند *** ---
START_MARKER = ''
END_MARKER = ''
# -------------------

def update_readme_line_by_line():
    """Reads the generated table and updates the README.md file line by line,
       replacing content between (and including) specified markers."""
    print(f"Starting README update (line-by-line method)...")
    print(f"Using START_MARKER: '{START_MARKER}'")
    print(f"Using END_MARKER: '{END_MARKER}'")

    try:
        # Read the generated table content
        print(f"Reading table from {TABLE_FILE}...")
        with open(TABLE_FILE, 'r', encoding='utf-8') as f:
            table_content = f.read().strip() # The content to insert

        # Read the current README lines
        print(f"Reading {README_FILE}...")
        with open(README_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        in_block_to_replace = False
        block_written = False
        start_marker_found = False

        for line in lines:
            stripped_line = line.strip()

            if stripped_line == START_MARKER:
                print(f"Found START_MARKER: '{START_MARKER}'")
                new_lines.append(START_MARKER + '\n') # Keep the start marker
                new_lines.append(table_content + '\n') # Add the new table content
                block_written = True
                in_block_to_replace = True
                start_marker_found = True
            elif stripped_line == END_MARKER:
                print(f"Found END_MARKER: '{END_MARKER}'")
                if not start_marker_found:
                    print(f"Warning: END_MARKER found before START_MARKER. Keeping original END_MARKER.")
                    new_lines.append(line)
                else:
                    new_lines.append(END_MARKER + '\n') # Keep/Add the end marker
                    in_block_to_replace = False
            elif not in_block_to_replace:
                new_lines.append(line) # Keep lines outside the block
            else:
                # Inside the block to replace, so skip this original line
                print(f"Skipping line inside old block: {line.strip()}")


        if not block_written:
            print(f"Error: START_MARKER ('{START_MARKER}') not found in {README_FILE}.")
            print(f"Table content could not be inserted. Please ensure markers exist in {README_FILE}.")
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