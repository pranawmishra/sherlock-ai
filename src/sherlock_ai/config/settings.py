from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # env_nested_delimiter="_",
        # env_prefix="SHERLOCK_AI_",
        extra="ignore"
    )

    # LLM Provider selection
    llm_provider: str = "groq"

    # Groq
    groq_api_key: str | None = None

    # Azure OpenAI
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_openai_deployment_name: str | None = None

    # Storage
    mongo_uri: str | None = None
    sherlock_ai_api_key: str | None = None

settings = Settings()