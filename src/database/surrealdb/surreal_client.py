from surrealdb import AsyncSurreal


class SurrealDBClient:
    def __init__(self, ns="clank", db="vault"):
        self.client = None
        self.ns = ns
        self.db = db

    @classmethod
    async def from_config(cls, config: dict):
        url = f"{config['protocol']}://{config['host']}:{config['port']}{config['rpc_path']}"
        client = cls(ns=config["namespace"], db=config["database"])
        client.client = AsyncSurreal(url)
        
        await client.client.signin({
            "username": config["username"],
            "password": config["password"]
        })

        await client.client.use(config["namespace"], config["database"])
        
        return client

    async def query(self, surrealql: str):
        return await self.client.query(surrealql)
    
    async def select(self, table: str, where: str):
        return await self.query(f"SELECT * FROM {table} WHERE {where}")

    async def upsert(self, table: str, data: dict, record_id=None):
        """Upserts a record using the SDK-native method."""
        if record_id:
            return await self.client.upsert(f"{table}:{record_id}", data)
        
        return await self.client.create(table, data)

    async def close(self):
        await self.client.close()


async def insert_notes_to_surreal(notes, db: SurrealDBClient):
    for note in notes:
        note_data = {
            "slug": note["slug"],
            "filepath": note["filepath"],
            "frontmatter": note.get("frontmatter", {})
        }

        note_ulid = note_data["frontmatter"]["id"]
        await db.upsert("note", note_data, record_id=note_ulid)

        for tag in note_data["frontmatter"].get("tags", []):
            print(f"SELECT * FROM tag WHERE name = {tag}")
            existing_tag = await db.client.query(f"SELECT * FROM tag WHERE name = '{tag}'")
            
            if existing_tag and existing_tag[0]:
                print(existing_tag)
                tag_id = existing_tag[0]['id']
                new_tag = await db.upsert("tag", { "name": tag }, record_id=tag_id.id)
            else:
                new_tag = await db.upsert("tag", { "name": tag })

            await db.query(f'RELATE note:{note_ulid}->note_tag->{new_tag["id"]}')

        for chunk in note["chunks"]:
            chunk_data = {
                "chunk_index": chunk["index"],
                "content": chunk["content"],
                "headers": chunk["headers"],
                "note": f"note:{note_ulid}"
            }

            existing_chunk = await db.client.query(f"SELECT * FROM chunk WHERE index = {chunk['index']} AND note = {chunk_data['note']}")

            if  existing_chunk and existing_chunk[0]:
                chunk_id = existing_chunk[0]['id']
                new_chunk = await db.upsert("chunk", chunk_data, record_id=chunk_id.id)
            else:
                new_chunk = await db.upsert("chunk", chunk_data)

            for link in chunk.get("links", []):
                if link["resolved"]:
                    await db.query(f"""
                        RELATE {new_chunk['id']}->chunk_links_note->{link['resolved']}
                    """)
