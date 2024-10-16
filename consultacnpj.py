import streamlit as st
import requests
import re

# Função para validar CNPJ
def validate_cnpj(cnpj):
    return bool(re.match(r'^\d{14}$', cnpj))

# Função para formatar CNPJ
def format_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)  # Remove caracteres não numéricos
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj

# Título da página
st.title("Consulta de CNPJ")

# Campo de input para o usuário digitar o CNPJ
cnpj_input = st.text_input("Digite o CNPJ (apenas números):", key="cnpj")

# Formatação do CNPJ no campo de input
formatted_cnpj = format_cnpj(cnpj_input)

# Verifica se o CNPJ foi preenchido e é válido
if formatted_cnpj and len(formatted_cnpj) == 18:  # 18 é o comprimento do CNPJ formatado
    # URL da API com o CNPJ fornecido
    url = f"https://brasilapi.com.br/api/cnpj/v1/{formatted_cnpj.replace('.', '').replace('/', '').replace('-', '')}"

    # Fazendo a requisição GET
    with st.spinner("Consultando..."):
        response = requests.get(url)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()

        # Exibindo os dados formatados
        st.subheader("Dados da Empresa")
        st.write(f"**Razão Social:** {data.get('razao_social', 'N/A')}")
        st.write(f"**Nome Fantasia:** {data.get('nome_fantasia', 'N/A')}")
        st.write(f"**CNPJ:** {data.get('cnpj', 'N/A')}")
        st.write(f"**Situação Cadastral:** {data.get('descricao_situacao_cadastral', 'N/A')} (desde {data.get('data_situacao_cadastral', 'N/A')})")
        st.write(f"**Data de Início de Atividade:** {data.get('data_inicio_atividade', 'N/A')}")
        st.write(f"**Natureza Jurídica:** {data.get('natureza_juridica', 'N/A')}")
        st.write(f"**CNAE Principal:** {data.get('cnae_fiscal', 'N/A')} - {data.get('cnae_fiscal_descricao', 'N/A')}")

        st.subheader("Endereço")
        st.write(f"**Logradouro:** {data.get('logradouro', 'N/A')}, Nº {data.get('numero', 'N/A')}, {data.get('complemento', '')}")
        st.write(f"**Bairro:** {data.get('bairro', 'N/A')}")
        st.write(f"**Município:** {data.get('municipio', 'N/A')} - {data.get('uf', 'N/A')}")
        st.write(f"**CEP:** {data.get('cep', 'N/A')}")

        st.subheader("Contato")
        st.write(f"**Telefone:** {data.get('ddd_telefone_1', 'N/A')}")
        st.write(f"**E-mail:** {data.get('email', 'N/A')}")

        # Verificando e exibindo CNAEs secundários
        cnaes_secundarios = data.get('cnaes_secundarios', [])
        if cnaes_secundarios:
            st.subheader("CNAEs Secundários")
            for cnae in cnaes_secundarios:
                st.write(f"- **{cnae['codigo']}**: {cnae['descricao']}")

        # Verificando e exibindo sócios
        qsa = data.get('qsa', [])
        if qsa:
            st.subheader("Quadro Societário")
            for socio in qsa:
                st.write(f"- **Nome do Sócio:** {socio['nome_socio']}")
                st.write(f"  **Qualificação:** {socio['codigo_qualificacao_socio']}")
                st.write(f"  **Data de Entrada:** {socio['data_entrada_sociedade']}")
    else:
        # Exibindo mensagem de erro
        st.error(f"Erro: {response.status_code} - {response.text}")
else:
    # Exibir erro se o CNPJ não é válido
    if formatted_cnpj and len(formatted_cnpj) < 18:
        st.error("CNPJ inválido. Certifique-se de que está digitado apenas com números e possui 14 dígitos.")
