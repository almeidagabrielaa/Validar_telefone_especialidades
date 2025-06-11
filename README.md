# Validar_Telefone_Especialidades

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
instalacao_uso:
  - passo: Clone o projeto
    comandos:
      - git clone https://github.com/seuusuario/validar_telefone_especialidades.git
      - cd validar_telefone_especialidades

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

  - passo: Prepare seus arquivos
    instrucoes:
      - Coloque todos os arquivos .csv e .xlsx a serem processados na mesma pasta do script.

  - passo: Execute o script
    comandos:
      - python validar_telefone_especialidades.py
