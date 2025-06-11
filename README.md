# Validar\_Telefone\_Especialidades

Projeto para validar, padronizar e extrair informações relevantes de planilhas de pacientes (especialidades), com foco em validação de números de WhatsApp, CNS e nomes.

---

## 📋 Descrição

Este script processa automaticamente arquivos `.csv` ou `.xlsx` contendo dados de pacientes extraídos do GLPI, realizando:

- **Validação de nomes de pacientes**
- **Validação e padronização de números de telefone/Whatsapp** (com DDI 55 e filtragem por DDD)
- **Validação e padronização do número CNS**
- **Correção automática de nomes comuns com erros de acentuação/caracteres**
- **Geração de arquivos separados de pacientes válidos e inválidos** para facilitar integrações ou campanhas de comunicação

Os dados finais são salvos em arquivos `.csv` separados para casos válidos e inválidos.

---

## 🚀 Instalação & Uso

### 1. Clone o projeto

```bash
git clone https://github.com/gabrielalmeida/validar_telefone_especialidades.git
cd validar_telefone_especialidades
```

### 2. Crie um ambiente virtual (recomendado)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```
pandas
openpyxl
```

### 4. Prepare seus arquivos

Coloque todos os arquivos `.csv` e `.xlsx` a serem processados na mesma pasta do script.

### 5. Execute o script

```bash
python validar_telefone_especialidades.py
```

---

## ⚙️ Como funciona

O script:

- Procura arquivos `.csv` e `.xlsx` na pasta atual.
- Valida nomes, CNS e telefones/Whatsapps, corrige nomes comuns com erros e gera dois arquivos `.csv` para cada entrada: um com dados válidos, outro com inválidos.
- Os arquivos de saída incluem as colunas:
  - Nome Paciente
  - CNS
  - Whatsapp (com DDI 55)
  - Whatsapp (somente DDD)
  - Especialidade (se houver)

---

## 📝 Observações

- **Colunas esperadas:** Nome Paciente ou Título, CNS, Whatsapp ou Telefone, e Especialidade (opcional).
- **DDDs permitidos:** 82, 71, 73, 74, 75, 77, 85, 88, 98, 99, 83, 81, 87, 86, 89, 84, 79.
- Números com 4 ou mais dígitos repetidos consecutivos são descartados.
- Apenas números iniciando com 7, 8 ou 9 (após DDD) são aceitos para celulares.

---

## 📦 Estrutura esperada de arquivos de entrada

| Nome Paciente   | CNS             | Whatsapp/Telefone | Especialidade |
| --------------- | --------------- | ----------------- | ------------- |
| Fulano da Silva | 123456789012345 | 82999999999       | Cardiologia   |

---

## 📄 Configuração YAML (referência para integração)

```yaml
instalacao_uso:
  - passo: Crie um ambiente virtual (recomendado)
    sistemas:
      Windows:
        comandos:
          - python -m venv venv
          - venv\Scripts\activate
      Linux/Mac:
        comandos:
          - python3 -m venv venv
          - source venv/bin/activate

  - passo: Instale as dependências
    comandos:
      - pip install -r requirements.txt
    requirements_txt:
      - pandas
      - openpyxl

  - passo: Prepare seus arquivos
    instrucoes:
      - Coloque todos os arquivos .csv e .xlsx a serem processados na mesma pasta do script.

  - passo: Execute o script
    comandos:
      - python validar_telefone_especialidades.py

como_funciona:
  descricao:
    - Procura arquivos .csv e .xlsx na pasta atual.
    - Valida nomes, CNS e telefones/Whatsapps, corrige nomes comuns com erros e gera dois arquivos .csv para cada entrada: um com dados válidos, outro com inválidos.
    - Os arquivos de saída incluem as colunas:
      - Nome Paciente
      - CNS
      - Whatsapp (com DDI 55)
      - Whatsapp (somente DDD)
      - Especialidade (se houver)

observacoes:
  - Colunas esperadas: Nome Paciente ou Título, CNS, Whatsapp ou Telefone, e Especialidade (opcional).
  - DDDs permitidos: 82, 71, 73, 74, 75, 77, 85, 88, 98, 99, 83, 81, 87, 86, 89, 84, 79.
  - Números com 4 ou mais dígitos repetidos consecutivos são descartados.
  - Apenas números iniciando com 7, 8 ou 9 (após DDD) são aceitos para celulares.

estrutura_entrada:
  colunas:
    - Nome Paciente
    - CNS
    - Whatsapp/Telefone
    - Especialidade
  exemplo:
    - Nome Paciente: Fulano da Silva
    - CNS: 123456789012345
    - Whatsapp/Telefone: 82999999999
    - Especialidade: Cardiologia
```

.

