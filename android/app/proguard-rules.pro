# R8 configuration (release builds, see isMinifyEnabled in app/build.gradle.kts).
# Activities, services, receivers and widgets referenced from the manifest are kept automatically
# by aapt2. Add -keep rules only for classes reached by reflection (e.g. WebView JS interfaces).

-repackageclasses
-allowaccessmodification
-overloadaggressively

# Strip Kotlin null-check intrinsics (the compiler already omits most via -Xno-*-assertions).
-assumenosideeffects class kotlin.jvm.internal.Intrinsics {
    public static void check*(...);
}

# Drop verbose/debug/info logging from release builds (warnings and errors stay).
-assumenosideeffects class android.util.Log {
    public static int v(...);
    public static int d(...);
    public static int i(...);
}

# Uncomment to keep line numbers in release stack traces:
#-keepattributes SourceFile,LineNumberTable
#-renamesourcefileattribute SourceFile
