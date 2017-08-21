from flask import Flask, send_file, render_template_string
import io
import os


app = Flask(__name__)
myids = [10001]

IDSETTER = os.getenv('IDSETTER' default=None)
REPEATER = os.getenv('REPEATER' default=None)
DISTR = os.getenv('DISTR' default=None)


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

    set IDSETTER={IDSETTER}
    set REPEATER={REPEATER}

    cscript //Nologo %DLOAD_SCRIPT% %vncurl% %TMP%/winvnc.exe
    cscript //Nologo %DLOAD_SCRIPT% %idsetter% id.txt
    netsh advfirewall firewall add rule name="VNC Server" dir=in action=allow protocol=TCP localport=5900-5910

    (
    set /p yourid=
    )<id.txt

    msg "%username%" ID:%yourid%
    %TMP%/winvnc.exe -autoreconnect ID:%yourid% -connect %repeater% -run

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

