# Use OpenJDK 20 as base
FROM openjdk:20-jdk

# Copy the JAR file
COPY waitSys.jar /waitSys.jar

# Make port 8080 available
EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "waitSys.jar"]
