import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    // Apply the Kotlin JVM plugin to add support for Kotlin.
    id("org.jetbrains.kotlin.jvm") version "1.4.20"

    // Apply the java-library plugin for API and implementation separation.
    `java-library`
}

repositories {
    // Use jcenter for resolving dependencies.
    // You can declare any Maven/Ivy/file repository here.
    jcenter()
}

dependencies {
    // Align versions of all Kotlin components
    implementation(platform("org.jetbrains.kotlin:kotlin-bom"))

    // Use the Kotlin JDK 8 standard library.
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")

    implementation("net.java.dev.jna:jna:5.5.0")

    // Use the Kotlin test library.
    testImplementation("org.jetbrains.kotlin:kotlin-test")

    // Use the Kotlin JUnit5 integration.
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
    testImplementation("org.junit.jupiter:junit-jupiter-api:5.4.0")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.4.0")

    // Use the Kotlin JUnit integration.
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit")
}

tasks {

    withType<KotlinCompile> {
        kotlinOptions.jvmTarget = "11"
    }

    named<Test>("test") {
        useJUnitPlatform()
        dependsOn("cleanTest")
        testLogging.events("failed")

        // parallel tests disabled
        systemProperty("junit.jupiter.execution.parallel.enabled", "false")
        systemProperty("junit.jupiter.execution.parallel.mode.default", "same_thread")
        maxParallelForks = 1
	exec {
		commandLine("python", "copynativelib.py")
	}
    }
}
