# Verify configuration changes

Target: use the project path supplied by the user. Keep existing work intact.

1. Read the project's instructions, inspect the diff, and check for unresolved placeholders.
2. Check new text for credential values without printing matches. Confirm no credential files
   were added; ignore rules alone do not protect tracked files.
3. Android: use a compatible JDK (17 for this template) and locally installed Android SDK.
   Run gradlew printVersion testDebugUnitTest assembleDebug assembleRelease lint
   (./gradlew on POSIX, .\gradlew.bat on Windows). Do not run bump tasks in the real project
   merely to test them; exercise version bumps only in an isolated temporary copy.
4. Verify versionName/versionCode and the versioned APK filename. With configured external keys,
   verify the release signature without printing credential values. With missing configuration or
   -Pandroid.common.unsigned=true, verify unsigned output. Do not install or publish during checks.
5. PHP: run php -l on each PHP source file. If .htaccess changed, validate rewrite and access
   behavior with Apache when available; php -l does not validate Apache configuration.
6. Confirm workflows reference existing tasks and artifact paths. Use available YAML/CI validators.
7. Report actual results and missing tools explicitly. Avoid claiming a check passed if it did not run.
