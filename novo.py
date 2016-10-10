from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QInputDialog, QGridLayout
import sys
from errors import ValorInvalidoError
from errors import SaldoInsuficienteError
from conta import Conta



class sfBanco(QWidget):
	def __init__(self):
		super(sfBanco, self).__init__(None)
		self.logIn()
		self.contas = {}

	def logIn(self):
		self.setGeometry(300,300,365,50)
		self.setWindowTitle("Log-In")
		self.cadastroBotao = QPushButton("Cadastrar Conta", self)
		self.cadastroBotao.clicked.connect(self.cadastroContas)
		self.acessoBotao = QPushButton("Acessar Conta", self)
		self.acessoBotao.clicked.connect(self.acessoContas)
		self.sairBotao = QPushButton("Sair", self)
		self.sairBotao.clicked.connect(self.close)

		self.grid = QGridLayout()
		self.grid.addWidget(self.cadastroBotao, 1,0)
		self.grid.addWidget(self.acessoBotao, 1, 1)
		self.grid.addWidget(self.sairBotao, 4,0,1,2)
		self.setLayout(self.grid)

	def cadastroContas(self):
		numConta, ok = QInputDialog.getInt(self, 'Cadastar Conta', 'Digite o número da conta:')
		if ok:
			if numConta in self.contas:
				errAddConta = QMessageBox.warning(self, "Informação", "Já existe uma conta cadastrada com este número!")
				
			else :
				conta = Conta(numConta)
				self.contas[numConta] = conta.saldo
				scsAddConta = QMessageBox.information(self, "Informação", "Conta cadastrada com sucesso!")

	def acessoContas(self):
		numAcessoConta, ok = QInputDialog.getInt(self, 'Acessar Conta', 'Digite o número da conta:')
		if numAcessoConta in self.contas:
			self.conta = Conta(numAcessoConta)
			self.visaoGeralCC()
		else:
			errAcsConta = QMessageBox.warning(self, "Erro", "Não existe uma conta cadastrada com esse número!")

	def visaoGeralCC(self):
		self.setWindowTitle("Visão Geral da Conta")

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
		valor, ok = QInputDialog.getText(self, 'Depósito', 'Digite o valor desejado:')
		valor = float(valor)
		if ok:
			try :
				self.conta.op_deposito(valor)
				depScs = QMessageBox.information(self, "Informação", "Deposito realizado com sucesso!")
			except ValorInvalidoError:
				depErr = QMessageBox.warning(self, "Erro", "Valor informado é inválido!")

	def saque(self):
		valor, ok = QInputDialog.getText(self, 'Saque', 'Digite o valor desejado:')
		valor = float(valor)
		if ok:
			try:
				self.conta.op_saque(valor)
				saqScs = QMessageBox.information(self, "Informação", "Saque realizado com sucesso!")
			except ValorInvalidoError:
				depErr = QMessageBox.warning(self, "Erro", "Valor informado é inválido!")
			except SaldoInsuficienteError:
				depErr = QMessageBox.warning(self, "Erro", "Saldo insuficiente!")

	def saldo(self):
		saldoScs = QMessageBox.information(self, "Saldo", " Conta: " + str(self.conta.numero) + "\n" + " Saldo: R$" + str(self.conta.saldo))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	root = sfBanco()
	root.show()
	sys.exit(app.exec_())