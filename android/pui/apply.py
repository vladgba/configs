"""Copy the pUI kit into an Android app module (overwrites the kit's own p_* files only).

usage: python -I apply.py <project-dir> [module]      module defaults to "app"

- res/**            -> <module>/src/main/res/**              (all files are p_* prefixed)
- kotlin/PUi.kt     -> <module>/src/main/<java|kotlin>/<namespace path>/pui/PUi.kt
                       with __PKG__ replaced by the module's `namespace`
Re-run after changing the kit; app-owned files are never touched.
"""
import pathlib
import re
import shutil
import sys

KIT = pathlib.Path(__file__).resolve().parent


def namespace(module: pathlib.Path) -> str:
    for name in ("build.gradle.kts", "build.gradle"):
        f = module / name
        if f.exists():
            m = re.search(r"""namespace\s*=?\s*["']([\w.]+)["']""", f.read_text(encoding="utf-8"))
            if m:
                return m.group(1)
    sys.exit(f"no namespace found in {module}")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    project = pathlib.Path(sys.argv[1]).resolve()
    module = project / (sys.argv[2] if len(sys.argv) > 2 else "app")
    ns = namespace(module)
    main_dir = module / "src" / "main"

    copied = 0
    for src in (KIT / "res").rglob("*"):
        if src.is_file():
            dst = main_dir / "res" / src.relative_to(KIT / "res")
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            copied += 1

    build_files = [module / n for n in ("build.gradle.kts", "build.gradle") if (module / n).exists()]
    if not any("kotlin" in f.read_text(encoding="utf-8") for f in build_files):
        print(f"pUI -> {module.relative_to(project.parent)}: {copied} resource files (Java-only: no PUi.kt)")
        return

    src_root = main_dir / ("kotlin" if (main_dir / "kotlin").is_dir() else "java")
    kt_dst = src_root.joinpath(*ns.split("."), "pui", "PUi.kt")
    kt_dst.parent.mkdir(parents=True, exist_ok=True)
    kt_dst.write_text((KIT / "kotlin" / "PUi.kt").read_text(encoding="utf-8").replace("__PKG__", ns),
                      encoding="utf-8", newline="\n")
    print(f"pUI -> {module.relative_to(project.parent)}: {copied} resource files, {kt_dst.relative_to(project)} ({ns})")


if __name__ == "__main__":
    main()
