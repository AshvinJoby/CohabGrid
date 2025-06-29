@echo off
SET RETRIES=30

:waitForPod
SET FOUND=

FOR /F "tokens=* USEBACKQ" %%i IN (`kubectl get pods -l app=cohabgrid --no-headers`) DO (
    SET FOUND=1
)

IF NOT DEFINED FOUND (
    echo 🔁 Pod not yet created. Retrying...
    ping 127.0.0.1 -n 4 >nul
    SET /A RETRIES-=1
    IF %RETRIES% GTR 0 GOTO waitForPod
    echo ❌ Timed out waiting for pod to appear.
    exit /b 1
)

FOR /F "delims=" %%i IN (`kubectl get pods -l app=cohabgrid --sort-by=.metadata.creationTimestamp -o jsonpath={.items[-1].metadata.name}`) DO (
    echo 🔍 Waiting on pod: %%i
    kubectl wait --for=condition=ready pod %%i --timeout=90s
    IF ERRORLEVEL 1 (
        echo ❌ Pod did not become ready in time.
        exit /b 1
    )
)
