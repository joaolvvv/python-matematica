import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Curso Superior", layout="wide")

# ---------------------------------------------------------
# 1) LER A TABELA
# ---------------------------------------------------------
# As 3 primeiras linhas da planilha são títulos, por isso pulamos elas.
tabela = pd.read_excel("Tabela_3_Areas_gerais_de_formacao_na_graduacao.xlsx", header=None, skiprows=3)

# Damos nome para as colunas que vamos usar (a planilha tem uma ordem fixa)
tabela = tabela.iloc[:, :10]
tabela.columns = ["Local", "Total", "Total_Homens", "Total_Mulheres",
                  "Exatas", "Exatas_Homens", "Exatas_Mulheres",
                  "Saude", "Saude_Homens", "Saude_Mulheres"]

# Tiramos a linha da "Fonte" que fica no final
tabela = tabela[tabela["Local"] != "Fonte: IBGE - Censo Demográfico"]

# Tiramos Brasil e as regiões, ficando só com os estados
nao_sao_estados = ["Brasil", "Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]
estados_df = tabela[~tabela["Local"].isin(nao_sao_estados)].copy()

# "Outras áreas" = o que sobra do total depois de tirar as duas áreas da tabela
estados_df["Outras_Homens"] = estados_df["Total_Homens"] - estados_df["Exatas_Homens"] - estados_df["Saude_Homens"]
estados_df["Outras_Mulheres"] = estados_df["Total_Mulheres"] - estados_df["Exatas_Mulheres"] - estados_df["Saude_Mulheres"]

# ---------------------------------------------------------
# 2) BARRA LATERAL (FILTROS)
# ---------------------------------------------------------
st.sidebar.title("Filtros")

todos_estados = list(estados_df["Local"])
padrao = ["Minas Gerais", "Espírito Santo", "São Paulo", "Paraná", "Mato Grosso do Sul"]
estados = st.sidebar.multiselect("Estado", todos_estados, default=padrao)

areas = st.sidebar.multiselect(
    "Área do conhecimento",
    ["Exatas", "Educação e Saúde", "Outras áreas"],
    default=["Exatas", "Educação e Saúde", "Outras áreas"])

sexos = st.sidebar.multiselect("Sexo", ["Homens", "Mulheres"], default=["Homens", "Mulheres"])

# Se o usuário limpar algum filtro, avisamos e paramos
if len(estados) == 0 or len(areas) == 0 or len(sexos) == 0:
    st.warning("Escolha pelo menos uma opção em cada filtro.")
    st.stop()

dados = estados_df[estados_df["Local"].isin(estados)]

# ---------------------------------------------------------
# 3) TÍTULO
# ---------------------------------------------------------
st.title("🎓 Ensino Superior: quem se forma e em quê?")
st.write("Persona: governadores de MG, ES, SP, PR e MS, que querem atrair talentos de alta qualificação.")
st.caption("Fonte: IBGE - Censo Demográfico (pessoas com nível superior completo)")

# ---------------------------------------------------------
# 4) KPIs (números de destaque)
# ---------------------------------------------------------
total = int(dados["Total"].sum())
mulheres = dados["Total_Mulheres"].sum()
pct_mulheres = mulheres / total * 100
pct_exatas = dados["Exatas_Mulheres"].sum() / dados["Exatas"].sum() * 100
pct_saude = dados["Saude_Mulheres"].sum() / dados["Saude"].sum() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Pessoas com curso superior", f"{total:,}".replace(",", "."))
col2.metric("% de mulheres", f"{pct_mulheres:.1f}%")
col3.metric("% de mulheres em Exatas", f"{pct_exatas:.1f}%")
col4.metric("% de mulheres em Educação e Saúde", f"{pct_saude:.1f}%")

# ---------------------------------------------------------
# 5) GRÁFICO: BARRAS 100% EMPILHADAS (proporção de gênero por área)
# ---------------------------------------------------------
st.subheader("Proporção de homens e mulheres por área")

# Montamos uma tabela "comprida" com uma linha para cada combinação
linhas = []
for i, linha in dados.iterrows():
    for area, col in [("Exatas", "Exatas"), ("Educação e Saúde", "Saude"), ("Outras áreas", "Outras")]:
        for sexo in ["Homens", "Mulheres"]:
            linhas.append({
                "Estado": linha["Local"],
                "Área": area,
                "Sexo": sexo,
                "Pessoas": linha[col + "_" + sexo],
            })
grafico_df = pd.DataFrame(linhas)
 
# Aplicamos os filtros de área e sexo
grafico_df = grafico_df[grafico_df["Área"].isin(areas) & grafico_df["Sexo"].isin(sexos)]

# Cálculo da porcentagem: pessoas do sexo / total da área naquele estado
soma = grafico_df.groupby(["Estado", "Área"])["Pessoas"].transform("sum")
grafico_df["Porcentagem"] = grafico_df["Pessoas"] / soma * 100

fig = px.bar(
    grafico_df,
    x="Porcentagem",
    y="Estado",
    color="Sexo",
    facet_row="Área",          # um gráfico para cada área
    orientation="h",
    text=grafico_df["Porcentagem"].round(0).astype(int).astype(str) + "%",
    color_discrete_map={"Homens": "#2E86AB", "Mulheres": "#E4572E"},
)
fig.update_layout(height=250 * len(areas) + 100)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 6) NOTÍCIAS
# ---------------------------------------------------------
st.subheader("📰 Notícias")

st.markdown("**🧠 Fuga de cérebros:** [Apagão profissional: há vagas abertas, mas talentos estão fugindo do Brasil (Tecnoblog)](https://tecnoblog.net/495835/apagao-profissional-ha-vagas-abertas-mas-talentos-estao-fugindo-do-brasil/)")
st.markdown("**💻 Escassez de profissionais de TI:** [Sobram vagas, apesar de salário alto (InfoMoney)](https://www.infomoney.com.br/?p=2260681)")
st.markdown("**👩‍🔬 Mulheres em STEM:** [Quem são as mulheres na ciência (Portal da Indústria)](https://noticias.portaldaindustria.com.br/noticias/inovacao-e-tecnologia/quem-sao-as-mulheres-na-ciencia-e-por-que-elas-precisam-estar-cada-vez-mais-presentes/)")
