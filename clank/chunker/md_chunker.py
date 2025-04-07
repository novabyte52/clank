"""
Markdown Chunker — Parses and chunks Markdown notes into semantically useful units
for embedding, linking, and storage in vector + graph databases.

Each chunk includes:
- A unique ID
- The full filepath
- Contextual header breadcrumbs
- Normalized wiki/markdown-style links
- (Future: inline tags, frontmatter, etc.)

Example output:

{
  "id": "chunk_5",
  "note_id": "grand-whimsy",
  "filepath": "markdown_testing/grand whimsy.md",
  "content": "...",
  "headers": [{ "level": 1, "text": "Grand Whimsy" }],
  "links": [
    { "raw": "vector-embeddings", "resolved": null },
    { "raw": "cosmic-design", "resolved": null }
  ]
}
"""

import re
import json
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Union


# ─────────────────────────────────────────────────────────────
# 🔹 File Handling
# ─────────────────────────────────────────────────────────────

def read_markdown(file_path: Union[str, Path]) -> str:
    """Reads a markdown file and returns its text content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# ─────────────────────────────────────────────────────────────
# 🔹 Link Parsing & Normalization
# ─────────────────────────────────────────────────────────────

def extract_links(text: str) -> List[str]:
    """
    Extracts internal links from markdown text.
    Supports [[wiki-style]] and [Markdown](file.md) formats.
    """
    wiki_links = re.findall(r'\[\[([^\]]+)\]\]', text)
    md_links = re.findall(r'\[.*?\]\(([^)]+\.md)\)', text)
    return list(set(wiki_links + md_links))


def normalize_link(link: str) -> str:
    """Strips .md extensions and lowercases the link for consistent comparison."""
    return link.strip().lower().replace(".md", "")


# ─────────────────────────────────────────────────────────────
# 🔹 Header-Aware Markdown Chunking
# ─────────────────────────────────────────────────────────────

def extract_header_from_line(line: str) -> Optional[Dict[str, Union[int, str]]]:
    """
    If the line is a markdown header, extract its level and text.
    Returns None otherwise.
    """
    match = re.match(r'^(#{1,6})\s+(.*)', line)
    if not match:
        return None
    return {"level": len(match.group(1)), "text": match.group(2).strip()}


def chunk_markdown_text(text: str, include_headers_in_content: bool = True) -> List[Dict]:
    """
    Splits markdown text into semantically meaningful chunks.
    Uses headers and blank lines as structure hints.

    Each chunk:
    - Includes active headers as breadcrumb metadata.
    - Optionally prepends the most recent header to the content itself.

    Args:
        text (str): Raw markdown content.
        include_headers_in_content (bool): Whether to prepend header to chunk text.

    Returns:
        List[Dict]: List of chunk objects.
    """
    lines = text.splitlines()
    chunks = []
    current_chunk = ""
    header_stack = []
    next_header_line = ""

    def flush_chunk():
        nonlocal current_chunk, next_header_line
        if current_chunk.strip():
            chunk_text = current_chunk.strip()
            if include_headers_in_content and next_header_line:
                chunk_text = f"{next_header_line}\n\n{chunk_text}"
            chunks.append({
                "id": f"chunk_{len(chunks)}",
                "content": chunk_text,
                "headers": list(header_stack)
            })
        current_chunk = ""
        next_header_line = ""

    for line in lines:
        header = extract_header_from_line(line)
        if header:
            flush_chunk()
            # Trim header stack to maintain hierarchy
            header_stack[:] = [h for h in header_stack if h["level"] < header["level"]]
            header_stack.append(header)
            next_header_line = f"{'#' * header['level']} {header['text']}"
        elif line.strip() == "":
            flush_chunk()
        else:
            current_chunk += line + "\n"

    flush_chunk()
    return chunks


# ─────────────────────────────────────────────────────────────
# 🔹 Chunking a Single File
# ─────────────────────────────────────────────────────────────

def extract_frontmatter(text: str) -> (Dict, str):
    """
    Extracts YAML-style frontmatter from markdown and returns the remaining body.

    Returns:
        Tuple[frontmatter_dict, content_str]
    """
    if text.startswith("---"):
        try:
            _, front, rest = text.split("---", 2)
            frontmatter = yaml.safe_load(front)
            return frontmatter or {}, rest.strip()
        except (ValueError, yaml.YAMLError):
            pass
    return {}, text


def chunk_markdown_file(file_path: Path) -> List[Dict]:
    """
    Processes a single markdown file into structured chunks,
    with filepath and extracted links attached.

    Args:
        file_path (Path): Path to a markdown file.

    Returns:
        List[Dict]: List of structured chunk dictionaries.
    """
    raw_text = read_markdown(file_path)
    frontmatter, content = extract_frontmatter(raw_text)
    chunks = chunk_markdown_text(content)

    for chunk in chunks:
        chunk["filepath"] = str(file_path)
        chunk["frontmatter"] = frontmatter

        raw_links = extract_links(chunk["content"])
        chunk["links"] = [
            { "raw": link, "resolved": None }
            for link in map(normalize_link, raw_links)
        ]

    return chunks


# ─────────────────────────────────────────────────────────────
# 🔹 Directory-Wide Chunking
# ─────────────────────────────────────────────────────────────

def chunk_all_markdown_in_dir(directory: Union[str, Path]) -> List[Dict]:
    """
    Recursively chunks all `.md` files in a directory.

    Args:
        directory (str | Path): Root directory to scan.

    Returns:
        List[Dict]: All chunks from all files.
    """
    all_chunks = []
    print(f"[Chunker] Scanning directory: {directory}")

    for path in Path(directory).rglob("*.md"):
        print(f"[Chunker] Found file: {path}")
        all_chunks.extend(chunk_markdown_file(path))

    return all_chunks


# ─────────────────────────────────────────────────────────────
# 🔹 JSON Output Helper
# ─────────────────────────────────────────────────────────────

def write_chunks_to_json(chunks: List[Dict], out_path: Union[str, Path]) -> None:
    """
    Writes a list of chunk dictionaries to a readable JSON file.

    Args:
        chunks (List[Dict]): Chunk objects.
        out_path (str | Path): Destination JSON file path.
    """
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"[Serializer] ✅ Wrote {len(chunks)} chunks to {path}")
