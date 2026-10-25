# Template review — 2026-10-25

Reviewed the Android, PHP and common templates, ignore rules, instructions and reusable commands.
Preserved `PROJECT_NAME` and `APP_ID`; no target application settings were changed.

## Isolated Android checks

Created a temporary project at `%TEMP%/configs-review-5e84b4a5` from the templates,
with a minimal Kotlin framework Activity and manifest. Copied only the Gradle launcher
and wrapper JAR from picoSMS. Generated `local.properties` for the installed SDK;
no credential file or keystore was copied into the fixture or this repository.

Toolchain: JDK 17.0.20.1, Gradle 8.14.3, AGP 8.13.2, Kotlin 2.0.21, Android SDK 36.

- `printVersion testDebugUnitTest assembleDebug assembleRelease lint -Pandroid.common.unsigned=true`:
  passed with all tasks rerun. The unit-test task had no test sources; this is compilation/build
  validation, not a unit-test suite. Lint reported no errors and one newer-Gradle warning.
- Explicit unsigned release output used a versioned APK filename; `apksigner verify` rejected
  that unsigned APK as expected.
- `printVersion assembleRelease lint` using the external Windows signing configuration passed;
  `apksigner verify` accepted the signed versioned release APK. Credential values were not printed.
- Isolated version task checks cover patch/minor/major bumps, patch overflow rejection without
  editing the version file, invalid minor rejection, and `syncAndroidCommon` using an explicit
  source directory. All fixture edits stay outside application repositories.
- Seven synthetic signing-loader checks passed: Windows and Android path selection,
  missing settings, incomplete settings, missing keystore, traversal outside the keys directory,
  and explicit unsigned mode bypassing malformed settings. These evaluate the actual loader
  block with temporary directories and a stub Android DSL; they do not prove a native Android build.

The first fixture command required quoting the dotted Gradle property in PowerShell. An initial
lint error came from an unescaped drive colon in the generated fixture's `local.properties`;
after escaping it, rerunning lint tasks cleared the cached report and passed. Neither issue
required changing the template's Android source files.

## PHP, workflows and repository hygiene

- Changed the PHP CI pipeline to invoke `php -l` separately for each file with null-delimited
  paths. PHP 8.4.26 and Git Bash exercised multiple files, a filename containing spaces,
  hidden-directory exclusion, a syntax error in a later file causing failure, and empty input.
  All three pipeline scenarios passed. The workflow targets PHP 8.2; that runtime was not
  available locally, so no PHP 8.2 execution is claimed.
- Parsed both workflow YAML files with PyYAML in a temporary dependency directory and checked
  trigger/job/step structure and absence of credential secret references. This is structural
  validation; workflows were not dispatched on GitHub.
- Checked private-file ignore rules in Android and PHP templates, placeholder preservation,
  private-key file extensions and PEM private-key blocks in the reviewed text file set.
  Added `.agents/` and `.claude/` to this repository's own ignore rules.
- Reviewed Apache rewrite/access rules statically. Apache was unavailable, so live `.htaccess`
  behavior was not tested. Deployment requires Apache with `AllowOverride` permitting these
  directives and `mod_rewrite` enabled; optional compression/expiry modules control their blocks.

No device installation, native Termux Gradle build, sibling sync, version bump in a real app,
or publishing was performed. Existing application build conventions remain independent of these
templates. The similar PHP lint pipelines in other repositories need their own reviewed changes.
