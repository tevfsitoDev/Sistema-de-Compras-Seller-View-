import pandas as pd
import numpy as np
import requests
import sqlite3
from tabulate import tabulate

PyToSql = sqlite3.connect("vendedores.db")
cursor = PyToSql.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Sellers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Usuario TEXT NOT NULL,
  Password TEXT NOT NULL,
  data DATETIME DEFAULT CURRENT_TIMESTAMP
  )
  """) 
PyToSql.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Stock (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 item TEXT NOT NULL,
 quantidade INTEGER NOT NULL,
 preço_und REAL NOT NULL,
 total REAL NOT NULL,
 disponivel INTEGER NOT NULL DEFAULT 1,
 data DATETIME DEFAULT CURRENT_TIMESTAMP
  ) """)
PyToSql.commit()

def verificar_login(u_l,p_l,id_l):
 cursor.execute("SELECT * FROM Sellers WHERE Usuario = ? AND Password = ? AND id = ?",(u_l,p_l,id_l)) 
 user_found = cursor.fetchone()
 if user_found:
  return True
 else:
  return False

def verStock():
 query = "SELECT * FROM Stock WHERE disponivel = 1"
 df = pd.read_sql_query(query,PyToSql)
 if df.empty:
  print("\n Stock Vacio")
 else:
  tabla = tabulate(df,headers='keys', tablefmt='fancy_grid',showindex=False)
  print(tabla)
  
def verForaStock():
 query = "SELECT * FROM Stock WHERE disponivel = 0"
 df = pd.read_sql_query(query,PyToSql)
 if df.empty:
  print("\n offStock Vacio")
 else:
  tabla = tabulate(df,headers='keys', tablefmt='fancy_grid',showindex=False) 
  print(tabla) 
 
def register(n_u,n_p):
 cursor.execute("INSERT INTO Sellers (Usuario,Password) VALUES (?,?)", (n_u,n_p))
 PyToSql.commit()
 
print("--Bem-Vindo Vendedor--")
print()
while True:
 print("--Escolha Uma Opçāo--")
 print("""
 1.Acessar
 2.Cadastro
 3.Sair""")

 op1 = int(input(""))
 if op1 == 1:
  print("Digite Seus Dados\n")
  usuario_login = input("Usuario: ")
  password_login = input("Senha: ")
  id_login = int(input("id: "))
  verificar_login(usuario_login,password_login,id_login)

  if verificar_login(usuario_login,password_login,id_login) == True:
   while True:
    print("Escolha Uma Opçāo.\n")
    print("""
    1.Ver Items Em Stock
    2.Ver Items Fora De Stock
    3.Sair \n""")
    op2 = int(input(""))
    if op2 == 1:
     print("Items Em Stock\n")
     verStock()


     print("1.Editar Item | 2.Novo Item | 3.Sair")
   
     op2_1 = int(input(""))
     if op2_1 == 1:
      print("Digite O ID Do Item A Editar\n")
      op2_2 = int(input(""))
      print("Seleccione A Informaçāo A Editar\n")
      print("""
      1.Item
      2.Quatidade
      3.Preço_und
      4.Total
      5.Mudar A Nāo Disponivel
      """)
    
      op2_3 = int(input(""))
      if op2_3 == 1:
       n_item = input("")
       cursor.execute("UPDATE Stock SET item = ? WHERE id = ?",(n_item,op2_2))
       PyToSql.commit()
       print("Sucesso!")
      elif op2_3 == 2:
       n_quantidade = int(input(""))
       cursor.execute("UPDATE Stock SET quantidade = ? WHERE id = ?",(n_quantidade,op2_2))
       PyToSql.commit()
       print("Sucesso!")
      elif op2_3 == 3:
       n_preço = float(input(""))
       cursor.execute("UPDATE Stock SET preço_und = ? WHERE id = ?",(n_preço,op2))
       PyToSql.commit()
       print("Sucesso!")
      elif op2_3 == 4:
       n_total = float(input(""))
       cursor.execute("UPDATE Stock SET total = ? WHERE id = ?",(n_total,op2_2))            
       PyToSql.commit()
       print("Sucesso!")
      elif op2_3 == 5:
       cursor.execute("UPDATE Stock SET disponivel = 0 WHERE id = ?",(op2_2,))
       PyToSql.commit()
       print("Sucesso!")

     elif op2_1 == 2:
      print("Adicionando um novo item...")
      add_it = input("Nome Do Item: ")
      add_qd = int(input("Quantidade De Items: "))
      add_pr = float(input("Preço Por Unidade: "))
      print("1 = Sim | 0  = Nāo")
      add_dp = int(input("Disponivel Para Compra: "))
      add_tt = add_pr * add_qd
      cursor.execute("INSERT INTO Stock (item,quantidade,preço_und,total,disponivel) VALUES(?,?,?,?,?)", (add_it,add_qd,add_pr,add_tt,add_dp))
      PyToSql.commit()

      
     elif op2_1 == 3:
      print()
      
    elif op2 == 2:
     print("Items Fora De Stock\n")
     verForaStock()

     print("1.Enviar Item De Volta A Stock | 2.Sair ")
     op3 = int(input(""))
     if op3 == 1:
      print("Digite O ID Do Item A Editar\n")
      op3_1 = int(input(""))
      cursor.execute("UPDATE Stock SET disponivel = 1 WHERE id = ?",(op3_1,))
      print("Sucesso!")
      PyToSql.commit()
     elif op3 == 2:
      print()
    elif op2 == 3:
     break
 
 elif op1 == 2:
  print("Bem Vindo Novo Vendedor")
  n_user = input("Nome De Usuario: ")
  n_pword = input("Senha: ")
  register(n_user,n_pword)
  print("Conta Criada Com Sucesso.")
 elif op1 == 3:
  print("Saindo...")
  break  
PyToSql.commit()  
PyToSql.close()
    
    
