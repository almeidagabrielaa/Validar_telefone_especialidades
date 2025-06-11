import pandas as pd           # Manipulação de dados e leitura de planilhas
import re                     # Expressões regulares (validação e formatação)
import glob                   # Busca por arquivos no diretório
import os                     # Operações do sistema operacional
import unicodedata            # Normalização de caracteres especiais

# Função para verificar se o nome é válido (apenas letras e espaços)
def verificar_nome_valido(nome):
    try:
        if isinstance(nome, bytes):
            nome = nome.decode('utf-8')
    except UnicodeDecodeError:
        print(f"Erro de decodificação: {nome}")
        return False

    nome = unicodedata.normalize('NFKC', nome)
    nome_valido_regex = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$")
    return bool(nome_valido_regex.match(nome))

# Função para validar e formatar telefones (com DDDs específicos e regras de repetição)
def validar_formatar_telefone(telefone):    
    if pd.isnull(telefone) or str(telefone).strip() == '':        
        return None    
    numeros = re.split(r'[;, ]+', str(telefone))  # Permite separar múltiplos números
    for numero in numeros:        
        numero = re.sub(r'\D', '', numero)  # Remove caracteres não numéricos      
        if not numero.startswith('55'):            
            numero = '55' + numero         # Adiciona DDI se faltar        
        numero_sem_ddi = numero[2:]        
        # Valida DDD e formato (só aceita celulares de DDDs definidos e com 9 dígitos)
        if re.fullmatch(r'(82|71|73|74|75|77|85|88|98|99|83|81|87|86|89|84|79)\d{9}', numero_sem_ddi):            
            # Descarta números com 4+ dígitos iguais seguidos, aceita apenas se começar com 7,8,9 após DDD
            if not re.search(r'(\d)\1{3,}', numero_sem_ddi) and numero_sem_ddi[2] in ['7', '8', '9']:                
                return numero    
    return None

# Validação do whatsapp = telefone
def validar_formatar_whatsapp(whatsapp):
    return validar_formatar_telefone(whatsapp)

# Remove o DDI do número para mostrar apenas o DDD+telefone
def remover_ddi(whatsapp):
    if pd.isnull(whatsapp):
        return None
    whatsapp = str(whatsapp)
    if whatsapp.startswith('55'):
        return whatsapp[2:]
    return whatsapp

# Validação de CNS (apenas 15 dígitos)
def validar_cns(cns):
    if pd.isnull(cns):
        return None

    cns = str(cns)
    cns = re.sub(r'\D', '', cns)

    if not re.fullmatch(r'\d{15}', cns):
        return None
    return cns

# Correções de nomes conhecidos com caracteres errados
correcoes_nomes = {
    "Cristiana da Conceiç?o": "Cristiana da Conceição",
    "Edivânia Conceiç?o Dos Santos": "Edivânia Conceição Dos Santos",
    "Nívea de Lucena Brand?o": "Nívea de Lucena Brandão",
    "Valdinete Maria da Conceiç?o Silva": "Valdinete Maria da Conceição Silva",
    "CONCEIÇ?O ELITA SILVA PINTO": "CONCEIÇÃO ELITA SILVA PINTO",
    "Andreia Rom?o da Silva": "Andreia Romão da Silva",
    "Adriana da Conceiç?o Cruz": "Adriana da Conceição Cruz",
    "Ver?nica da Silva": "Verônica da Silva",
    "Claudiceia da Conceiç?o Ramos": "Claudiceia da Conceição Ramos",
    "Solange Guimar?es Dos Santos": "Solange Guimarães Dos Santos",
    "Maria Elenilda Fraz?o Bezerra": "Maria Elenilda Frazão Bezerra"
}

# Função principal que processa cada dataframe (cada aba ou arquivo CSV)
def processar_dataframe(df, arquivo, aba):
    try:
        print(f"📄 Processando: {arquivo} - Aba: {aba}")

        # Identifica nomes das colunas conforme variações possíveis
        col_nome = 'Nome Paciente' if 'Nome Paciente' in df.columns else 'Título'
        col_CNS = next((col for col in df.columns if 'CNS' in col), None)
        col_whatsapp = next((col for col in df.columns if 'Whatsapp' in col), None)        
        col_telefone = next((col for col in df.columns if 'telefone' in col), None)
        col_especialidade = next((col for col in df.columns if 'Especialidade' in col), None)

        # Checagem das colunas mínimas esperadas
        if col_CNS is None or (col_whatsapp is None and col_telefone is None):
            print(f"⚠️ Uma ou mais colunas necessárias não foram encontradas na aba {aba} do arquivo {arquivo}.")
            print(f"🔍 Esperadas: ['Título', 'CNS', 'Whatsapp ou Telefone']")
            print(f"📋 Encontradas: {list(df.columns)}")
            return

        # Corrige nomes problemáticos
        df[col_nome] = df[col_nome].replace(correcoes_nomes)

        # Verifica validade dos nomes
        df['Nome Paciente'] = df[col_nome].apply(lambda nome: verificar_nome_valido(unicodedata.normalize('NFKC', nome)))

        # Validação do CNS
        df['CNS'] = df[col_CNS].apply(validar_cns)

        # Validação e formatação do Whatsapp
        df['Whatsapp'] = df[col_whatsapp].apply(validar_formatar_whatsapp)
        
        # Se Whatsapp inválido, tenta usar o telefone
        if col_telefone is not None:
            linhas_invalidas = df['Whatsapp'].isnull()
            df.loc[linhas_invalidas, 'Whatsapp'] = df.loc[linhas_invalidas, col_telefone].apply(validar_formatar_telefone)

        # Cria coluna Whatsapp 2, sem o DDI
        df['Whatsapp 2'] = df['Whatsapp'].apply(remover_ddi)

        # Define as colunas de saída
        colunas_final = [col_nome, 'CNS', 'Whatsapp', 'Whatsapp 2']
        if col_especialidade:
            colunas_final.append(col_especialidade)

        # Filtra registros válidos
        df_validos = df[
            df['CNS'].notnull() & 
            df['Whatsapp'].notnull()
        ][colunas_final].copy()

        # Ajusta nome das colunas na saída
        df_validos.columns = ['Nome Paciente', 'CNS', 'Whatsapp', 'Whatsapp 2', 'Especialidade'] if col_especialidade else ['Nome Paciente', 'CNS', 'Whatsapp', 'Whatsapp 2']

        # Seleciona registros inválidos (CNS/Whatsapp ausentes ou nome inválido)
        df_invalidos = df[
            (df['CNS'].isnull()) |     
            (df['Whatsapp'].isnull()) |    
            (~df['Nome Paciente'])
        ][colunas_final].copy()

        df_invalidos.columns = df_validos.columns

        # Salva arquivos CSV com os dados válidos e inválidos
        nome_base = arquivo.replace('.xlsx', '').replace('.csv', '')
        output_file_validos = f"{nome_base}_{aba}_validos.csv"
        df_validos.to_csv(output_file_validos, index=False, sep=';')

        print(f"✅ Arquivo salvo (válidos):\n - {output_file_validos}")

        if not df_invalidos.empty:
            output_file_invalidos = f"{nome_base}_{aba}_invalidos.csv"
            df_invalidos.to_csv(output_file_invalidos, index=False, sep=';')
            print(f"⚠️ Arquivo salvo (inválidos):\n - {output_file_invalidos}")
        else:
            print("✅ Nenhum registro inválido encontrado.")

    except Exception as e:
        print(f"❌ Erro ao processar aba {aba} do arquivo {arquivo}: {e}")

# Processa cada arquivo .csv ou .xlsx no diretório
def processar_arquivo(arquivo):
    try:
        ext = os.path.splitext(arquivo)[1].lower()

        if ext == '.csv':
            df = pd.read_csv(arquivo, encoding='utf-8', delimiter=';', on_bad_lines='skip', dtype=str)
            processar_dataframe(df, arquivo, 'especialidade')
        elif ext == '.xlsx':
            sheets = pd.read_excel(arquivo, sheet_name=None, dtype=str)
            for aba, df in sheets.items():
                processar_dataframe(df, arquivo, aba)
        else:
            print(f"❌ Extensão não suportada: {ext}")
    except Exception as e:
        print(f"❌ Erro ao processar o arquivo {arquivo}: {e}")

# Lista todos os arquivos .csv e .xlsx na pasta e executa o processamento
arquivos = glob.glob("*.csv") + glob.glob("*.xlsx")

for arquivo in arquivos:
    processar_arquivo(arquivo)
