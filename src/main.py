
import uvicorn
from fastapi import FastAPI


from api.routes import all_routers







app = FastAPI(
    title="SimbirGO",
    # lifespan=lifespan
)



for router in all_routers:
    app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0", port=8000)