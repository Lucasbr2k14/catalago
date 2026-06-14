from os import getenv

bind = f"{getenv('HOST')}:{getenv('PORT')}"

workers = int(
    getenv("WORKERS", "2")
)

timeout = int(
    getenv("TIMEOUT", "60")
)