@echo on
cd %~dp0/src/neqsim/lib
call java -classpath NeqSimpy4j.jar;NeqSimS.jar;py4j0.10.8.1.jar neqsimpy4j.startJavaGateway
pause
