import asyncio
from app.scheduler import Scheduler

if __name__ == "__main__":
    asyncio.run(Scheduler.run_scheduler())
