from os import environ
from pydantic import BaseSettings


ENV_PREFIX = 'FASMS_'
DEV_PROD_ENV: str = environ.get(ENV_PREFIX + 'DEV_PROD_ENV', 'dev')
IS_PROD: bool = True if DEV_PROD_ENV == 'prod' else False
IS_DEV: bool = True if DEV_PROD_ENV == 'dev' else False


class FastAPISimpleMutexServerConfig(BaseSettings):
    port_number: int
    service_name: str = 'FastAPI Simple Mutex Server'
    redis_dsn: str
    default_mutex_expire: int = 3600 # one hour
    api_key: str

    class Config:
        env_prefix = ENV_PREFIX


if IS_DEV:
    service_config: FastAPISimpleMutexServerConfig = FastAPISimpleMutexServerConfig(
        port_number = 7777,
        redis_dsn = 'redis://localhost',
        api_key = 'solarwinds123'
    )
elif IS_PROD:
    service_config: FastAPISimpleMutexServerConfig = FastAPISimpleMutexServerConfig()
else:
    print(f'{ENV_PREFIX}DEV_PROD_ENV must be set to either "dev" or "prod", but "{DEV_PROD_ENV}" was given!')
    exit(1)


APP_VERSION = None
version_files = ['VERSION', '/usr/src/app/VERSION']
for version_file in version_files:
    try:
        APP_VERSION = open(version_file).read()
        APP_VERSION = APP_VERSION.strip()
        break
    except FileNotFoundError:
        pass

