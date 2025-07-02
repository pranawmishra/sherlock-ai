from tests.test_local import test_main
from tests.test_configuration import test_configuration_complete
import asyncio

async def main():
    print("Hello from sherlock-ai!")
    # await test_main()
    # await test_configuration_complete()


if __name__ == "__main__":
    asyncio.run(main())
