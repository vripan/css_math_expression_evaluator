@ECHO OFF

sphinx-build -M html docsrc .temp || goto error
xcopy .temp\html docs /F /S /Y || goto error
coverage html || goto error

exit 0

:error
echo "something went wrong :("
exit 1