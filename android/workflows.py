"""Write the standard CI workflow (.github/workflows/build.yml) into every p* Android repo.

usage: python -I configs/android/workflows.py [--dry]

The template is configs/android/.github/workflows/build.yml. Per project it fills in the app name,
the Gradle module, the unit-test tasks and the release task. Older overlapping workflows
(android.yml, debug-apk.yml) are removed: build.yml covers tests and the release APK artifact.
Folder names: the new p* name is used when present, else the old one.
"""
import pathlib
import sys

GIT = pathlib.Path(__file__).resolve().parents[2]
TEMPLATE = GIT / "configs" / "android" / ".github" / "workflows" / "build.yml"
OBSOLETE = ("android.yml", "debug-apk.yml")

# app name, new folder, old folder, module, test tasks, release task
PROJECTS = [
    ("pCalc", "pCalc", "Qalc", "app", "", "assembleRelease"),
    ("pCalendar", "pCalendar", "picoCalendar", "app", "", "assembleRelease"),
    ("pDimmer", "pDimmer", "Darker", "app", "", "assembleRelease"),
    ("pFiles", "pFiles", "UniFX", "app", "testDebugUnitTest", "assembleRelease"),
    ("pGPS", "pGPS", "GPS Tools", "app", "", "assembleRelease"),
    ("pGestures", "pGestures", "smallGestures", "app", "testDebugUnitTest", "assembleRelease"),
    # "*": the keyboard (app) and its voice add-on (voice) are both uploaded
    ("pKeyboard", "pKeyboard", "VKeyboard", "*", "testDebugUnitTest", "assembleRelease"),
    ("pLauncher", "pLauncher", "Sheaf-launcher", "app", "", "assembleRelease"),
    ("pSMS", "pSMS", "picoSMS", "app", "testDebugUnitTest", "assembleRelease"),
    ("pScanner", "pScanner", "picoStrips", "app", "", "assembleRelease"),
    ("pShare", "pShare", "Send Anyway", "app", "testDebugUnitTest", "assembleRelease"),
    ("pSync", "pSync", "pBridge", "android", ":core:runTests", ":android:assembleRelease"),
    ("pUtils", "pUtils", "picoSensors", "app", "", "assembleRelease"),
    # internal (non-public) but still gets CI on its private repo
    ("pInventory", "pInventory", "Warehousy", "app", "", "assembleRelease"),
]


def main() -> None:
    dry = "--dry" in sys.argv
    template = TEMPLATE.read_text(encoding="utf-8")
    for app, new, old, module, tests, release in PROJECTS:
        root = GIT / new if (GIT / new / "gradlew").exists() else GIT / old
        if not (root / "gradlew").exists():
            print(f"skip {app}: project folder not found")
            continue
        wf_dir = root / ".github" / "workflows"
        text = (template.replace("__APP_NAME__", app).replace("__MODULE__", module)
                .replace("__TEST_TASKS__", tests).replace("__RELEASE_TASK__", release))
        removed = [n for n in OBSOLETE if (wf_dir / n).exists()]
        print(f"{app:11} -> {root.name}/.github/workflows/build.yml"
              + (f" (removes {', '.join(removed)})" if removed else ""))
        if dry:
            continue
        wf_dir.mkdir(parents=True, exist_ok=True)
        (wf_dir / "build.yml").write_text(text, encoding="utf-8", newline="\n")
        for n in removed:
            (wf_dir / n).unlink()


if __name__ == "__main__":
    main()
