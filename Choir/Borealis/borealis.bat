C:
C:\Users\Public\Borealis
taskkill /f /im pythonw.exe
start "" cmd /c "pythonw borealis.pyw" && timeout /t 2 && taskkill /F /IM cmd.exe
