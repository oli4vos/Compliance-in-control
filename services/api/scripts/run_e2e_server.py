import os
from pathlib import Path

database = Path(__file__).resolve().parents[1] / "e2e.db"
database.unlink(missing_ok=True)
os.environ["AANTOONBAAR_DATABASE_URL"] = f"sqlite:///{database}"
os.environ["AANTOONBAAR_AUTO_SEED_DEMO"] = "false"

import uvicorn  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.modules.projects import models  # noqa: E402, F401

Base.metadata.create_all(engine)
uvicorn.run(app, host="127.0.0.1", port=18000)
