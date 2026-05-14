#!/bin/bash
mvn clean compile dependency:copy-dependencies -DincludeScope=compile -DskipTests
echo "✓ Compilation done"
