# promoHunter - KaBuM! Edition 🎯

O **promoHunter** é un bot de automação e web scraping desenvolvido em Python utilizando **Selenium**. O objetivo do projeto é monitorar preços de produtos na plataforma e-commerce KaBuM!, extrair os dados de forma estruturada, identificar oportunidades abaixo do orçamento e exportar os resultados diretamente para uma planilha.

## 🚀 Funcionalidades

* **Navegação Automatizada:** Realiza buscas por termos específicos (Ex: *PC Gamer*) simulando o comportamento de um usuário real.
* **Lazy-Load Bypass:** Sistema de rolagem de página incremental via JavaScript para forçar o carregamento assíncrono de preços e elementos dinâmicos.
* **Extração Defensiva:** Varre as tags internas de cada bloco de produto individual (`card`) de forma isolada, evitando o desalinhamento entre nomes e preços.
* **Regex Parsing:** Utiliza Expressões Regulares (`re`) para limpar ruídos de HTML (quebras de linha, strings vazias, anúncios patrocinados, avaliações de estrelas e parcelamentos).
* **Data Cleaning:** Converte os preços raspados de formato textual monetário brasileiro (`R$ 2.147,95`) para números reais (`2147.95` em tipo `float`).
* **Smart Alerting:** Alerta visual no terminal caso algum produto seja encontrado abaixo do teto de gastos configurado.
* **Exportação em Excel/CSV:** Armazena os dados finais em arquivo `.csv` utilizando codificação `utf-8-sig` (garante compatibilidade imediata de acentuação nativa no Microsoft Excel).

## 🛠️ Tecnologias Utilizadas

* [Python 3](https://www.python.org/)
* [Selenium WebDriver](https://www.selenium.dev/)
* [Regex (Biblioteca Nativa `re`)](https://docs.python.org/3/library/re.html)
* [CSV (Biblioteca Nativa `csv`)](https://docs.python.org/3/library/csv.html)

## 📁 Estrutura do Projeto

```text
promoHunter/
│
├── src/
│   ├── engine.py       # Configuração e inicialização do WebDriver
│   └── scrapers.py     # Lógica principal de scraping e tratamento de dados
│
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação
