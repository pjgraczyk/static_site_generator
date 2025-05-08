import os
import shutil
from lxml import etree, html
from jinja2 import Environment, FileSystemLoader
from markdown_utils import markdown_to_html_node, extract_title
from logger import log_message


def format_html(content):
    html_content = markdown_to_html_node(content).to_html()
    document_root = html.fromstring(html_content)
    prettified_html = etree.tostring(
        document_root, encoding="unicode", pretty_print=True
    )
    log_message("Markdown content translated to HTML and formatted", "info")
    return prettified_html


def delete_dest_dir(abspath):
    if not os.path.exists(abspath):
        error = f"The given path of the destination directory does not exist: {abspath}"
        log_message(error, "error")
        raise ValueError(error)

    if not os.listdir(abspath):
        log_message(
            f"The given path of the destination directory is empty: {abspath}", "info"
        )
        return

    for entry in os.listdir(abspath):
        entry_path = os.path.join(abspath, entry)
        if os.path.isfile(entry_path):
            os.remove(entry_path)
            log_message(f"File deleted: {entry_path}", "info")
        elif os.path.isdir(entry_path):
            shutil.rmtree(entry_path)
            log_message(f"Directory deleted: {entry_path}", "info")
    log_message(f"The deletion has been completed for the directory: {abspath}", "info")


def move_src_to_dest_dir(src_path, dest_dir):
    # Make sure the destination directory is cleared
    if os.path.exists(dest_dir):
        delete_dest_dir(dest_dir)
    else:
        log_message(f"Skipping deletion of the existing directory: {dest_dir}", "info")

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        log_message(f"Destination directory created: {dest_dir}", "info")

    for item in os.listdir(src_path):
        s = os.path.join(src_path, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
            log_message(f"Directory moved: {s} to {d}", "info")
        else:
            shutil.copy2(s, d)
            log_message(f"File moved: {s} to {d}", "info")
    log_message(f"All items from {src_path} have been moved to {dest_dir}", "info")
    log_message(f"Source directory: {src_path}", "info")
    log_message(f"Destination directory: {dest_dir}", "info")
    log_message("Moving process completed", "info")


def generate_page(from_path, template_path, dest_path):
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("template.html")
    with open(from_path, "r", encoding="utf-8") as file:
        content = file.read()
    log_message(f"Markdown content read from file: {from_path}", "info")

    title = extract_title(from_path)
    html_body = format_html(content)
    html_content = template.render(Title=title, Content=html_body)
    log_message(f"The HTML content is following: {html_body}", "info")
    log_message(f"The title of the webpage is following: {html_body}", "info")
    log_message("HTML content generated from markdown", "info")

    with open(os.path.join(dest_path, "index.html"), "w", encoding="utf-8") as file:
        file.write(html_content)
        log_message(f"Generated HTML page written to: {dest_path}", "info")
    log_message("HTML page generation completed", "info")


def generate_pages_recursive(from_path, template_path, dest_path):
    if os.path.isdir(from_path):
        # Process all .md files in the current directory
        for item in os.listdir(from_path):
            item_path = os.path.join(from_path, item)
            if os.path.isfile(item_path) and item.endswith(".md"):
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                generate_page(item_path, template_path, dest_path)
        for item in os.listdir(from_path):
            item_path = os.path.join(from_path, item)
            if os.path.isdir(item_path):
                new_dest_dir = os.path.join(
                    dest_path, os.path.relpath(item_path, from_path)
                )
                if not os.path.exists(new_dest_dir):
                    os.makedirs(new_dest_dir)
                    log_message(f"Created directory: {new_dest_dir}", "info")
                generate_pages_recursive(item_path, template_path, new_dest_dir)
    else:
        log_message(f"Provided path is not a directory: {from_path}", "error")
        raise ValueError(f"The provided path is not a directory: {from_path}")
    log_message("Recursive page generation completed", "info")
    log_message(f"All pages generated from markdown files in {from_path}", "info")
    log_message(f"Template path: {template_path}", "info")
    log_message(f"Destination path: {dest_path}", "info")
    log_message("Page generation process completed", "info")
