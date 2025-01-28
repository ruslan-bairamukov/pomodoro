from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from handlers import routers

app = FastAPI()
for router in routers:
    app.include_router(router=router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
