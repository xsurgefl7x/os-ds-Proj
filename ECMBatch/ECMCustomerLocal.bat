@ECHO off

echo.
echo Running ECM Customer
echo.

REM If ecm_prefs exist then make a backup and copy ecm prefs. Proc out to produce customer file. 

IF EXIST "C:\ECM\" (
	echo directory already there!
) ELSE (
	mkdir "C:\ECM\" 
)
set oecPath4="C:\ECM\Polling\0010000"
set oecPath3="C:\Users\sergio.salazar\Dropbox\tools\ECM\Customers"
set oecPath2="C:\Users\sergio.salazar\Dropbox\tools\ECM"
set oecPath1="C:\Users\sergio.salazar\Dropbox\tools\ECM\ECMforRpro8\ECM"
set oecPath="C:\ECM"
set string="%COMPUTERNAME%"
set /A "b=0"
set /A "a=0"
set /A "c=0"

netsh advfirewall firewall add rule name="ECM" profile=domain,private protocol=any enable=yes DIR=In program="C:\ECM\ecmexchange.exe" Action=Allow
netsh advfirewall firewall add rule name="ECM" profile=domain,private protocol=any enable=yes DIR=In program="C:\ECM\ecmproc.exe" Action=Allow

cd %oecPath1%
setup.exe /s /a /s /f1C:\Users\sergio.salazar\Dropbox\tools\ECM\ECMforRpro8\ECM\record.iss




cd %oecPath%
IF EXIST ecm_prefs.xml (
	cd  %oecPath%
	ren "ecm_prefs.xml" "ecm_prefs.xml.bak"
	ren "stations.xml" "stations.xml.bak"	
	xcopy /s/y C:\Users\sergio.salazar\Dropbox\tools\ECM\ecm_prefs.xml
	xcopy /s/y C:\Users\sergio.salazar\Dropbox\tools\ECM\stations.xml /q

) ELSE (
	xcopy /s/y C:\Users\sergio.salazar\Dropbox\tools\ECM\ecm_prefs.xml
	xcopy /s/y C:\Users\sergio.salazar\Dropbox\tools\ECM\stations.xml /q
)

IF EXIST "C:\ECM\ECM.exe" (
	START "" "C:\ECM\ECM.exe"
) ELSE (
	IF EXIST "C:\ECM\ECM.exe" (
		START "" "C:\ECM\ECM.exe"
	)
)

cd %oecPath%
ecmproc.exe -out -show -a

cd %oecPath4%
echo F|xcopy /s/y C:\ECM\Polling\0010000\OUT\Customer.xml C:\Users\sergio.salazar\Desktop\batchFiles\testing\Customers.%string%.xml /q

:loop1
set /A "a=0"
:loop
IF Exist "C:\ECM\Polling\0010000\Customer0%b%%a%.xml" set /a a+=1 && copy "C:\ECM\Polling\0010000\Customer0%b%%a%.xml" "C:\Users\sergio.salazar\Desktop\batchFiles\testing\Customers0%b%%a%.%string%.xml" && goto :loop
IF %a% GTR 10 (set /a c = %a% %% 10
) ELSE IF %a% == 0 (set /a c = %a% %% 10
) ELSE set /a c = %a% %% 10
IF %c% == 0  (set /a b+=1 && goto :loop1)

cd "C:\ECM\Polling\0010000"
set filesCount=0 & for %%f in (*) do @(set /a filesCount+=1 > nul)
cd "C:\Users\sergio.salazar\Desktop\batchFiles\testing"
set filesCounts=0 & for %%f in (*) do @(set /a filesCounts+=1 > nul)

IF %filesCount% == %filesCounts% (goto :end
) ELSE (set /a a+=1 && goto :loop)

:end

taskkill /IM ECM.exe /f

cd %oecPath1%
@Rem setup.exe /s /a /s /f1C:\Users\sergio.salazar\Dropbox\tools\ECM\ECMforRpro8\ECM\uninstall.iss

sc config "EcmExchange20000" start= disabled
sc stop "EcmExchange20000"

pause

echo.
echo ECM Customer Completed
echo.