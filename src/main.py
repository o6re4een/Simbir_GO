# from typing import Union

# import uvicorn
# import setting
# from fastapi import FastAPI

# app = FastAPI()




# for router in all_routers:
#     app.include_router(router)


# if __name__ == "__main__":
#     uvicorn.run(app="main:app", reload=True)

import uvicorn
from fastapi import FastAPI

from api.routes import all_routers


app = FastAPI(
    title="SimbirGO"
)


for router in all_routers:
    app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)