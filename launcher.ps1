$host.ui.RawUI.WindowTitle = "Tacho Inteligente IA"
$env:STREAMLIT_EMAIL = ""
$env:TF_CPP_MIN_LOG_LEVEL = "3"
$env:STREAMLIT_SERVER_HEADLESS = "true"
$env:STREAMLIT_BROWSER_GATHER_USAGE_STATS = "false"
$port = 8510
$url = "http://127.0.0.1:$port"

Write-Host "============================================" -f Cyan
Write-Host "      Tacho Inteligente con IA" -f Cyan
Write-Host "============================================" -f Cyan
Write-Host ""
Write-Host "  Iniciando servidor, espere..." -f Yellow
Write-Host ""

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "C:\Users\jaire\Downloads\TachoInteligenteIA\venv\Scripts\streamlit.exe"
$psi.Arguments = "run", "app.py", "--server.port", $port
$psi.WorkingDirectory = "C:\Users\jaire\Downloads\TachoInteligenteIA"
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false
$proc = [System.Diagnostics.Process]::Start($psi)

Start-Sleep -Seconds 3

# Esperar a que el servidor responda
for ($i = 1; $i -le 60; $i++) {
    try {
        $r = [System.Net.HttpWebRequest]::Create("$url/_stcore/health")
        $r.Timeout = 2000
        $resp = $r.GetResponse()
        if ($resp.StatusCode -eq 200) {
            Write-Host "  Servidor listo!" -f Green
            Write-Host "  Abriendo: $url" -f Green
            Start-Process $url
            Write-Host ""
            Write-Host "  Presiona Ctrl+C para detener" -f Gray
            break
        }
    } catch {
        if ($i % 10 -eq 0) {
            Write-Host "  Esperando servidor... ($i seg)" -f DarkYellow
        }
        Start-Sleep -Seconds 1
    }
}

$proc.WaitForExit()
