#===============================================================================
#
#          FILE: validate_taxonomy.py
#
#         USAGE: python validate_taxonomy.py <json_ld_file>
#
#   DESCRIPTION: Validates JSON-LD taxonomies following DFC naming conventions:
#                - Must be valid JSON-LD
#                - IDs must be alphanumeric
#                - IDs must start with a letter
#                - Classes use PascalCase
#                - Properties use camelCase
#
#===============================================================================

import sys

from validator import TaxonomyValidator

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_taxonomy.py <json_ld_file>")
        sys.exit(1)

    tv = TaxonomyValidator(sys.argv[1])
    if tv.validate():
        print(f"\n✨ PASS {tv.file_path.name} is valid!")
        sys.exit(0)

    count = tv.get_errors_count()
    print(f"\n❌ FAIL Found {count} issues in {tv.file_path.name}:\n")
    tv.print_errors()
    sys.exit(1)

if __name__ == "__main__":
    main()