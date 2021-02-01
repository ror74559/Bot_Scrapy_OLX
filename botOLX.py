from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
import re

class Bot_OLX:
	def __init__(self):

		options = webdriver.ChromeOptions()

		options.add_argument('lang=pt-br')

		self.driver = webdriver.Chrome(executable_path = r'./chromedriver.exe')

		self.driver.get('https://www.olx.com.br/')


	def buscar(self, produto):

		#Obtendo o caixa de pesquisa
		busca = self.driver.find_element_by_tag_name('input')
		#inserindo o produto no input
		busca.send_keys(f'{produto}')
		#obtendo o botao de pesquisar
		btn_buscar = self.driver.find_element_by_tag_name('#___gatsby > div.bigger-grid-style > div.iza-top > div.iza-container.container > div:nth-child(1) > div > div > div > div.searchButtonBox > button')

		self.action = ActionChains(self.driver)
		#clicando no botão pesquisar
		self.action.move_to_element(btn_buscar).click().perform()
		#obtendo lista com cada resultado da primeira página(50 elementos)
		lista = self.driver.find_elements_by_tag_name('#ad-list > li > a > div')
		#obtendo o link da postagem de cada produto
		link = self.driver.find_elements_by_tag_name('#ad-list > li > a ')
		#obtendo o link da foto dos produtos
		foto = self.driver.find_elements_by_tag_name('#ad-list > li > a > div > div.sc-1q8ortj-0.gIkEbD > div.sc-101cdir-2.kBCTPf > img')
		#Obtendo a quantidade de elementos
		quant_elementos = len(lista)
		#lista que terá como elementos cada resultado da pesquisa com um dicionário				
		res_pesquisa = []

		for i in range(len(lista)):
			#Obtendo o texto de cada elemento da lista e separando_os pela quera de linha
			resultado = (lista[i].text).split('\n')
			#dicionário auxiliar que será adicionado ao res_pesquisa
			dic_aux = {}
			#separando elemento da lista resultado por chaves
			dic_aux['produto'] = resultado[1]
			dic_aux['caracteristicas'] = resultado[2]
			dic_aux['preco'] = ''
			#buscando o preço em cada elemento, pois pode aparecer em posições diferentes, caso tenha.
			for elemento in resultado:
				preco = r'^R\$ ?(\d{1,3}.)?(\d{1,3}.)?(\d{1,3}.)?'
				res = re.fullmatch(preco,elemento)
				if res != None:
					dic_aux['preco'] = res.group(0)
			#verificando o final da lista para obter a localidade, data e hora
			if resultado[len(resultado) - 1] != 'Profissional':
				dic_aux['localidade'] = resultado[len(resultado) - 1]
				dic_aux['data'] = resultado[len(resultado) - 3]
				dic_aux['hora'] = resultado[len(resultado) - 2]
			else:
				dic_aux['localidade'] = resultado[len(resultado) - 2]
				dic_aux['data'] = resultado[len(resultado) - 4]
				dic_aux['hora'] = resultado[len(resultado) - 3]
			dic_aux['link_foto'] = foto[i].get_attribute('src')
			dic_aux['link_postagem'] = link[i].get_attribute('href')
			res_pesquisa.append(dic_aux)
		self.driver.quit()
		return res_pesquisa

bot = Bot_OLX()
print(bot.buscar('casa'))
