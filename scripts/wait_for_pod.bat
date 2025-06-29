@echo off
SET RETRIES=30

:waitForPod
kubectl get pods -l app=cohabgrid --no-headers > podlist.txt 2>nul
findstr /R "." podlist.txt >nul
IF %ERRORLEVEL% NEQ 0 (
    echo 🔁 Pod not yet created. Retrying...
    ping 127.0.0.1 -n 4 >nul
    SET /A RETRIES-=1
    IF %RETRIES% GTR 0 GOTO waitForPod
    echo ❌ Timed out waiting for pod to appear.
    exit /b 1
)
del podlist.txt

:: Use PowerShell to preserve proper quoting!
for /f "usebackq delims=" %%i in (`powershell -Command "kubectl get pods -l app=cohabgrid --sort-by=.metadata.creationTimestamp -o 'jsonpath={.items[-1].metadata.name}'"`) do (
    echo 🔍 Waiting on pod: %%i
    kubectl wait --for=condition=ready pod %%i --timeout=90s
    IF ERRORLEVEL 1 (
        echo ❌ Pod did not become ready in time.
        exit /b 1
    )
)
