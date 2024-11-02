from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import orjson
import sys


from app.api.endpoints import files
from app.core import settings
from app.utils.folder_util import initialize_shared_folder
from app.lifespan import lifespan

initialize_shared_folder(settings.UPLOAD_DIR)
app = FastAPI(lifespan=lifespan)

# Include routers for different parts of the API
app.include_router(files.router, prefix="/api/files", tags=["Files"])

# Mount the shared files directory as a static path
app.mount("/storage", StaticFiles(directory=settings.UPLOAD_DIR), name="MizbanShared")


if __name__ == '__main__':

    async_loop = "uvloop" if sys.platform == 'linux' else "asyncio"
    uvicorn.run(app, host="0.0.0.0", port=8000, loop=async_loop, http='httptools', log_level='critical')