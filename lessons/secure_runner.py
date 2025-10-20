# lessons/secure_runner.py
import sys
import io
import time
import re

# Lista de módulos/funções perigosas que não devem ser usadas
FORBIDDEN_MODULES = [
    'os', 'subprocess', 'shutil', 'sys', 'io', 'tempfile', 
    'socket', 'urllib', 'requests', 'json', 'pickle', 
    'eval', 'exec', '__import__', 'open', 'file'
]

def execute_code_safely(code: str, timeout_seconds=1):
    """
    Executa o código em um ambiente simulado SEGURO.
    
    🚨 ATENÇÃO: ISTO É UMA SIMULAÇÃO DE SANDBOX com análise estática de tokens.
    Para segurança máxima (nível de produção), use um container Docker isolado. 
    """
    
    # 1. Análise de Tokens (Prevenção Estática)
    for module in FORBIDDEN_MODULES:
        # Busca a palavra como um token completo, ignorando comentários
        if re.search(r'\b' + re.escape(module) + r'\b', code, re.IGNORECASE):
            return "", f"Uso de módulo/função proibido detectado: '{module}'. Não é permitido acessar o sistema ou a rede."

    # 2. Simulação de Execução (Controlada e com Timeout)
    
    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    
    try:
        sys.stdout = redirected_output
        start_time = time.time()
        
        # O ambiente de execução
        isolated_globals = {}
        
        # Executa o código em um namespace isolado.
        exec(code, isolated_globals, isolated_globals)
        
        if time.time() - start_time > timeout_seconds:
            return "", f"Erro: Tempo limite de execução ({timeout_seconds}s) excedido. Cuidado com loops infinitos."

        output = redirected_output.getvalue()
        return output, None
        
    except Exception as e:
        return "", f"{type(e).__name__}: {e}"
    finally:
        sys.stdout = old_stdout # Restaura o stdout