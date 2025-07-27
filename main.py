# from tests.test_local import test_main
# from tests.test_configuration import test_configuration_complete
import asyncio
import uvicorn
from sherlock_ai import get_logging_stats, get_current_config, SherlockAI, LoggingConfig, LogFileConfig, LoggerConfig
from dotenv import load_dotenv

load_dotenv()

log_files={
    "app": LogFileConfig("app", max_bytes=50*1024*1024),
    "api": LogFileConfig("api", max_bytes=50*1024*1024),
    "errors": LogFileConfig("errors", level="ERROR"),
    "performance": LogFileConfig("performance"),
    "custom": LogFileConfig("custom", backup_count=10)
}

config = LoggingConfig(
    # log_files=log_files,
    # loggers=loggers,
    log_format_type="json"
)

logging_manager = SherlockAI(config=config)
logging_manager.setup()

# async def main():
#     print("Hello from sherlock-ai!")
    # await test_main()
    # await test_configuration_complete()


if __name__ == "__main__":
    # stats = get_logging_stats()
    # print(stats)
    # config = get_current_config()
    # print(config)
    uvicorn.run(
        "tests.test_fastapi:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
