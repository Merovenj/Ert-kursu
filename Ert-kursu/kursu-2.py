import asyncio
import json
import redis.asyncio as aioredis

# Hard limits to protect your Relational Database Management System (RDBMS)
MAX_CONCURRENT_DB_WRITES = 50
db_semaphore = asyncio.Semaphore(MAX_CONCURRENT_DB_WRITES)


async def process_single_vote(raw_vote_data: str):
    """Worker task that actually commits data to the persistent DB."""
    async with db_semaphore:
        vote = json.loads(raw_vote_data)

        try:
            # --- Simulated Database Transaction Block ---
            # In production, use your DB pool here (e.g., asyncpg for PostgreSQL)
            # await db_pool.execute(
            #     "INSERT INTO votes (voter_id, candidate_id) VALUES ($1, $2)",
            #     vote['voter_id'], vote['candidate_id']
            # )

            await asyncio.sleep(0.02)  # Simulate optimized DB write (20ms)
            print(f"🔒 [DB Success] Vote committed for voter: {vote['voter_id']}")

        except Exception as e:
            # If DB write fails (e.g. deadlock), push to a Dead Letter Queue (DLQ)
            print(f"❌ [DB Failure] Redirecting to retry queue: {e}")


async def main_worker_loop():
    r_client = aioredis.Redis(host='localhost', port=6379, db=0)
    print("🚀 Voting background worker initialized. Awaiting queue items...")

    while True:
        # 1. Fetch data from Redis queue. BLPOP blocks until an item is available.
        # It pops 1 item out atomically, ensuring no two workers process the same vote.
        queue_name, raw_vote = await r_client.blpop("voting_queue")

        if raw_vote:
            # 2. Schedule the DB task asynchronously.
            # The loop keeps pulling from Redis instantly without waiting for the DB write to finish.
            asyncio.create_task(process_single_vote(raw_vote.decode('utf-8')))


if __name__ == "__main__":
    asyncio.run(main_worker_loop())
print("=== User Input Choice Example ===\n")

# *This part is for experimental purposes only*

# choice = input('Choose an option:\n1. Option A (Take one)\n2. Option B (Take other)\nEnter 1 or 2: ').strip()

# if choice == "1":
    # Option A: Take one as "YES"
    number = float(input("Enter a number: "))
    result = number ** 2
    print(f"Square of {number} is {result}")
# else:
    # Option B: Take other as "NO"
    number = float(input("Enter a number: "))
    result = number ** 3
    print(f"Cube of {number} is {result}")

