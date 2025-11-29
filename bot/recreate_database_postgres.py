from bot.infrastructure.storage_postgres import StoragePostgres
import asyncio


async def main():
    await StoragePostgres().recreate_database()


if __name__ == "__main__":
    asyncio.run(main())
