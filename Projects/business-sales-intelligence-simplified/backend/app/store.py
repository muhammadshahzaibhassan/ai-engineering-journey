"""
Simple in-memory session store.

Each uploaded CSV gets a session_id (uuid4). We keep the raw df, cleaned df,
customer feature table, trained pipelines, and metrics all keyed by that id.
This is intentionally NOT a database -- it's a demo/portfolio app. Sessions
are lost on server restart, which is fine for the free tier this is meant
to be deployed on (Render). If you outgrow this, swap Session for a Redis-
or Postgres-backed store; every other module only talks to get_session().
"""
from __future__ import annotations
import uuid
import time
import threading
from dataclasses import dataclass, field
from typing import Optional
import pandas as pd

SESSION_TTL_SECONDS = 60 * 60 * 6  # 6 hours


@dataclass
class Session:
    id: str
    created_at: float = field(default_factory=time.time)
    filename: str = ""
    raw_df: Optional[pd.DataFrame] = None
    schema: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)
    cleaned_df: Optional[pd.DataFrame] = None
    cleaning_log: list = field(default_factory=list)
    customer_features: Optional[pd.DataFrame] = None
    returns_df: Optional[pd.DataFrame] = None
    models: dict = field(default_factory=dict)          # name -> sklearn Pipeline
    metrics: Optional[list] = None                        # list of dicts per model
    feature_importance: Optional[list] = None
    best_model_name: Optional[str] = None


_sessions: dict[str, Session] = {}
_lock = threading.Lock()


def create_session() -> Session:
    _evict_expired()
    sid = str(uuid.uuid4())
    s = Session(id=sid)
    with _lock:
        _sessions[sid] = s
    return s


def get_session(session_id: str) -> Session:
    with _lock:
        s = _sessions.get(session_id)
    if s is None:
        raise KeyError(f"Unknown or expired session_id: {session_id}")
    return s


def _evict_expired():
    now = time.time()
    with _lock:
        expired = [k for k, v in _sessions.items() if now - v.created_at > SESSION_TTL_SECONDS]
        for k in expired:
            del _sessions[k]
