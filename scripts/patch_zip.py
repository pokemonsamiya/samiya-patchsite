import sys
import zipfile
from pathlib import Path

PATCH_EXTENSIONS = (".bps", ".ups", ".xdelta")
LIMIT_MB = 100

patches_dir = Path(__file__).resolve().parent.parent / "patches"
zip_path = patches_dir / "patch.zip"

patch_files = [
    f for f in patches_dir.iterdir()
    if f.is_file() and not f.name.startswith(".") and f.suffix.lower() in PATCH_EXTENSIONS
]

if not patch_files:
    sys.exit(f"No patch file found in {patches_dir}")
if len(patch_files) > 1:
    names = "\n  ".join(f.name for f in patch_files)
    sys.exit(f"Found more than one patch file in {patches_dir}, remove the old one(s):\n  {names}")

patch = patch_files[0]
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(patch, arcname=patch.name)

size_mb = zip_path.stat().st_size / (1024 * 1024)
if size_mb > LIMIT_MB:
    zip_path.unlink()
    sys.exit(f"ERROR: zip is {size_mb:.2f} MB, over GitHub's {LIMIT_MB} MB file limit. Removed it.")

print(f"Created {zip_path.relative_to(patches_dir.parent)} from {patch.name}, {size_mb:.2f} MB")
