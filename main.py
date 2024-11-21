# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import function

# Specify the archiving condition (adjust as needed)
archiving_condition = "creation_date < SYSDATE - 365"  # Example: Archive records older than 1 year
if __name__ == '__main__':
    function.archive_schema_tables(archiving_condition)