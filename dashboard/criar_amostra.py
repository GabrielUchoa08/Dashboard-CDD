import pandas as pd

# Nome do arquivo original gigante
NOME_ARQUIVO_ORIGINAL = 'all_jobs.csv' 

# Nome do novo arquivo de amostra que será criado
NOME_ARQUIVO_AMOSTRA = 'all_jobs_amostra.csv'

# Número de linhas que queremos na amostra (suficiente para a análise, leve para o deploy)
NUMERO_DE_LINHAS = 40000 

try:
    print(f"Lendo o arquivo grande: {NOME_ARQUIVO_ORIGINAL}...")
    df = pd.read_csv(NOME_ARQUIVO_ORIGINAL)

    print(f"Criando uma amostra aleatória com {NUMERO_DE_LINHAS} linhas...")
    # Usamos random_state=42 para que a amostra seja sempre a mesma se você precisar rodar de novo
    df_amostra = df.sample(n=NUMERO_DE_LINHAS, random_state=42)

    # Salva o novo arquivo CSV, que será muito menor
    df_amostra.to_csv(NOME_ARQUIVO_AMOSTRA, index=False)

    print(f"SUCESSO! O arquivo '{NOME_ARQUIVO_AMOSTRA}' foi criado e é muito menor que o original.")

except FileNotFoundError:
    print(f"ERRO: O arquivo original '{NOME_ARQUIVO_ORIGINAL}' não foi encontrado nesta pasta.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")