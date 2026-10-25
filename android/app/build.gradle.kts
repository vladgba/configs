import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

// Shared versioning adapted from android-common, included in this template.
// Sets versionCode/versionName and reads signing settings from the external platform keys folder.
// Keep production signing configuration outside this template repository.
apply(from = rootProject.file("gradle/android-common.gradle"))

android {
    namespace = "x.vladgba.APP_ID"
    compileSdk = 36

    defaultConfig {
        applicationId = "x.vladgba.APP_ID"
        minSdk = 24
        targetSdk = 36
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            vcsInfo.include = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        buildConfig = false
        resValues = false
        shaders = false
    }

    // Keep only these translations from libraries (remove to ship every locale).
    androidResources {
        localeFilters += listOf("en")
    }

    packaging {
        resources.excludes += listOf(
            "kotlin/**", "kotlin-tooling-metadata.json", "META-INF/*.version", "META-INF/version-control-info.textproto", "META-INF/*.kotlin_module",
            "**/*.kotlin_builtins", "DebugProbesKt.bin", "META-INF/com/android/build/gradle/**"
        )
    }

    // No Google-encrypted dependency blob in the APK/AAB (F-Droid / reproducible builds).
    dependenciesInfo {
        includeInApk = false
        includeInBundle = false
    }

    lint {
        abortOnError = true
    }
}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_17)
        freeCompilerArgs.addAll(
            "-Xno-param-assertions",
            "-Xno-call-assertions",
            "-Xno-receiver-assertions"
        )
    }
}

dependencies {
    testImplementation("junit:junit:4.13.2")
}
