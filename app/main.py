from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import email, call, upload

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",  # Next.js development server
    "http://localhost:3000",  # Sometimes it's accessed via localhost
    "*"
]

# Enable CORS so Next.js frontend can communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Update this to your frontend URL in production
    #allow_origins=[os.getenv("NEXT_PUBLIC_FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the scraper API
app.include_router(email.router, prefix="/api")
app.include_router(call.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Multi Task LLMs and Chain is running!"}
