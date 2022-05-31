@ECHO OFF

DEL /Q /S .temp\* > nul 2>&1 || goto error
sphinx-build -M html docsrc .temp || goto error
xcopy .temp\html docs /F /S /Y > nul 2>&1|| goto error
coverage html || goto error

goto eof

:error
echo something went wrong :(