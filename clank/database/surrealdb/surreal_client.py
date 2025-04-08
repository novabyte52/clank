from surrealdb import AsyncSurreal


class SurrealDBClient:
    def __init__(self, ns="clank", db="vault"):
        self.client = None
        self.ns = ns
        self.db = db

    @classmethod
    async def from_config(cls, config: dict):
        """
        Creates and connects a SurrealDBClient using a config dict.
        Example shape:
        {
            "host": "localhost",
            "port": 8000,
            "protocol": "ws",
            "rpc_path": "/rpc",
            "namespace": "clank",
            "database": "vault",
            "username": "root",
            "password": "root"
        }
        """
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

    async def create(self, table: str, data: dict, record_id: str = None):
        if record_id:
            return await self.client.create(f"{table}:{record_id}", data)
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

        note_uuid = note_data["frontmatter"]["id"]
        await db.create("note", note_data, record_id=note_uuid)

        # Tags (optional step, coming later)
        # for tag in note_data["frontmatter"].get("tags", []):
        #     await db.create("tag", { "name": tag })
        #     await db.query(f"RELATE note:{note['note_id']}->note_tag->tag:{tag}")

        for chunk in note["chunks"]:
            chunk_data = {
                "chunk_index": chunk["index"],
                "content": chunk["content"],
                "headers": chunk["headers"],
                "note": f"note:{note_uuid}"
            }

            await db.create("chunk", chunk_data)

            # Links (optional step, coming later)
            # for link in chunk.get("links", []):
            #     if link["resolved"]:
            #         await db.query(f"""
            #             RELATE chunk:{chunk['id']}->chunk_link->chunk:{resolved_chunk_id}
            #         """)