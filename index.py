# Vercel finds the FastAPI app here (a root index.py exporting `app`): no rewrites needed.
from app.main import app  # noqa: F401
