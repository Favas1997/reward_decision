from fastapi import FastAPI
from app.api.reward import router
from dotenv import load_dotenv


load_dotenv()


app = FastAPI(title="Reward Decision Service")
app.include_router(router)
