from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QInputDialog, QGridLayout
import sys
from errors import ValorInvalidoError
from errors import SaldoInsuficienteError
from conta import Conta



class sfBanco(QWidget):
	def __init__(self):
		super(sfBanco, self).__init__(None)
		self.logIn()	#Chama tela de Log-In
		self.contas = {}
		self.conta = Conta(0, 0.0)

	def logIn(self):
		self.setGeometry(300,300,365,50) #define posição e tamanho da janela, as duplas, respectivamente.
		self.setWindowTitle("Log-In")
		self.cadastroBotao = QPushButton("Cadastrar Conta", self) #Cria botão e define titulo dele.
		self.cadastroBotao.clicked.connect(self.cadastroContas) #Define o que o botão faz quando é clicado, nesse caso chama a funcao 'cadastroContas'.
		self.acessoBotao = QPushButton("Acessar Conta", self) 
		self.acessoBotao.clicked.connect(self.acessoContas)
		self.sairBotao = QPushButton("Sair", self)
		self.sairBotao.clicked.connect(self.close)

		self.grid = QGridLayout() #Inicializa/Cria Layout.
		self.grid.addWidget(self.cadastroBotao, 1,0) #Cria objeto no layout, seus parametros são: o objeto, o numero da linha, e o numero da coluna onde ele vai ficar.
		self.grid.addWidget(self.acessoBotao, 1, 1)
		self.grid.addWidget(self.sairBotao, 4,0,1,2) #Aqui, além dos parametros normais, temos mais dois numeros, que são: quantas linhas ele vai ocupar, e quantas colunas, respectivamente.
		self.setLayout(self.grid) #Define o Layout.

	def cadastroContas(self):
		numConta, ok = QInputDialog.getText(self, 'Cadastar Conta', 'Digite o número da conta:') #Cria dialogo, ele recebe o self da função, o titulo da janela, e a solicitacao do que voce quer.
		if ok:
			if numConta in self.contas: #Se o numero da conta pego no dialogo acima esta dentro do dicionario "self.contas"
				errAddConta = QMessageBox.warning(self, "Informação", "Já existe uma conta cadastrada com este número!") #cria popup, para dar alguma informacao, ele recebe o self da função, o titulo da janela, e a mensagem.
																														#em 'QMessage.warning' o 'warning' é a definição do icone que aparece junto com a msg do popup
			else :
				conta = Conta(numConta, 0.0) #cria objeto conta, passando o numero da conta e um saldo inicial "0.0"
				self.contas[numConta] = conta.saldo #cria conta no dicionario.
				scsAddConta = QMessageBox.information(self, "Informação", "Conta cadastrada com sucesso!") #Cria um popup, com icone diferente.

	def acessoContas(self):
		numAcessoConta, ok = QInputDialog.getText(self, 'Acessar Conta', 'Digite o número da conta:') #outro dialogo.
		if numAcessoConta in self.contas:
			self.conta = Conta(numAcessoConta, self.contas[numAcessoConta])
			self.visaoGeralCC() #Para chamar os outros botoes "saldo, saque, etc." qndo clicar para acessar conta
		else:
			errAcsConta = QMessageBox.warning(self, "Erro", "Não existe uma conta cadastrada com esse número!")

	def visaoGeralCC(self): #Responsavel pelos botoes que aparecem ao acessar conta
		self.setWindowTitle("Visão Geral da Conta") #redefine titulo da janela

		self.saqueBotao = QPushButton("Saque", self)
		self.saqueBotao.clicked.connect(self.saque)
		self.depositoBotao = QPushButton("Depósito", self)
		self.depositoBotao.clicked.connect(self.deposito)
		self.saldoBotao = QPushButton("Saldo", self)
		self.saldoBotao.clicked.connect(self.saldo)
		self.extratoBotao = QPushButton("Extrato", self)
		self.voltarBotao = QPushButton("Sair", self)
		self.voltarBotao.clicked.connect(self.close)

		self.grid.addWidget(self.saldoBotao, 2,0)
		self.grid.addWidget(self.extratoBotao, 2,1)
		self.grid.addWidget(self.saqueBotao, 3,0)
		self.grid.addWidget(self.depositoBotao, 3,1)
		
	def deposito(self):
		valor, ok = QInputDialog.getText(self, 'Depósito', 'Digite o valor desejado:') #dialogo
		valor = float(valor)
		if ok:
			try :
				self.conta.op_deposito(valor) #chama metodo do arquivo "conta.py",  recebendo o valor do dialogo acima
				self.contas[self.conta.numero] = self.conta.saldo #Escreve saldo atual no dicionario
				depScs = QMessageBox.information(self, "Informação", "Deposito realizado com sucesso!")
			except ValorInvalidoError:
				depErr = QMessageBox.warning(self, "Erro", "Valor informado é inválido!")

	def saque(self):
		valor, ok = QInputDialog.getText(self, 'Saque', 'Digite o valor desejado:') #Dialogo
		valor = float(valor)
		if ok:
			try:
				self.conta.op_saque(valor) #chama metodo do arquivo "conta.py", recebendo o valor do dialogo acima
				self.contas[self.conta.numero] = self.conta.saldo #Escreve saldo atual no dicionario
				saqScs = QMessageBox.information(self, "Informação", "Saque realizado com sucesso!")
			except ValorInvalidoError:
				depErr = QMessageBox.warning(self, "Erro", "Valor informado é inválido!")
			except SaldoInsuficienteError:
				depErr = QMessageBox.warning(self, "Erro", "Saldo insuficiente!")

	def saldo(self): #Retorna o saldo
		saldoScs = QMessageBox.information(self, "Saldo", " Conta: %s \n Saldo: R$ %.2f" %(self.conta.numero, self.conta.saldo))

if __name__ == '__main__': #Não sei pra que serve...
	app = QApplication(sys.argv)
	root = sfBanco()
	root.show() #serve para mostrar a classe definida lá no começo
	sys.exit(app.exec_())
