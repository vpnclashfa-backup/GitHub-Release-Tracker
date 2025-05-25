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
        # بررسی حیاتی: نشانگرها نباید خالی باشند
        if not START_MARKER or not END_MARKER:
            print(f"CRITICAL Error: START_MARKER or END_MARKER is empty in the Python script. Cannot reliably update README.")
            print(f"Please define them at the top of scripts/update_readme.py as HTML comments.")
            exit(1) # خروج با خطا چون این یک مشکل اساسی در پیکربندی اسکریپت است

        # Read the generated table content
        print(f"Reading table from {TABLE_FILE}...")
        if not os.path.exists(TABLE_FILE):
            print(f"Error: Table file {TABLE_FILE} not found. Skipping README update.")
            # اگر فایل جدول وجود ندارد، شاید بهتر باشد اسکریپت متوقف شود تا از ایجاد README ناقص جلوگیری شود
            exit(1) 

        with open(TABLE_FILE, 'r', encoding='utf-8') as f:
            table_content = f.read().strip()

        # Read the current README content
        print(f"Reading {README_FILE}...")
        if not os.path.exists(README_FILE):
            # این حالت توسط مرحله "Create initial files" در workflow باید پوشش داده شود.
            # اما اگر به هر دلیلی README.md در این مرحله وجود نداشته باشد، اسکریپت آن را ایجاد می‌کند.
            print(f"Info: {README_FILE} not found by Python script. Workflow should have created it.")
            print(f"Attempting to create {README_FILE} from Python script with markers and table...")
            with open(README_FILE, 'w', encoding='utf-8') as f:
                # ایجاد یک README.md پایه با نشانگرها و محتوای جدول
                f.write(f"# رهیاب نسخه‌ها\n\n")
                f.write(f"لیست آخرین نسخه‌های مخازن مورد نظر:\n\n")
                f.write(f"{START_MARKER}\n{table_content}\n{END_MARKER}\n\n")
                f.write(f"این مخزن به صورت خودکار به‌روز می‌شود.\n")
            print(f"✅ {README_FILE} created and populated by Python script.")
            return # پس از ایجاد، کار تمام است

        with open(README_FILE, 'r', encoding='utf-8') as f:
            readme_content = f.read()

        # Escape markers for regex (though not strictly necessary for these specific strings)
        start_escaped = re.escape(START_MARKER)
        end_escaped = re.escape(END_MARKER)
        
        # Build the regex to find content between markers (inclusive of markers)
        # Use re.DOTALL (s) to make '.' match newlines
        pattern = re.compile(f"({start_escaped})(.*?)({end_escaped})", re.DOTALL)

        # Check if the pattern (markers) exists in the README
        if pattern.search(readme_content):
            # Define the new block content, including markers, to replace the old block
            replacement = f"{START_MARKER}\n{table_content}\n{END_MARKER}"
            # Use re.sub to replace the first occurrence of the block.
            new_readme_content, num_replacements = pattern.subn(replacement, readme_content, count=1)

            if num_replacements == 0:
                # این حالت نباید اتفاق بیفتد اگر pattern.search() موفق بوده باشد
                print(f"Error: Markers were found but no replacement occurred. This is unexpected.")
                # به عنوان یک راه حل موقت، به انتهای فایل اضافه می‌کنیم تا داده از دست نرود، اما این باعث تکرار می‌شود.
                print(f"Appending table to the end of {README_FILE} as a fallback due to replacement failure.")
                if readme_content and not readme_content.endswith('\n'):
                    readme_content += '\n'
                new_readme_content = f"{readme_content}\n{START_MARKER}\n{table_content}\n{END_MARKER}\n"
            elif num_replacements > 1: # Should not happen with count=1
                print(f"Warning: Replaced more than one block. Check your README for duplicate marker sets.")
        else:
            print(f"Warning: Markers '{START_MARKER}' and '{END_MARKER}' not found in {README_FILE}.")
            print(f"Appending table with markers to the end of {README_FILE}.")
            # Ensure there's a newline before appending if the file doesn't end with one
            if readme_content and not readme_content.endswith('\n'):
                readme_content += '\n'
            # اضافه کردن محتوا همراه با نشانگرها اگر نشانگرها وجود نداشتند
            new_readme_content = f"{readme_content}\n{START_MARKER}\n{table_content}\n{END_MARKER}\n"


        # Write the updated content back to README
        print(f"Writing updated content to {README_FILE}...")
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(new_readme_content)

        print(f"✅ {README_FILE} updated successfully.")

    except FileNotFoundError: # این خطا برای TABLE_FILE باید توسط بررسی اولیه گرفته شود
        print(f"Error: A file was not found (e.g. {TABLE_FILE}). Ensure it's created by the previous step.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred in Python script: {e}")
        exit(1)
    finally:
        # Clean up the temporary table file
        if os.path.exists(TABLE_FILE):
            print(f"Cleaning up {TABLE_FILE}...")
            os.remove(TABLE_FILE)

# Ensure the main function is called
if __name__ == "__main__":
    update_readme_with_regex()
