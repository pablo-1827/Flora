from pathlib import Path


def test_alembic_files_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "alembic.ini").exists()
    assert (root / "alembic" / "env.py").exists()
    assert (root / "alembic" / "script.py.mako").exists()
    assert (root / "alembic" / "versions").exists()


def test_model_metadata_is_visible_to_alembic():
    from app.core.database import Base

    assert len(Base.metadata.tables) > 0
    assert "users" in Base.metadata.tables
    assert "opportunities" in Base.metadata.tables
    assert "applications" in Base.metadata.tables
