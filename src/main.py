import os
from logger import initialize_logger, log_message
from file_utils import (
    move_src_to_dest_dir,
    generate_pages_recursive,
)


def main():
    initialize_logger()
    log_message("Starting the script", "info")

    src_path = os.path.abspath(os.path.join(__file__, "../../static"))
    dest_path = os.path.abspath(os.path.join(__file__, "../../public"))
    content_path = os.path.abspath(os.path.join(__file__, "../../content"))
    template_path = os.path.abspath(os.path.join(__file__, "../../"))

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
