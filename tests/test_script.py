from constants import AUTHOR_NAME, EXAMPLE_API_URL, MAX_SPEED_LIMIT, MAX_WAIT_TIME, TIMEOUT_SECONDS
from sherlock_ai import hardcoded_value_detector
import asyncio
from sherlock_ai import SherlockAI, LoggingConfig
config = LoggingConfig(log_format_type='json')
sherlock_ai = SherlockAI(config=config)
sherlock_ai.setup()


@hardcoded_value_detector
async def third_function():
    s = AUTHOR_NAME
    num = MAX_SPEED_LIMIT
    print(f'Connecting to {s} with timeout {num}')

    @hardcoded_value_detector
    async def second_function():
        url = EXAMPLE_API_URL
        timeout = TIMEOUT_SECONDS
        print(f'Connecting to {url} with timeout {timeout}')
    await second_function()


if __name__ == '__main__':
    asyncio.run(third_function())
