# Maintaining universal configs

- These are templates, not applications. Inspect the target project's existing conventions before copying.
- Keep edits within this repository unless the user explicitly requests changes to another project.
- Never add tokens, passwords, private keys, keystores, login state, personal account configuration,
  or machine-specific credential values. Do not print credential values while inspecting source repos.
- Load configured Android signing only from /sdcard/keys/keystore.properties on Android or
  W:/Desktop/keys/keystore.properties on Windows. Keep credential values outside this repository.
  Missing configuration leaves releases unsigned; CI has no credential inputs.
- Preserve PROJECT_NAME and APP_ID placeholders; do not embed a real application's identity.
- The included android/gradle/android-common.gradle adapts android-common versioning and uses
  external platform keys. Do not replace it with upstream project-local or global credential lookup.
- Do not run the upstream sync.cmd: it writes to multiple sibling projects.
- Preserve deliberate SDK, plugin, JVM, Compose and module-layout differences in existing projects.
- Validate meaningful behavior in an isolated temporary project. Never copy local.properties or
  credential files from source repos. Use a locally configured Android SDK and JDK 17 for this template.
- Review git status and file contents before committing. Do not push unless instructed.
- See commands/ for reusable inspection, application and verification prompts.
