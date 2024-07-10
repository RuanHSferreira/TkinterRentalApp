"""
PRAGMA foreign_keys = OFF;
DROP TABLE Locatarios;
PRAGMA foreign_keys = ON;



CREATE TABLE Locadores (
	id_locador INTEGER PRIMARY KEY,
	nome TEXT NOT NULL,
	est_civil TEXT NOT NULL,
	cpf TEXT NOT NULL,
	rg TEXT NOT NULL,
	org_rg TEXT NOT NULL,
	est_rg TEXT NOT NULL,
	cidade TEXT NOT NULL,
	end_estado TEXT NOT NULL,
	end_numero TEXT NOT NULL,
	end_rua TEXT NOT NULL,
	end_bairro TEXT NOT NULL,
	id_contr INTEGER NOT NULL
		REFERENCES Contratos (id_contr)
);

CREATE TABLE Locatarios (
	id_morador INTEGER PRIMARY KEY,
	nome TEXT NOT NULL,
	est_civil TEXT NOT NULL,
	cpf TEXT NOT NULL,
	rg TEXT NOT NULL,
	org_rg TEXT NOT NULL,
	est_rg TEXT NOT NULL,
	cidade TEXT NOT NULL,
	end_estado TEXT NOT NULL,
	id_contr INTEGER NOT NULL
		REFERENCES Contratos (id_contr)
);
"""

import sqlite3

# con = sqlite3.connect("my_db.db")
# cur = con.cursor()


# data = [('Rua Matheus Leite', 3575, 'Mirassol', 'SP', 'S. BERNARDO', '20/08/2023', '19/08/2024', '12 (Mesês)', '1.356,00', 'NÂO', 'LOCADOR', 'RESIDENCIA', 2)]
# print(len(data[0]))
# #cur.execute("CREATE TABLE Locadores(Nome, CPF, RG, Estado_Civil)")

# cur.executemany("""INSERT INTO Contratos (rua, numero, cidade, end_estado, end_bairro, inicio, fim, prazo_loc, valor, caucao, pg_iptu, tipo, id_locador) 
#                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)

#locador_date = [('Ruan H. S. Ferreira', 'solteiro', '502.699.448-26', '22.666.555-44', 'SSP', 'SP', 'MIRASSOL', 'SP', '6598', 'Rua Frei Gil maria', 'S. FRANCISCO'),
#                ('Maria Lurde', 'Divorciada', '365.666.888-45', '33.777.666-55', 'SSP', 'SP', 'MIRASSOL', 'SP', '777', 'Rua MATHEUS', 'S. BERNARDO')]

#cur.executemany("""INSERT INTO Locadores (nome, est_civil, cpf, rg, org_rg, est_rg, cidade, end_estado, end_numero, end_rua, end_bairro)
#                VALUES (?,?,?,?,?,?,?,?,?,?,?)""", locador_date)

# res = cur.execute("SELECT * FROM Locadores")

# for a in res.fetchall():
#     print(a)

# con.commit()

# con.close()


class conn_connection(object):

	def __init__(self, connection_string):
		self.connection_string = connection_string
		self.connectior = None

	def __enter__(self):
		self.connector = sqlite3.Connection(self.connection_string)
		self.cur = self.connector.cursor()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_tb is None:
			self.connector.commit()
		else:
			self.connector.rollback()
		self.connector.close()


class BancoDados:

	def __init__(self, name_banco_dados="my_db.db"):
		with conn_connection(name_banco_dados) as conn:
			self.__name_banco = name_banco_dados
			print(name_banco_dados)
			print("Banco de Dados aberto!\n")
			print("Tabelas Criadas:")
			sql = "SELECT name FROM sqlite_master WHERE type='table';"
			tabs = conn.cur.execute(sql)
			for tables in tabs.fetchall():
				print(str(tables[0]).center(40))

	def show_line(self, name):
		"""
		:param args:
		:return:
		"""
		sql_id = f"SELECT * FROM Locadores WHERE nome='{name}'"
		with conn_connection(self.__name_banco) as conn:
			line = conn.cur.execute(sql_id)
			line = [i for i in line.fetchall() if i]
			if line:
				sql_id = f"SELECT * FROM Contratos WHERE id_locador='{line[0][0]}'"
				contr = conn.cur.execute(sql_id)
				contr = [i for i in contr.fetchall() if i]

				sql_id = f"SELECT * FROM Locatarios WHERE id_morador='{contr[0][-1]}'"
				morador = conn.cur.execute(sql_id)
				morador = [i for i in morador.fetchall() if i]

				line.append(contr)
				line.append(morador)
				return line
			
	def return_ids(self, nome, tabela):
		
		if tabela == 'Locadores':
			sql = f"SELECT id_locador FROM {tabela} WHERE nome='{nome}'"
		else:
			sql = f"SELECT id_morador FROM {tabela} WHERE nome='{nome}'"
		with conn_connection(self.__name_banco) as conn:
			id = conn.cur.execute(sql)
			id = id.fetchone()

		return id

			
	def insert_morador(self, dados=list):
		sql_id = f"""INSERT INTO Locatarios (nome, est_civil, cpf, rg, org_rg, est_rg, cidade, end_estado)
				   VALUES (?,?,?,?,?,?,?,?)"""
		#sql_id = f"INSERT INTO Locatarios (nome, est_civil, cpf, rg, org_rg, est_rg, cidade, end_estado, id_contr)
		#		   VALUES (?,?,?,?,?,?,?,?,?)"
		with conn_connection(self.__name_banco) as conn:
			conn.cur.execute(sql_id, dados)

	def insert_cont(self, dados=list):

		sql_id = f"""INSERT INTO Contratos (rua, numero, cidade, end_estado, end_bairro, inicio, fim, prazo_loc, valor, caucao, pg_iptu, tipo, id_locador, id_morador)
					VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
		
		with conn_connection(self.__name_banco) as conn:
			conn.cur.execute(sql_id, dados)

	def insert_locador(self, dados=list):
		sql_id = f"""INSERT INTO Locadores (nome, est_civil, cpf, rg, org_rg, est_rg, cidade, end_estado, end_numero, end_rua, end_bairro)
					VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
		
		with conn_connection(self.__name_banco) as conn:
			conn.cur.execute(sql_id, dados)
	
	def show_names(self):
		sql = "SELECT nome FROM Locadores"
		with conn_connection(self.__name_banco) as conn:
			line = conn.cur.execute(sql)
			line = [i for i in line.fetchall() if i]
			return line
		
	def search(self, nome):
		
		sql = f"SELECT * FROM Locadores WHERE nome LIKE '%{nome}%'"
		with conn_connection(self.__name_banco) as conn:
			line = conn.cur.execute(sql)
			line = line.fetchall()
			consulta_retorno = []

			if len(line) > 1:
				
				for i in line:

					sql = f"SELECT inicio, fim, id_morador FROM Contratos WHERE id_locador={i[0]}"
					loc = conn.cur.execute(sql)
					loc = loc.fetchall()

					if len(loc) == 0:
						continue

					sql = f"SELECT nome FROM Locatarios WHERE id_morador={loc[0][2]}"
					mor = conn.cur.execute(sql)
					mor = mor.fetchall()
					
					self._temp = []
					self._temp.append(i[1])
					self._temp.append(mor[0][0])
					self._temp.append(f"{loc[0][0]} - {loc[0][1]}")

					consulta_retorno.append(self._temp)
					del mor
					del sql
					del loc
					del self._temp
					
			else:

				sql = f"SELECT inicio, fim, id_morador FROM Contratos WHERE id_locador={line[0][0]}"
				loc = conn.cur.execute(sql)
				loc = loc.fetchall()

				sql = f"SELECT nome FROM Locatarios WHERE id_morador={loc[0][2]}"
				mor = conn.cur.execute(sql)
				mor = mor.fetchall()

				self._temp = []
				self._temp.append(line[0][1])
				self._temp.append(mor[0][0])
				self._temp.append(f"{loc[0][0]} - {loc[0][1]}")

				consulta_retorno.append(self._temp)

			return consulta_retorno
		
	def dados_tkinter(self):
		sql = f"SELECT inicio, fim, id_locador, id_morador FROM Contratos"
		with conn_connection(self.__name_banco) as conn:
			line = conn.cur.execute(sql)
			line = [i for i in line.fetchall() if i]
			dd = []

			for i in line:

				sql = f"SELECT nome FROM Locadores WHERE id_locador={i[-2]}"
				loc_d = conn.cur.execute(sql)
				loc_d = [loc_name for loc_name in loc_d.fetchall() if loc_d]
				
				sql = f"SELECT nome FROM Locatarios WHERE id_morador={i[-1]}"
				mor_d = conn.cur.execute(sql)
				mor_d = [mor_name for mor_name in mor_d.fetchall() if mor_d]

				
				dd.append((loc_d[0][0], mor_d[0][0], i[0]+' - '+i[1]))
				
			return dd


# db = BancoDados()

# locador_id_db = db.return_ids('RUAN HENRIQUE DA SILVA FERREIRA', "Locadores")
# print(str(locador_id_db))

# print(db.dados_tkinter())
#print('Julia fernandes ferreira 33' in db.show_line("juliana 33")[2][0])
# print(len(db.show_line("juliana 33")))
# for i in db.show_line("juliana 33")[2:]:
# 	print("Julia fernandes ferreira 33" in i[0])
# nomes_list_tupl = db.show_names()
# nome = [nm[0] for nm in nomes_list_tupl]
# print(db.dados_tkinter())

# tst = db.show_line('Ruan H. S. Ferreira')
# locador, contrato, morador = tst
# locador = [lc for lc in tst[0]]
# contrato = [ct for ct in tst[1][0]]
# morador = [mr for mr in tst[2][0]]
# print(contrato)
# print(locador)
# print(morador)

# morad = ['Julia fernandes ferreira', 'Solteira', '235.987.689-45', '11.698.245-66',
#  	 	 'SSP', 'SP', 'Mirassol', 'rua dos achados']

#contr_d = ['rua maria 157', '3467', 'mirassol', 'sp', 'favela', '25/06/2023', '24/06/2024', '12 (meses)', '1.300,00', 'não', 'Locador', 'Residencial', 2, 3]
#locador = ['juliana', 'casada', '555.444.333-56', '44.333.777-45', 'SSP', 'SP', 'Mirassol', 'SP', '5675', 'rua sebastiana', 'são das graças']

#db.insert_locador(locador)
#num = 35
# for i in range(1, 41):
# 	morad = [f'Julia fernandes ferreira {i}', 'Solteira', '235.987.689-45', '11.698.245-66',
# 	 	 	 'SSP', 'SP', 'Mirassol', 'rua dos achados']
# 	locador = [f'juliana {i}', 'casada', '555.444.333-56', '44.333.777-45', 'SSP', 'SP', 'Mirassol', 'SP', '5675', 'rua sebastiana', 'são das graças']
# 	contr_d = ['rua maria 157', '3467', 'mirassol', 'sp', 'favela', '25/06/2023', '24/06/2024', '12 (meses)', '1.300,00', 'não', 'Locador', 'Residencial', i, i]
# 	db.insert_morador(morad)
# 	db.insert_locador(locador)
# 	db.insert_cont(contr_d)
	#num += 1


#print(len(contr_d))
#db.insert_morador(morad)
#db.insert_cont(contr_d)
#db.dados_tkinter()
