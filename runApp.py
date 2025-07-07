# run_app.py
import subprocess
import threading
import time
import os

# Define os caminhos relativos para as pastas do backend e frontend
BACKEND_PATH = './backend'
FRONTEND_PATH = './frontend'

def run_backend():
    """Inicia o servidor Bottle (backend)."""
    print("Iniciando o backend (servidor Bottle)...")
    if not os.path.exists(BACKEND_PATH):
        print(f"Erro: Pasta do backend '{BACKEND_PATH}' não encontrada. Certifique-se de que sua aplicação Bottle está lá.")
        return

    # Usamos o cwd (current working directory) para executar o comando na pasta do backend
    # Use 'python -u' para evitar buffer de saída e ver logs em tempo real
    backend_process = subprocess.Popen(['python', '-u', 'main.py'], cwd=BACKEND_PATH, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iter(backend_process.stdout.readline, ''):
        print(f"[BACKEND]: {line}", end='')
    backend_process.wait()
    print("Backend encerrado.")

def run_frontend():
    """Inicia o servidor de desenvolvimento React (frontend)."""
    print("\nIniciando o frontend (servidor de desenvolvimento React)...")
    if not os.path.exists(FRONTEND_PATH):
        print(f"Erro: Pasta do frontend '{FRONTEND_PATH}' não encontrada. Certifique-se de que sua aplicação React está lá.")
        return

    # Usamos o cwd (current working directory) para executar o comando na pasta do frontend
    # Comando para iniciar o frontend React (npm start)
    # Certifique-se de que você já executou 'npm install' ou 'yarn install' na pasta do frontend
    frontend_process = subprocess.Popen(['npm', 'run', 'dev'], cwd=FRONTEND_PATH, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iter(frontend_process.stdout.readline, ''):
        print(f"[FRONTEND]: {line}", end='')
    frontend_process.wait()
    print("Frontend encerrado.")

if __name__ == '__main__':
    # Threads para rodar o backend e o frontend em paralelo
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)

    # Inicia as threads
    backend_thread.start()
    # Dá um pequeno tempo para o backend iniciar antes do frontend (opcional, mas pode ajudar)
    time.sleep(5)
    frontend_thread.start()

    print("\n---------------------------------------------------------")
    print("Servidor Bottle (backend) e Servidor React (frontend) iniciados.")
    print("Acesse o frontend em: http://localhost:3000 (ou a porta que o React indicar)")
    print("Pressione Ctrl+C para parar ambos os servidores.")
    print("---------------------------------------------------------\n")

    try:
        # Mantém o script principal rodando até que as threads terminem (Ctrl+C)
        # O .join() garante que o script principal espera as threads terminarem.
        backend_thread.join()
        frontend_thread.join()
    except KeyboardInterrupt:
        print("\nDetectado Ctrl+C. Encerrando servidores...")
        # Em um cenário mais robusto, você poderia enviar sinais de término aos subprocessos.
        # Para Popen, você pode usar .terminate() ou .kill().
        # Aqui, a simples saída do script Python causará o término dos filhos em muitos OS.
    finally:
        print("Execução finalizada.")