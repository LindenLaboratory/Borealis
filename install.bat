@echo off
set "sourceFolder=Borealis"
set "destinationFolder=C:\Users\Public\Borealis"
xcopy "%sourceFolder%" "%destinationFolder%\" /E /I /Y
C:
cd C:\Users\Public\Borealis
start "" cmd /c "python borealis.pyw"