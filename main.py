from tests.test_local import test_main
from tests.test_configuration import test_configuration_complete
import asyncio
import uvicorn
from sherlock_ai import setup_logging

setup_logging()

# async def main():
#     print("Hello from sherlock-ai!")
    # await test_main()
    # await test_configuration_complete()


if __name__ == "__main__":
    uvicorn.run(
        "tests.test_fastapi:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
