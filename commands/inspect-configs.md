# Inspect a project's configuration

Target: use the project path supplied by the user. If absent, use the current project.

1. Read its AGENTS.md instructions and git status before making changes.
2. Identify modules, languages, Gradle wrapper/plugins, SDK and JVM levels, PHP entry points,
   workflows, ignore rules, versioning, and existing configuration conventions.
3. Compare applicable files with common/, android/ and php/ in the configs repository.
   Inspect android-common as shared configuration when available, not as an app.
4. Avoid reading credential files. If a potential secret appears, report only its path and category;
   never reproduce the value or copy it into configs.
5. Report reusable settings, intentional project differences, and proposed file changes.
   This command is read-only; do not change projects or run sync scripts.
