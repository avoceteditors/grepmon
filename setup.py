from distutils.core import setup
import re
import pathlib
import subprocess
import sys

# Configure Packages
packages = [
    "grepmon"
]

package_dirs = {}
exts = []
for package in packages:
    src = re.sub("\.", "/", package)
    package_dirs[package] = src

    # Find Cython Extensions
    path = pathlib.Path(src)
    for i in path.rglob("*.pyx"):
        exts.append(str(i))

    for i in path.rglob("*.pxd"):
        exts.append(str(i))

# Configure Scripts
scripts_path = pathlib.Path("scripts")
scripts = []
for i in scripts_path.glob('*'):
    if i.is_file():
        scripts.append(str(i))

for gramm in pathlib.Path("dion").rglob("*.g4"):
    gramm = gramm.resolve()
    print(f"Updating Grammar: {str(gramm)}")
    try:
        subprocess.run(["antlr4", "-Dlanguage=Python3", "-visitor", str(gramm)], cwd=str(gramm.parent),check=True)
    except:
        sys.exit(1)

setup(
    name="grepmon",
    version="2021.1",
    scripts=scripts,
    package_dir=package_dirs,
    packages=packages
)


