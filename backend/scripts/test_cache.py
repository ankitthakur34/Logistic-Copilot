from app.rag.cache.joblib_cache import JoblibCache

cache = JoblibCache()

cache.save(
    "numbers",
    [1, 2, 3]
)

print(
    cache.load("numbers")
)