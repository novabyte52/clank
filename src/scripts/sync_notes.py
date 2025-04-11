"""
Runs the note chunking and sync process.
Intended for cron jobs or scheduled tasks.
"""

import asyncio
from clank.config import app_config
from clank.chunker.md_chunker import load_all_notes_in_dir
from clank.utils.notes import resolve_links_in_notes, inject_ulid_into_notes
from clank.database.surrealdb.surreal_client import SurrealDBClient, insert_notes_to_surreal
from clank.chunker.md_chunker import write_notes_to_json


async def run_sync():
    notes_dir = app_config["notes_dir"]

    # inject uuid into notes if needed
    inject_ulid_into_notes(notes_dir)

    # load notes into structure for storage
    notes = load_all_notes_in_dir(notes_dir)
    resolve_links_in_notes(notes)

    write_notes_to_json(notes, "notes_as.json")

    # insert notes into surrealdb
    db = await SurrealDBClient.from_config(app_config["db"]["surrealdb"])
    await insert_notes_to_surreal(notes, db)
    await db.close()


if __name__ == "__main__":
    asyncio.run(run_sync())
