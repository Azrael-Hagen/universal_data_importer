from pathlib import Path
from core.engine import ImportEngine

engine = ImportEngine()

file = Path("test.csv")

engine.detect_format(file)

preview = engine.load_preview(file)

schema = engine.detect_schema(preview)

print(schema)