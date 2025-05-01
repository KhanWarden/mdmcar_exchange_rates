import asyncio
from app.scheduler import run_scheduler


if __name__ == "__main__":
    try:
        asyncio.run(run_scheduler())
    except KeyboardInterrupt:
        print("Stopped")
