import aiosqlite
import asyncio
from core.config import DB_URL


async def main():
    async with aiosqlite.connect(DB_URL) as connection:
        cursor = await connection.cursor()

        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme TEXT NOT NULL,
        description TEXT NOT NULL,
        request_type TEXT NOT NULL,
        request_type_probability TEXT NOT NULL,
        hardware_type TEXT NOT NULL,
        hardware_type_probability TEXT NOT NULL
        )''')

        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS serial_numbers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id INTEGER NOT NULL,
        serial_number TEXT NOT NULL
        )''')

        await connection.commit()

if __name__=='__main__':
   asyncio.run(main()) 
