import re
import os

# --- Configuration ---
TABLE_FILE = 'releases_content.md'
README_FILE = 'README.md'
START_MARKER = '' # نشانگر شروع بخش جدول
END_MARKER = ''   # نشانگر پایان بخش جدول
# -------------------

def update_readme_with_regex():
    """Reads the generated table and updates the README.md file using regex
    to replace content between markers, preventing repetition."""
    print(f"Starting README update using regex...")
    try:
        # Read the generated table content
        print(f"Reading table from {TABLE_FILE}...")
        if not os.path.exists(TABLE_FILE):
            print(f"Error: Table file {TABLE_FILE} not found. Skipping README update.")
            # exit(1) # یا تصمیم بگیرید که آیا خروج از اسکریپت ضروری است یا خیر
            return

        with open(TABLE_FILE, 'r', encoding='utf-8') as f:
            table_content = f.read().strip()

        # Read the current README content
        print(f"Reading {README_FILE}...")
        if not os.path.exists(README_FILE):
            print(f"Error: README file {README_FILE} not found. Cannot update.")
            # اگر README وجود ندارد، شاید بخواهید آن را با محتوای جدول ایجاد کنید
            # یا اینکه خطا داده و خارج شوید. در اینجا فرض می‌کنیم باید وجود داشته باشد.
            # For example, create it:
            # print(f"{README_FILE} not found. Creating it with table content.")
            # with open(README_FILE, 'w', encoding='utf-8') as f:
            #    f.write(f"{START_MARKER}\n{table_content}\n{END_MARKER}\n")
            # return
            exit(1)


        with open(README_FILE, 'r', encoding='utf-8') as f:
            readme_content = f.read()

        # Escape markers for regex (though not strictly necessary for these specific strings)
        start_escaped = re.escape(START_MARKER)
        end_escaped = re.escape(END_MARKER)

        # Build the regex to find content between markers (inclusive of markers)
        # Use re.DOTALL (s) to make '.' match newlines
        pattern = re.compile(f"({start_escaped})(.*?)({end_escaped})", re.DOTALL)

        # Check if the pattern (markers) exists in the README
        if not pattern.search(readme_content):
            print(f"Warning: Markers '{START_MARKER}' and '{END_MARKER}' not found in {README_FILE}.")
            # اگر نشانگرها یافت نشدند، می‌توانید محتوای جدول را به انتهای فایل اضافه کنید
            # یا یک پیام خطا نمایش دهید. در اینجا ما آن را به انتهای فایل اضافه می‌کنیم.
            print(f"Appending table to the end of {README_FILE} as markers were not found.")
            # Ensure there's a newline before appending if the file doesn't end with one
            if readme_content and not readme_content.endswith('\n'):
                readme_content += '\n'
            new_readme_content = f"{readme_content}{START_MARKER}\n{table_content}\n{END_MARKER}\n"
        else:
            # Define the new block content, including markers, to replace the old block
            replacement = f"{START_MARKER}\n{table_content}\n{END_MARKER}"
            # Use re.sub to replace the first occurrence of the block.
            new_readme_content, num_replacements = pattern.subn(replacement, readme_content, count=1)

            if num_replacements == 0:
                # این حالت نباید اتفاق بیفتد اگر pattern.search() موفق بوده باشد
                print(f"Error: Could not perform replacement even though markers were found. This is unexpected.")
                exit(1)
            elif num_replacements > 1:
                 # این هم نباید با count=1 اتفاق بیفتد
                print(f"Warning: Replaced more than one block. Check your README for duplicate marker sets.")

        # Write the updated content back to README
        print(f"Writing updated content to {README_FILE}...")
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(new_readme_content)

        print(f"✅ {README_FILE} updated successfully.")

    except FileNotFoundError:
        # این مورد باید توسط بررسی‌های os.path.exists در بالا گرفته شود
        print(f"Error: A file was not found during the process.")
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
