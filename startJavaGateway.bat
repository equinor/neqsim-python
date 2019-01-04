@echo on
cd %~dp0/java/bin
call java -classpath NeqSimpy4j.jar;NeqSimSource.jar;py4j0.10.8.1.jar neqsimpy4j.startJavaGateway
pause
