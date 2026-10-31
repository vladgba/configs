"""Copy the pUI kit into an Android app module (overwrites the kit's own p_* files only).

usage: python -I apply.py <project-dir> [module]      module defaults to "app"

- res/**            -> <module>/src/main/res/**              (all files are p_* prefixed)
- kotlin/*.kt       -> <module>/src/main/<java|kotlin>/<namespace path>/pui/*.kt  (Kotlin modules only)
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

    # Kotlin modules get the Kotlin helpers; detect by sources (AGP 9 builds Kotlin without naming a plugin).
    pui_parts = (*ns.split("."), "pui")
    if not any(p for p in main_dir.rglob("*.kt") if "pui" not in p.parts):
        print(f"pUI -> {module.relative_to(project.parent)}: {copied} resource files (Java-only: no Kotlin helpers)")
        return

    src_root = main_dir / ("kotlin" if (main_dir / "kotlin").is_dir() else "java")
    pui_dir = src_root.joinpath(*pui_parts)
    pui_dir.mkdir(parents=True, exist_ok=True)
    names = []
    for kt in sorted((KIT / "kotlin").glob("*.kt")):
        (pui_dir / kt.name).write_text(kt.read_text(encoding="utf-8").replace("__PKG__", ns),
                                       encoding="utf-8", newline="\n")
        names.append(kt.name)
    print(f"pUI -> {module.relative_to(project.parent)}: {copied} resource files, "
          f"{pui_dir.relative_to(project)}/{{{', '.join(names)}}} ({ns})")


if __name__ == "__main__":
    main()
