from flask import Flask, send_file, render_template_string
import io
import os


app = Flask(__name__)
myids = [10001]

IDSETTER = os.getenv('IDSETTER', default=None)
REPEATER = os.getenv('REPEATER', default=None)
DISTR = os.getenv('DISTR', default=None)


@app.route('/', methods=['GET'])
def index():
    myids.append(myids[-1] + 1)
    myids.pop(0)
    f = io.BytesIO(myids[-1].__str__().encode('cp1251'))
    return send_file(
        f,
        attachment_filename='id.txt',
        mimetype='text/plain',
        as_attachment=True
    )


@app.route('/runner', methods=['GET'])
def get_runner():

    batch: str = f"""
    @echo off

    rem Windows has no built-in wget or curl, so generate a VBS script to do it:
    rem -------------------------------------------------------------------------
    set DLOAD_SCRIPT=%TMP%/download.vbs
    echo Option Explicit                                                    >  %DLOAD_SCRIPT%
    echo Dim args, http, fileSystem, adoStream, url, target, status         >> %DLOAD_SCRIPT%
    echo.                                                                   >> %DLOAD_SCRIPT%
    echo Set args = Wscript.Arguments                                       >> %DLOAD_SCRIPT%
    echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1")              >> %DLOAD_SCRIPT%
    echo url = args(0)                                                      >> %DLOAD_SCRIPT%
    echo target = args(1)                                                   >> %DLOAD_SCRIPT%
    echo.                                                                   >> %DLOAD_SCRIPT%
    echo http.Open "GET", url, False                                        >> %DLOAD_SCRIPT%
    echo http.Send                                                          >> %DLOAD_SCRIPT%
    echo status = http.Status                                               >> %DLOAD_SCRIPT%
    echo.                                                                   >> %DLOAD_SCRIPT%
    echo If status ^<^> 200 Then                                            >> %DLOAD_SCRIPT%
    echo    WScript.Echo "FAILED to download: HTTP Status " ^& status       >> %DLOAD_SCRIPT%
    echo    WScript.Quit 1                                                  >> %DLOAD_SCRIPT%
    echo End If                                                             >> %DLOAD_SCRIPT%
    echo.                                                                   >> %DLOAD_SCRIPT%
    echo Set adoStream = CreateObject("ADODB.Stream")                       >> %DLOAD_SCRIPT%
    echo adoStream.Open                                                     >> %DLOAD_SCRIPT%
    echo adoStream.Type = 1                                                 >> %DLOAD_SCRIPT%
    echo adoStream.Write http.ResponseBody                                  >> %DLOAD_SCRIPT%
    echo adoStream.Position = 0                                             >> %DLOAD_SCRIPT%
    echo.                                                                   >> %DLOAD_SCRIPT%
    echo Set fileSystem = CreateObject("Scripting.FileSystemObject")        >> %DLOAD_SCRIPT%
    echo If fileSystem.FileExists(target) Then fileSystem.DeleteFile target >> %DLOAD_SCRIPT%
    echo adoStream.SaveToFile target                                        >> %DLOAD_SCRIPT%
    echo adoStream.Close                                                    >> %DLOAD_SCRIPT%
    echo.                                                                   >> %DLOAD_SCRIPT%
    rem -------------------------------------------------------------------------

    for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
    IF "%version%" == "5.1" set VNCURL={DISTR}/xp/winvnc.exe
    IF "%version%" == "5.2" set VNCURL={DISTR}/xp/winvnc.exe
    IF NOT "%version%" == "5.1" IF NOT "%version%" == "5.2" set VNCURL={DISTR}/win8/winvnc.exe

    cscript //Nologo %DLOAD_SCRIPT% %vncurl% %TMP%/winvnc.exe
    cscript //Nologo %DLOAD_SCRIPT% {IDSETTER} %TMP%/id.txt
    netsh advfirewall firewall add rule name="VNC Server" dir=in action=allow protocol=TCP localport=5900-5910

    (
    set /p yourid=
    )<%TMP%/id.txt

    echo [Permissions] > %TMP%/UltraVNC.ini
	echo [admin] >> %TMP%/UltraVNC.ini
	echo FileTransferEnabled=1 >> %TMP%/UltraVNC.ini
	echo FTUserImpersonation=1 >> %TMP%/UltraVNC.ini
	echo BlankMonitorEnabled=1 >> %TMP%/UltraVNC.ini
	echo BlankInputsOnly=0 >> %TMP%/UltraVNC.ini
	echo DefaultScale=1 >> %TMP%/UltraVNC.ini
	echo UseDSMPlugin=0 >> %TMP%/UltraVNC.ini
	echo DSMPlugin= >> %TMP%/UltraVNC.ini
	echo primary=1 >> %TMP%/UltraVNC.ini
	echo secondary=0 >> %TMP%/UltraVNC.ini
	echo SocketConnect=1 >> %TMP%/UltraVNC.ini
	echo HTTPConnect=1 >> %TMP%/UltraVNC.ini
	echo AutoPortSelect=1 >> %TMP%/UltraVNC.ini
	echo InputsEnabled=1 >> %TMP%/UltraVNC.ini
	echo LocalInputsDisabled=0 >> %TMP%/UltraVNC.ini
	echo IdleTimeout=0 >> %TMP%/UltraVNC.ini
	echo EnableJapInput=0 >> %TMP%/UltraVNC.ini
	echo QuerySetting=2 >> %TMP%/UltraVNC.ini
	echo QueryTimeout=10 >> %TMP%/UltraVNC.ini
	echo QueryAccept=0 >> %TMP%/UltraVNC.ini
	echo LockSetting=0 >> %TMP%/UltraVNC.ini
	echo RemoveWallpaper=0 >> %TMP%/UltraVNC.ini
	echo RemoveEffects=0 >> %TMP%/UltraVNC.ini
	echo RemoveFontSmoothing=0 >> %TMP%/UltraVNC.ini
	echo RemoveAero=0 >> %TMP%/UltraVNC.ini
	echo DebugMode=0 >> %TMP%/UltraVNC.ini
	echo Avilog=0 >> %TMP%/UltraVNC.ini
	echo path=%TMP% >> %TMP%/UltraVNC.ini
	echo DebugLevel=0 >> %TMP%/UltraVNC.ini
	echo AllowLoopback=1 >> %TMP%/UltraVNC.ini
	echo LoopbackOnly=0 >> %TMP%/UltraVNC.ini
	echo AllowShutdown=1 >> %TMP%/UltraVNC.ini
	echo AllowProperties=1 >> %TMP%/UltraVNC.ini
	echo AllowEditClients=1 >> %TMP%/UltraVNC.ini
	echo FileTransferTimeout=30 >> %TMP%/UltraVNC.ini
	echo KeepAliveInterval=5 >> %TMP%/UltraVNC.ini
	echo IdleInputTimeout=0 >> %TMP%/UltraVNC.ini
	echo DisableTrayIcon=0 >> %TMP%/UltraVNC.ini
	echo rdpmode=0 >> %TMP%/UltraVNC.ini
	echo MSLogonRequired=0 >> %TMP%/UltraVNC.ini
	echo NewMSLogon=0 >> %TMP%/UltraVNC.ini
	echo ConnectPriority=0 >> %TMP%/UltraVNC.ini
	echo [UltraVNC] >> %TMP%/UltraVNC.ini
	echo passwd=494015F9A35E8B2245 >> %TMP%/UltraVNC.ini
	echo passwd2=494015F9A35E8B2245 >> %TMP%/UltraVNC.ini
	echo [poll] >> %TMP%/UltraVNC.ini
	echo TurboMode=1 >> %TMP%/UltraVNC.ini
	echo PollUnderCursor=0 >> %TMP%/UltraVNC.ini
	echo PollForeground=0 >> %TMP%/UltraVNC.ini
	echo PollFullScreen=1 >> %TMP%/UltraVNC.ini
	echo OnlyPollConsole=0 >> %TMP%/UltraVNC.ini
	echo OnlyPollOnEvent=0 >> %TMP%/UltraVNC.ini
	echo MaxCpu=40 >> %TMP%/UltraVNC.ini
	echo EnableDriver=0 >> %TMP%/UltraVNC.ini
	echo EnableHook=1 >> %TMP%/UltraVNC.ini
	echo EnableVirtual=0 >> %TMP%/UltraVNC.ini
	echo SingleWindow=0 >> %TMP%/UltraVNC.ini
	echo SingleWindowName= >> %TMP%/UltraVNC.ini

    msg "%username%" ID:%yourid%
    %TMP%/winvnc.exe -autoreconnect ID:%yourid% -connect {REPEATER} -run

    endlocal
    """
    f = io.BytesIO(batch.encode('cp1251'))
    return send_file(
        f,
        attachment_filename='runner.bat',
        mimetype='application/bat',
        as_attachment=True
    )


@app.route('/helper', methods=['GET'])
def helper():
    return render_template_string("""
        # TODO: Make helper page
    """)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
