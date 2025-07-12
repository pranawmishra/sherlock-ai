# from tests.test_local import test_main
# from tests.test_configuration import test_configuration_complete
import asyncio
import uvicorn
from sherlock_ai import get_logging_stats, get_current_config, SherlockAI

logging_manager = SherlockAI.get_instance()
# async def main():
#     print("Hello from sherlock-ai!")
    # await test_main()
    # await test_configuration_complete()


if __name__ == "__main__":
    stats = get_logging_stats()
    print(stats)
    config = get_current_config()
    print(config)
    uvicorn.run(
        "tests.test_fastapi:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
