# Apply universal configuration to a project

Target: use the project path supplied by the user; require a clear target before writing.

1. Read project instructions and inspect git status. Preserve unrelated edits.
2. Compare existing configuration with the applicable common/, android/ and php/ templates.
3. Apply only files appropriate to the target. Include hidden files when copying; merge ignore rules.
   Preserve app identity, SDK/JVM/plugin choices, module layout, dependencies and Compose settings
   unless the task explicitly requests changing them. Set placeholders for a new project.
4. For a new Android project, include gradle/android-common.gradle and version.properties.
   Keep existing production signing in established apps unless the user requested replacing it;
   use /sdcard/keys/keystore.properties on Android or W:/Desktop/keys/keystore.properties on Windows.
   Absent external configuration produces unsigned releases; do not embed credentials in projects.
5. Never copy tokens, passwords, private keys, keystores, account state or machine-specific
   credential configuration. Do not execute broad sibling-project sync scripts.
6. Run the applicable checks from verify-configs.md. Review the diff and report changed files,
   results and any checks that could not run. Do not publish, push or release as part of this command.
