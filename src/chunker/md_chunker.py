"""
Markdown Chunker — Parses and chunks Markdown notes into semantically useful units
for embedding, linking, and storage in vector + graph databases.
"""

import re
import json
from urllib.parse import unquote

from pathlib import Path
from typing import List, Dict, Optional, Union, Tuple
from markdown_it import MarkdownIt
from markdown_it.token import Token
import frontmatter


MAX_CHUNK_CHARS = 512


def read_markdown(file_path: Union[str, Path]) -> str:
    """Reads a markdown file and returns its text content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_links_from_tokens(tokens: List[Token]) -> List[str]:
    links = []
    for token in tokens:
        if token.type == "inline":
            for child in token.children or []:
                if child.type == "link_open":
                    href = dict(child.attrs or {}).get("href")
                    if href and href.endswith(".md"):
                        links.append(href)
    return links


def normalize_link(link: str) -> str:
    return unquote(link.strip().removesuffix(".md"))


def extract_header_from_line(line: str) -> Optional[Dict[str, Union[int, str]]]:
    """
    If the line is a markdown header, extract its level and text.
    Returns None otherwise.
    """
    match = re.match(r'^(#{1,6})\s+(.*)', line)
    if not match:
        return None
    return {"level": len(match.group(1)), "text": match.group(2).strip()}


def split_large_text(text: str, max_chars: int = MAX_CHUNK_CHARS) -> List[str]:
    """
    Splits a long block of text into smaller chunks using newlines and periods.
    """
    if len(text) <= max_chars:
        return [text]

    # Prefer newline splits, fallback to sentence-like periods
    parts = re.split(r"(\n{2,}|\.\s)", text)
    chunks = []
    current = ""

    for part in parts:
        if not part.strip():
            continue
        current += part
        if len(current) >= max_chars:
            chunks.append(current.strip())
            current = ""
    if current.strip():
        chunks.append(current.strip())
    return chunks


def chunk_markdown_text_md_it(text: str, include_headers_in_content: bool = True) -> List[Dict]:
    md = MarkdownIt()
    tokens = md.parse(text)

    chunks = []
    current_headers = []
    chunk_index = 0

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.type == "heading_open":
            level = int(token.tag[1])
            heading_token = tokens[i + 1]
            heading_text = heading_token.content.strip()

            # Maintain header hierarchy
            current_headers = [h for h in current_headers if h["level"] < level]
            current_headers.append({ "level": level, "text": heading_text })

            i += 2
            continue

        if token.type in ("paragraph_open", "fence"):
            content_token = tokens[i + 1]
            content = content_token.content.strip()

            # Collect all inline tokens within the paragraph block
            inline_tokens = []
            if content_token.type == "inline":
                inline_tokens.append(content_token)

            # Look ahead for more inlines (some plugins or structures might inject them)
            j = i + 2
            while j < len(tokens) and tokens[j].type not in ("paragraph_open", "heading_open", "fence"):
                if tokens[j].type == "inline":
                    inline_tokens.append(tokens[j])
                j += 1

            links = extract_links_from_tokens(inline_tokens)

            if include_headers_in_content:
                header_str = "\n".join(f"{'#' * h['level']} {h['text']}" for h in current_headers)
                content = f"{header_str}\n\n{content}"

            for part in split_large_text(content):
                chunks.append({
                    "index": chunk_index,
                    "content": part.strip(),
                    "headers": list(current_headers),
                    "links": [
                        { "raw": link, "resolved": None }
                        for link in map(normalize_link, links)
                    ]
                })
                chunk_index += 1

            i = j
        else:
            i += 1

    return chunks


def extract_frontmatter(text: str) -> Tuple[Dict, str]:
    """
    Extracts frontmatter using the `python-frontmatter` package.

    Returns:
        Tuple[frontmatter_dict, content_str]
    """
    try:
        post = frontmatter.loads(text)
        return post.metadata, post.content.strip()
    except Exception:
        return {}, text


def chunk_markdown_note(file_path: Path) -> Dict:
    """
    Parses a single markdown note and returns a structured note dictionary:
    {
        slug, filepath, frontmatter, chunks[]
    }
    """
    raw_text = read_markdown(file_path)
    fm, content = extract_frontmatter(raw_text)
    chunks = chunk_markdown_text_md_it(content)

    note = {
        "slug": file_path.stem.replace(" ", "-").lower(),  # simple slug
        "filepath": str(file_path),
        "frontmatter": fm,
        "chunks": chunks
    }
    return note


def load_all_notes_in_dir(directory: Union[str, Path]) -> List[Dict]:
    """
    Loads and chunks all markdown notes in a directory.
    Returns a list of structured note objects.
    """
    notes = []
    print(f"[Chunker] Scanning directory: {directory}")

    for path in Path(directory).rglob("*.md"):
        print(f"[Chunker] Found file: {path}")
        note = chunk_markdown_note(path)
        notes.append(note)

    return notes


def write_notes_to_json(notes: List[Dict], out_path: Union[str, Path]) -> None:
    """
    Writes full note structures (with frontmatter + chunks) to JSON.
    """
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

    print(f"[Serializer] ✅ Wrote {len(notes)} notes to {path}")
