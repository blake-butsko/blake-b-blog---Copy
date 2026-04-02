import os
import shutil
import re
from datetime import datetime

# ===== CONFIG =====
VAULT_PATH = r"C:\Users\blake\Documents\Blake_Blog"
HUGO_CONTENT_PATH = r"C:\Users\blake\Desktop\Various VS Code projects\Web Dev\Dominoes Blog 4 - Hyde Theme attempt\blake-b-blog - Copy\content"

# ==================

def slugify(text):
    return text.lower().replace(" ", "-")

def generate_frontmatter(filepath, root):
    filename = os.path.basename(filepath)
    slug = filename.replace(".md", "")
    title = slug.replace("-", " ").title()

    rel_path = os.path.relpath(filepath, root)
    folders = os.path.dirname(rel_path).split(os.sep)

    categories = [slugify(f) for f in folders if f]

    date = datetime.utcnow().isoformat() + "Z"

    return f"""+++
title = "{title}"
date = {date}
draft = false
categories = {categories}
slug = "{slug}"
+++

"""

def convert_wikilinks(text):
    # [[Page]] → [Page](/page/)
    text = re.sub(
        r"\[\[([^\]|#]+)\]\]",
        lambda m: f"[{m.group(1)}](/" + slugify(m.group(1)) + "/)",
        text
    )

    # [[#Heading|Text]] → [Text](#heading)
    text = re.sub(
        r"\[\[#([^\]|]+)\|([^\]]+)\]\]",
        lambda m: f"[{m.group(2)}](#{slugify(m.group(1))})",
        text
    )

    return text

def process_file(src_path, dst_path, root):
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = convert_wikilinks(content)

    frontmatter = generate_frontmatter(src_path, root)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

def build_content():
    # wipe existing content (optional but clean)
    if os.path.exists(HUGO_CONTENT_PATH):
        shutil.rmtree(HUGO_CONTENT_PATH)

    for root, dirs, files in os.walk(VAULT_PATH):
        for file in files:
            if file.endswith(".md"):
                src_path = os.path.join(root, file)

                rel_path = os.path.relpath(src_path, VAULT_PATH)
                dst_path = os.path.join(HUGO_CONTENT_PATH, rel_path)

                process_file(src_path, dst_path, VAULT_PATH)

def create_index_files():
    for root, dirs, files in os.walk(HUGO_CONTENT_PATH):
        index_path = os.path.join(root, "_index.md")

        if not os.path.exists(index_path):
            folder_name = os.path.basename(root)
            title = folder_name.replace("-", " ").title()

            with open(index_path, "w", encoding="utf-8") as f:
                f.write(f"+++\ntitle = \"{title}\"\n+++\n")

if __name__ == "__main__":
    build_content()
    create_index_files()
    print("✅ Content pipeline complete.")