import requests
import json

# Solicitar que o usuário digite o CNPJ
cnpj = input("Digite o CNPJ (apenas números): ")

# URL da API com o CNPJ fornecido
url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"

# Fazendo a requisição GET
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()

    # Função para imprimir com formatação bonita
    def print_formatted(data):
        print("\n\033[1m" + "=== Dados da Empresa ===" + "\033[0m")
        print(f"\033[1mRazão Social:\033[0m {data.get('razao_social', 'N/A')}")
        print(f"\033[1mNome Fantasia:\033[0m {data.get('nome_fantasia', 'N/A')}")
        print(f"\033[1mCNPJ:\033[0m {data.get('cnpj', 'N/A')}")
        print(f"\033[1mSituação Cadastral:\033[0m {data.get('descricao_situacao_cadastral', 'N/A')} (desde {data.get('data_situacao_cadastral', 'N/A')})")
        print(f"\033[1mData de Início de Atividade:\033[0m {data.get('data_inicio_atividade', 'N/A')}")
        print(f"\033[1mNatureza Jurídica:\033[0m {data.get('natureza_juridica', 'N/A')}")
        print(f"\033[1mCNAE Principal:\033[0m {data.get('cnae_fiscal', 'N/A')} - {data.get('cnae_fiscal_descricao', 'N/A')}")

        print("\n\033[1m=== Endereço ===\033[0m")
        print(f"\033[1mLogradouro:\033[0m {data.get('logradouro', 'N/A')}, Nº {data.get('numero', 'N/A')}, {data.get('complemento', '')}")
        print(f"\033[1mBairro:\033[0m {data.get('bairro', 'N/A')}")
        print(f"\033[1mMunicípio:\033[0m {data.get('municipio', 'N/A')} - {data.get('uf', 'N/A')}")
        print(f"\033[1mCEP:\033[0m {data.get('cep', 'N/A')}")

        print("\n\033[1m=== Contato ===\033[0m")
        print(f"\033[1mTelefone:\033[0m {data.get('ddd_telefone_1', 'N/A')}")
        print(f"\033[1mE-mail:\033[0m {data.get('email', 'N/A')}")

        # Verificando se há CNAEs secundários
        cnaes_secundarios = data.get('cnaes_secundarios', [])
        if cnaes_secundarios:
            print("\n\033[1m=== CNAEs Secundários ===\033[0m")
            for cnae in cnaes_secundarios:
                print(f"- \033[1m{cnae['codigo']}:\033[0m {cnae['descricao']}")

        # Verificando se há sócios
        qsa = data.get('qsa', [])
        if qsa:
            print("\n\033[1m=== Quadro Societário ===\033[0m")
            for socio in qsa:
                print(f"- \033[1mNome do Sócio:\033[0m {socio['nome_socio']}")
                print(f"  \033[1mQualificação:\033[0m {socio['codigo_qualificacao_socio']}")
                print(f"  \033[1mData de Entrada:\033[0m {socio['data_entrada_sociedade']}")

    # Chamando a função para imprimir
    print_formatted(data)

else:
    # Exibindo o erro, se houver
    print(f"Erro: {response.status_code} - {response.text}")
