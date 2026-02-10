import asyncio, httpx, time

async def hit():
    async with httpx.AsyncClient() as c:
        await c.post("http://localhost:8000/reward/decide", json={
            "txn_id": "t",
            "user_id": "user1",
            "merchant_id": "m1",
            "amount": 100,
            "txn_type": "PAY",
            "ts": "2024-01-01T00:00:00"
        })

async def main():
    await asyncio.gather(*[hit() for _ in range(300)])


start = time.time()
asyncio.run(main())
print("Total time:", time.time() - start)
