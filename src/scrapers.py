import time
import re
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from engine import driver

site = "https://www.kabum.com.br"
driver.get(site)
time.sleep(3)

campo_busca = driver.find_element(By.ID, "inputBusca")
produto = "PC gamer"
campo_busca.send_keys(produto)
campo_busca.send_keys(Keys.ENTER)
time.sleep(4)

# Rolagem incremental para carregar lazy-load dos preços
print("Rolando a página para carregar os produtos...")
scroll_pos = 0
scroll_step = 800

while True:
    scroll_pos += scroll_step
    driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
    time.sleep(0.8)
    page_height = driver.execute_script("return document.body.scrollHeight")
    if scroll_pos >= page_height:
        break

driver.execute_script("window.scrollTo(0, 0);")
time.sleep(2)

print("\n--- PROMO HUNTER: LISTA COMPLETA DA KABUM ---")
cards_produtos = driver.find_elements(By.CSS_SELECTOR, "a.group")


def extrair_preco(card):
    """
    Varre todos os elementos de texto do card e retorna
    o primeiro que pareça um preço válido (R$ + número).
    Ignora parcelas '10x' e avaliações.
    """
    REGEX_PRECO = re.compile(r'R\$\s*[\d.,]+')
    IGNORAR = ["10x", "avalia", "parcela"]

    for tag in ["h4", "h3", "span", "p", "div"]:
        elementos = card.find_elements(By.TAG_NAME, tag)
        for el in elementos:
            texto = el.text.strip()
            if (REGEX_PRECO.search(texto)
                    and not any(ign in texto.lower() for ign in IGNORAR)
                    and len(texto) < 30):
                return texto
    return "Preço não encontrado"


def limpar_preco(texto_preco):
    """
    Converte texto de preço para float.
    Ex: "R$\\n2.147,95" -> 2147.95
    Retorna None se não conseguir converter.
    """
    try:
        # Remove "R$", espaços, quebras de linha e pontos de milhar
        limpo = re.sub(r'[R$\s\n.]', '', texto_preco)
        # Troca vírgula decimal por ponto
        limpo = limpo.replace(',', '.')
        return float(limpo)
    except (ValueError, TypeError):
        return None


# Limite de alerta de preço — altere conforme sua necessidade
ALERTA_ABAIXO_DE = 2000.00

produtos_salvos = []
contador = 1

for card in cards_produtos:
    try:
        nome = card.find_element(
            By.CSS_SELECTOR, "span.text-sm.text-left"
        ).text.strip()
        if not nome:
            continue

        preco_texto = extrair_preco(card)
        preco_float = limpar_preco(preco_texto)

        print(f"Produto {contador}: {nome}")
        print(f"Preço à Vista: {preco_texto}", end="")

        # Alerta de preço baixo
        if preco_float is not None and preco_float < ALERTA_ABAIXO_DE:
            print(f"  ⚠️  ABAIXO DE R$ {ALERTA_ABAIXO_DE:,.2f}!", end="")
    
        print()
        print("-" * 60)
        
        produtos_salvos.append({
            "Produto": nome,
            "Preco_Texto": preco_texto,
            "Preco_Float": preco_float if preco_float is not None else ""
        })

        contador += 1

    except Exception:
        continue

# Salva em CSV
nome_arquivo = "kabum_resultados.csv"
with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["Produto", "Preco_Texto", "Preco_Float"])
    writer.writeheader()
    writer.writerows(produtos_salvos)

print(f"\nTotal de produtos encontrados: {contador - 1}")
print(f"Planilha salva em: {nome_arquivo}")
print("---------------------------------------------")
time.sleep(5)
driver.quit()