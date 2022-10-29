@echo on

echo.
echo Running Lines.
echo.
set /A "b=0"
set /A "a=0"
set /A "c=0"
set string=%COMPUTERNAME%

@Rem for  /R %%x in (Customers*.xml) do (
@Rem	set /A counter+=1
@Rem	copy "%%x" "C:\Users\sergio.salazar\Dropbox\tools\ECM\testing\Customers00%counter%.%string%.xml")

:loop1
set /A "a=0"
:loop
IF Exist "C:\ECM\Polling\0010000\Customer0%b%%a%.xml" set /a a+=1 && copy "C:\ECM\Polling\0010000\Customer0%b%%a%.xml" "C:\Users\sergio.salazar\Desktop\batchFiles\testing\Customers0%b%%a%.%string%.xml"&&  goto :loop
IF %a% == 0 (goto :loop2)
set /a c = %a% %% 10
IF %c% == 0  (set /a b+=1 && goto :loop1)

:loop2
cd "C:\ECM\Polling\0010000"
set filesCount=0 & for %%f in (*) do @(set /a filesCount+=1 > nul)
cd "C:\Users\sergio.salazar\Desktop\batchFiles\testing"
set filesCounts=0 & for %%f in (*) do @(set /a filesCounts+=1 > nul)

IF %filesCount% == %filesCounts% (goto :end
) ELSE (set /a a+=1 && goto :loop)

:end
pause

echo.
echo Completed.
echo.
