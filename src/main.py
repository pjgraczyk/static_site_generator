import os
import sys
from logger import initialize_logger, log_message
from file_utils import (
    move_src_to_dest_dir,
    generate_pages_recursive,
)


def main():
    initialize_logger()
    log_message("Starting the script", "info")

    base_path = sys.argv[1]
    src_path = os.path.join(base_path, "static")
    dest_path = os.path.join(base_path, "public")
    content_path = os.path.join(base_path, "content")
    template_path = base_path

    move_src_to_dest_dir(src_path=src_path, dest_dir=dest_path)
    log_message("Source files moved to destination directory", "info")

    generate_pages_recursive(
        from_path=content_path,
        template_path=template_path,
        dest_path=dest_path,
    )
    log_message("HTML pages generated recursively", "info")
    log_message("Script completed successfully", "info")


if __name__ == "__main__":
    main()
