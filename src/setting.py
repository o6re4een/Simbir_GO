from envparse import Env

env =Env()

REAL_DB_URL= env.str(
    "REAL_DB_URL",
    default="postgresql+asyncpg://postgress:root@localhost:5432/simbir"
)

JWT_SECRET = env.str(
    "JWT_SECRET",
    default="secret"
)