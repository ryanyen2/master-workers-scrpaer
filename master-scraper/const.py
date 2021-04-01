import dotenv
import os
from pathlib import Path


current_dir = Path(__file__).parent.absolute()

env_file = os.getenv("MASTER_ENV_FILE", current_dir.parent.joinpath(".env"))
dotenv.load_dotenv(env_file, verbose=True)


def load_env_variable(key, default_value=None, none_allowed=False):
    v = os.getenv(key, default=default_value)
    if v is None and not none_allowed:
        raise RuntimeError(f"{key} returned {v} but this is not allowed.")
    return v


USERNAME = load_env_variable("TWITTER_USERNAME", none_allowed=True)
PASSWORD = load_env_variable("TWITTER_PASSWORD", none_allowed=True)

APP_ENV = os.getenv('APP_ENV', 'local')
if APP_ENV == 'development':
    DB_HOST = load_env_variable('DEV_DB_HOST', none_allowed=True)
elif APP_ENV == 'production':
    DB_HOST = load_env_variable('PROD_DB_HOST', none_allowed=True)
else:
    DB_HOST = load_env_variable('DB_HOST', none_allowed=True)

DB_USERNAME = load_env_variable('DB_USERNAME', none_allowed=True)
DB_PASSWORD = load_env_variable('DB_PASSWORD', none_allowed=True)
DB_DATABASE = load_env_variable('DB_DATABASE', none_allowed=True)


# if using redis channel => enable these lines
# REDIS_DB_HOST = load_env_variable('REDIS_DB_HOST', none_allowed=True)
# REDIS_DB_PORT = load_env_variable('REDIS_DB_PORT', none_allowed=True)
# REDIS_DB_NO = load_env_variable('REDIS_DB_NO', none_allowed=True)
# REDIS_DB_CHANNEL = load_env_variable('REDIS_DB_CHANNEL', none_allowed=True)

