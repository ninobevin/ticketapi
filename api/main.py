from fastapi import FastAPI
from routes.ticket_routes import router as ticket_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (not recommended for production)
origins = ["*"]

# Allow specific origins (recommended for security)
# origins = ["http://localhost", "http://localhost:3000", "https://yourdomain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    return {"Development": "Please Refer to the documentation about the Ticket API."}


app.include_router(ticket_router, prefix="/ticket")


# @app.get("/test")
# async def test_insert():
#     new_user = {
#         "name": "Auto User12",
#         "email": "auto@example.com",
#         "age": 25
#     }
#     result = users_collection.insert_one(new_user)
#     return {"message": "Test user inserted", "user_id": str(result.inserted_id)}
