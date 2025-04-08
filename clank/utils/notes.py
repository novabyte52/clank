from pathlib import Path
from typing import List, Dict
import frontmatter
import uuid

def build_note_reference_index(notes: List[Dict]) -> Dict[str, str]:
    """
    Builds a mapping of link targets to filepaths using:
    - File stems (e.g., 'Aloysius Aster')
    - Frontmatter titles (e.g., 'Grand Whimsy')

    Returns:
        Dict[raw_link_target] -> filepath
    """
    index = {}
    for note in notes:
        fm = note.get("frontmatter")
        note_uuid = fm.get("id")

        filepath = note.get("filepath")
        file_stem = Path(filepath).stem

        index[file_stem] = note_uuid

        title = note.get("frontmatter", {}).get("title")
        if title:
            index[title] = note_uuid

    return index


def resolve_links_in_notes(notes: List[Dict]) -> None:
    """
    Iterates over each note and each chunk, updating unresolved links
    with their matched `resolved` filepath (if found in the index).
    """
    index = build_note_reference_index(notes)

    for note in notes:
        for chunk in note["chunks"]:
            for link in chunk.get("links", []):
                raw_target = link["raw"]
                if link.get("resolved") is None:
                    link["resolved"] = f"note:{index.get(raw_target)}"


def inject_uuid_into_notes(notes_dir):
    for md_path in Path(notes_dir).rglob("*.md"):
        post = frontmatter.load(md_path)
        if "id" not in post.metadata:
            post.metadata["id"] = str(uuid.uuid4())
            frontmatter.dump(post, md_path)
            print(f"[UUID] Added id to {md_path}")
        else:
            print(f"[UUID] Already has id: {md_path}")
