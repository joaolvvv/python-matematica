# Atividade Final – Persona 2: Curso Superior

Dashboard em Streamlit com a tabela do IBGE (Censo) sobre pessoas com nível superior completo por área de formação, sexo e UF.

## Arquivos
- `app.py` – aplicação Streamlit
- `Tabela_3_Areas_gerais_de_formacao_na_graduacao.xlsx` – dados
- `requirements.txt` – streamlit, pandas, plotly (+ openpyxl para ler o .xlsx)

## Rodar localmente
    pip install -r requirements.txt
    streamlit run app.py

## Deploy (Streamlit Community Cloud)
1. Criar repositório no GitHub e enviar a pasta (`git init`, `git add .`, `git commit`, `git push`).
2. Em share.streamlit.io: Create app → escolher o repositório, branch `main`, arquivo `app.py` → Deploy.
