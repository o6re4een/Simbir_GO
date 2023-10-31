from envparse import env

env.read_envfile("./.env")


enviromnet = env.str(
    "prod",
    default = False
)
DB_HOST = env.str(
    "POSTGRES_HOST",
    default = "localhost"
)
DB_NAME = env.str(
    "POSTGRES_DB",
    default = "simbir"
)

DB_PORT = env.int(
    "POSTGRES_PORT",
    default = 5432
)
DB_USER = env.str(
    "POSTGRES_USER",
    default = "postgres"
)
DB_PASS = env.str(
    'POSTGRES_PASS', 
    default="root"
)

    
REAL_DB_URL= env.str(
    "REAL_DB_URL",
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

JWT_SECRET = env.str(
    "JWT_SECRET",
    default="secret"
)
print(REAL_DB_URL)