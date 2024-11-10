import aiosqlite
import pandas as pd

from core.config import DB_URL


async def add_request(theme, description, request_type, 
                      request_type_probability, hardware_type, hardware_type_probability):
    async with aiosqlite.connect(DB_URL) as connection:
        cursor = await connection.cursor()
        request = await cursor.execute('INSERT INTO `requests` (`theme`, `description`, `request_type`, `request_type_probability`, `hardware_type`, `hardware_type_probability`) VALUES (?, ?, ?, ?, ?, ?)',
                       (theme, description, request_type, request_type_probability, hardware_type, hardware_type_probability,))

        await connection.commit()
        return cursor.lastrowid
    

async def add_serial_number(request_id, serial_number):
    async with aiosqlite.connect(DB_URL) as connection:
        cursor = await connection.cursor()
        request = await cursor.execute('INSERT INTO `serial_numbers` (`request_id`, `serial_number`) VALUES (?, ?)',
                                 (request_id, serial_number,))
        await connection.commit()


async def fetch_request_types():
    async with aiosqlite.connect(DB_URL) as connection:
        cursor = await connection.cursor()
        await cursor.execute('SELECT `request_type` FROM `requests`')
        rows = await cursor.fetchall()

        return pd.DataFrame(rows, columns=["request_type"])
    

async def fetch_hardware_types():
    async with aiosqlite.connect(DB_URL) as connection:
        cursor = await connection.cursor()
        await cursor.execute('SELECT `hardware_type` FROM `requests`')
        rows = await cursor.fetchall()

        return pd.DataFrame(rows, columns=["hardware_type"])
    

async def fetch_serial_numbers_statistics():
    async with aiosqlite.connect(DB_URL) as connection:
        cursor = await connection.cursor()

        await cursor.execute('SELECT `id` FROM `requests`')
        requests = await cursor.fetchall()

        await cursor.execute('SELECT `request_id` FROM `serial_numbers`')
        serial_numbers = await cursor.fetchall()

        return pd.DataFrame(requests, columns=["id"]), pd.DataFrame(serial_numbers, columns=["request_id"])
    