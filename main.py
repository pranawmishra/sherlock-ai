from tests.test_local import test_main
import asyncio

async def main():
    print("Hello from sherlock-ai!")
    await test_main()


if __name__ == "__main__":
    asyncio.run(main())
