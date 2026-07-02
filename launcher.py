import subprocess
import sys
import os
import socket
import webbrowser
import time
import urllib.request

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def wait_for_server(url, timeout=30):
    health_url = url + "/_stcore/health"
    for i in range(timeout):
        try:
            with urllib.request.urlopen(health_url, timeout=2):
                return True
        except:
            time.sleep(1)
    return False

if __name__ == "__main__":
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    base = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base, "app.py")
    streamlit = os.path.join(base, "venv", "Scripts", "streamlit.exe")

    env = os.environ.copy()
    env["STREAMLIT_EMAIL"] = ""
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    env["TF_CPP_MIN_LOG_LEVEL"] = "3"

    print("=" * 50)
    print("  Tacho Inteligente con IA")
    print("=" * 50)
    print(f"\n  Iniciando servidor...")

    proc = subprocess.Popen(
        [streamlit, "run", app_path, "--server.port", str(port)],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    print("  Esperando que el servidor esté listo...")
    ready = wait_for_server(url)

    if ready:
        print(f"  OK - Servidor listo en: {url}")
        print(f"\n  Abriendo navegador...")
        webbrowser.open(url)
        print(f"\n  Presiona Ctrl+C para detener")
    else:
        print(f"  ERROR - El servidor no respondio a tiempo")
        proc.terminate()
        sys.exit(1)

    print("=" * 50)

    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        print("\n  Servidor detenido")
        sys.exit(0)
