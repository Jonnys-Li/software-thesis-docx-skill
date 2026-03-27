param(
    [string]$Ref = "main",
    [string]$Dest,
    [string]$Name = "software-thesis-docx",
    [switch]$Force
)

$Owner = "Jonnys-Li"
$Repo = "software-thesis-docx-skill"

function Get-PythonLauncher {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @{ Command = "py"; Prefix = @("-3") }
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @{ Command = "python"; Prefix = @() }
    }
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        return @{ Command = "python3"; Prefix = @() }
    }
    throw "Python 3 is required to install this skill."
}

$InstallPy = Join-Path $PSScriptRoot "install.py"
$TempFile = $null

try {
    if (-not (Test-Path $InstallPy)) {
        $TempFile = Join-Path ([System.IO.Path]::GetTempPath()) ("software-thesis-docx-install-" + [System.Guid]::NewGuid().ToString() + ".py")
        $RawUrl = "https://raw.githubusercontent.com/$Owner/$Repo/$Ref/install.py"
        Invoke-WebRequest -Uri $RawUrl -OutFile $TempFile
        $InstallPy = $TempFile
    }

    $Launcher = Get-PythonLauncher
    $Args = @($InstallPy, "--ref", $Ref, "--name", $Name)
    if ($Dest) {
        $Args += @("--dest", $Dest)
    }
    if ($Force) {
        $Args += "--force"
    }

    $InvocationArgs = $Launcher.Prefix + $Args
    & $Launcher.Command @InvocationArgs
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
finally {
    if ($TempFile -and (Test-Path $TempFile)) {
        Remove-Item $TempFile -Force
    }
}
