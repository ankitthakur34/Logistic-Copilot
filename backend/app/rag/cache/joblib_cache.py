from pathlib import Path

import joblib

from app.rag.cache.base_cache import BaseCache


class JoblibCache(BaseCache):

    def __init__(
        self,
        cache_dir: str = "cache",
    ):

        self.cache_dir = Path(cache_dir)

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _path(
        self,
        key: str,
    ) -> Path:

        return self.cache_dir / f"{key}.joblib"

    def save(
        self,
        key: str,
        data,
    ) -> None:

        joblib.dump(
            data,
            self._path(key),
            compress=3,
        )

    def load(
        self,
        key: str,
    ):

        return joblib.load(
            self._path(key)
        )

    def exists(
        self,
        key: str,
    ) -> bool:

        return self._path(key).exists()

    def delete(
        self,
        key: str,
    ) -> None:

        path = self._path(key)

        if path.exists():
            path.unlink()