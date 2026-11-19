# Local image of the recovery service. In ACE the module ships inside the ACE service image.
FROM eclipse-temurin:21-jdk AS build
WORKDIR /src
COPY gradlew settings.gradle.kts build.gradle.kts ./
COPY gradle gradle
RUN sed -i 's/\r$//' gradlew && chmod +x gradlew && ./gradlew --no-daemon dependencies > /dev/null
COPY src src
RUN ./gradlew --no-daemon bootJar -x test

FROM eclipse-temurin:21-jre
RUN groupadd --system rwb && useradd --system --gid rwb rwb
WORKDIR /app
COPY --from=build /src/build/libs/*-SNAPSHOT.jar app.jar
USER rwb
ENV TZ=Asia/Bangkok JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=75"
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
