# configs

Universal config files for the projects in `W:\Desktop\GIT`. They are taken from the repos themselves
(the most common and newest working variant of each file), cleaned up and made project-neutral.
Copy what you need into a project. Nothing here is linked or synced automatically.

The Android template includes `gradle/android-common.gradle`, adapted from
[`android-common`](../android-common). It retains version parsing, version bump tasks, APK names,
and an explicit sync task. Signing settings are loaded from the external platform keys folder;
without those settings release APKs are unsigned. The original android-common folder and existing projects are unchanged.

## Layout

| Folder | File | Goes to | Notes |
|---|---|---|---|
| `common/` | `.gitattributes` | project root | LF everywhere, CRLF for `*.bat`/`*.cmd`, binaries marked |
| | `.editorconfig` | project root | UTF-8, LF, 4 spaces (2 for YAML/JSON/TOML), Kotlin official style |
| `android/` | `.gitignore` | project root | Gradle/IDE/build output, keystores, APKs, agent tool folders |
| | `gradle.properties` | project root | 2 GB heap, parallel + build cache, `nonTransitiveRClass` |
| | `gradle/wrapper/gradle-wrapper.properties` | same path | Gradle 8.14.3 |
| | `settings.gradle.kts` | project root | replace `PROJECT_NAME` |
| | `build.gradle.kts` | project root | AGP 8.13.2 + Kotlin 2.0.21 (`apply false`) |
| | `gradle/android-common.gradle` | same path | versioning + external platform signing settings |
| | `version.properties` | project root | `major`/`minor`/`patch`, read by android-common |
| | `app/build.gradle.kts` | `app/` | replace `APP_ID`; SDK 24 → 36, Java/Kotlin 17, R8 + resource shrinking |
| | `app/proguard-rules.pro` | `app/` | aggressive R8, strips Kotlin null checks and `Log.v/d/i` |
| | `.github/workflows/build.yml` | same path | tests, debug + release APK, GitHub release with unsigned CI APK on `v*` tags |
| `php/` | `.gitignore` | project root | runtime data/cache, `.env`, `vendor/`, agent tool folders |
| | `.htaccess` | web root | front controller to `index.php`, hides dotfiles and `.sql/.log/.bak/.ini`, gzip + caching |
| | `.github/workflows/build.yml` | same path | `php -l` on every `.php` file (PHP 8.2) |

## New Android project

1. Copy `common/*` and `android/*` (including the dot files and `.github`) into the new folder.
2. Copy `gradlew`, `gradlew.bat` and `gradle/wrapper/gradle-wrapper.jar` from any project (or run `gradle wrapper`).
3. Keep the included `gradle/android-common.gradle`; no sibling folder is needed to build.
4. Replace `PROJECT_NAME` in `settings.gradle.kts` and `APP_ID` in `app/build.gradle.kts`.
5. If the app uses AndroidX libraries, set `android.useAndroidX=true` in `gradle.properties`.
6. If you use Compose, add the `org.jetbrains.kotlin.plugin.compose` plugin (same version as Kotlin) and
   `buildFeatures { compose = true }`. smallGestures is the only Compose project so far and uses a version catalog.

Gradle needs JDK 17+. On this PC, `JAVA_HOME` is not set and PATH has a 32-bit Java 8, so use for example
`set JAVA_HOME=%USERPROFILE%\.jdks\ms-17.0.20.1`, or Android Studio's Gradle JDK setting.

Validation 2026-10-25: the templates were reviewed and exercised in an isolated Android project.
See [VALIDATION.md](VALIDATION.md) for checks, results and runtime limits.

## Existing projects: what differs from the template

Look before overwriting: some differences are deliberate.

| Project | Differences |
|---|---|
| Darker | AGP 9.0.0-alpha06, Gradle 9.0.0, Java 11, minSdk 26; extra `debug-apk.yml` workflow |
| GPS Tools | AGP 8.13.2 without Kotlin plugin version in root, Gradle 9.3.0, no android-common |
| HolePunching | Groovy build (`build.gradle`), own `.gitignore` (server data), not a git repo |
| LocalBridge | multi-module (`android`, `core`), version catalog, AGP 8.11.1 / Kotlin 2.1.21 |
| Qalc, Sheaf-launcher, VKeyboard | match the template versions; compileSdk/targetSdk 35 |
| Send Anyway | AGP 8.9.1 / Kotlin 2.1.20, SDK 35; extra `debug-apk.yml` |
| UniFX, picoNotes, picoSensors | AGP 8.7.3, Gradle 8.11.1/8.9, SDK 35 |
| Warehousy | version catalog, Gradle 9.0.0, Java 11, minify off |
| picoCalendar | AGP 8.11.1 / Kotlin 2.1.21, no android-common |
| picoSMS, picoStrips | newer Kotlin (2.2.20 / 2.3.20); otherwise the template is based on picoSMS |
| smallGestures | Compose + version catalog, AGP 8.7.3 |
| php-cache-proxy | minimal `.htaccess` (rewrite everything); `.gitignore` for `cookies.txt`, `lastsite.txt`, `data/*` |
| simplemd4php | `.htaccess` also blocks raw `.md` files (keep that rule there) |

All Android repos use the same `.gitignore` as the template, but without `.autoagents/` (used by Send Anyway,
Sheaf-launcher and picoCalendar) and `.gradle-home/`. Projects without `.gitattributes`: Darker, Sheaf-launcher,
VKeyboard, php-cache-proxy, HolePunching.

## android-common integration

`android-common` contains shared configuration, rather than an application. Its `.gitignore`
conventions are covered by `android/.gitignore`. Its Gradle versioning logic is included in the
template; signing lookup uses the platform keys directory instead of project-local/global properties.
The broad sibling-project `sync.cmd` is deliberately omitted.

Run `gradlew printVersion`, `gradlew bumpPatch`, `gradlew bumpMinor`, or `gradlew bumpMajor` in a
project that uses the template. Bump tasks edit `version.properties`; run the build afterwards in a
new Gradle invocation. `gradlew syncAndroidCommon` explicitly updates only that project's script
from the sibling `configs/android/gradle` folder. For another location, pass
`-Pconfigs.android.dir=<path-to-configs/android/gradle>`. Review local customizations before syncing.
Do not use the original android-common `sync.cmd` to update the configs copy: it would restore
the original signing lookup instead of the required platform keys lookup.

## Credentials and release output

Keep this repository free of authentication tokens, private keys, passwords, keystores, login state,
and machine-specific credentials. The ignore files provide an extra guard, but do not sanitize files
already tracked or deliberately force-added. Review file contents before committing.
The CI template contains no credential inputs or secret references. GitHub Actions uses its automatic
job identity to upload artifacts and create tag releases; no personal token is configured here.

Debug builds use the Android tooling's normal local debug signing. Release signing is loaded
only from `keystore.properties` in the platform folder:

| Platform | External credential file |
|---|---|
| Windows | `W:\Desktop\keys\keystore.properties` |
| Android / Termux | `/sdcard/keys/keystore.properties` |

The external file contains Java-properties entries `storeFile`, `storePassword`, `keyAlias`, and
`keyPassword`. Use the keystore filename as `storeFile`, relative to the keys folder, so the same
configuration works on both platforms. The referenced keystore must exist inside that folder.
Password values are loaded as written, without trimming or quote removal; use Java-properties
escaping for backslashes or leading spaces. Save the file as UTF-8 without a BOM.
Never place this file or the keystore in `configs`. This repository contains only the loader.

Missing external configuration produces an unsigned release. Incomplete configuration or a missing
or out-of-folder keystore fails with a message that does not display credential values. To build
unsigned explicitly, use `-Pandroid.common.unsigned=true`, which skips credential loading entirely.
In PowerShell, quote this dotted property: `.\gradlew.bat '-Pandroid.common.unsigned=true' assembleRelease`.
The template never falls back to a debug key for release builds. The default CI runner has neither
platform keys folder, so its release artifact is unsigned and needs signing before distribution.

## Markdown instructions for agents

`AGENTS.md` describes how to maintain this repository. `commands/inspect-configs.md`,
`commands/apply-configs.md`, and `commands/verify-configs.md` are reusable prompts: give one to
an agent and specify the target project path. They require inspection, focused edits and checks.
For tools that support Markdown commands, copy the selected files into that tool's command
folder in the target project (for example `.claude/commands/`). These prompts need no auth setup.
