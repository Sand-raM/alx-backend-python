import aiosqlite
import asyncio

DB_FILE = "C:/Users/USER 1/Desktop/Sandra's projects/alx-backend-python/python-context-async-perations-0x02/users.db"
async def async_fetch_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users") as cursor:
           users = await cursor.fetchall()
           print("All Users:")

        for user in users:
            print(user)

        return users
    
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers Older Than 40:")

        for user in older_users:
            print(user)

        return older_users
    
async def fetch_concurrently():
    await asyncio.gather(async_fetch_users(), async_fetch_older_users())

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
        
    
                
