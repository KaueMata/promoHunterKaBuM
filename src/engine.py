from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# # 1. O MOTORISTA (Service) - Agora com Edge
service = Service(EdgeChromiumDriverManager().install())

# # 2. O CARRO (Driver) - Agora um Edge
driver = webdriver.Edge(service=service)

# # 3. A MANOBRA (Maximizar)
driver.maximize_window()