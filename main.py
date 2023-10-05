from flet import *
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DB_NAME = 'dados.db'
DB_FILE = ROOT_DIR / DB_NAME

# connectar ao banco de dados
connection = sqlite3.connect(DB_FILE,check_same_thread=False)
cur = connection.cursor()

# criar uma tabela no banco de dados
cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS clientes 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
    )
    '''
)

class App(UserControl):
    def __init__(self):
        super().__init__()

        self.all_data = Column(auto_scroll=True)
        self.add_product = TextField(label='Nome do Produto')
        self.edit_data = TextField(label='Editar')

    def delete(self, x, y):
        cur.execute("DELETE FROM clientes WHERE id = ?", [x])
        y.open = False

        # chamando a função de renderizar dados 
        self.all_data.controls.clear()
        self.render_all()
        self.page.update()

    def atualizar(self, x, y, z):
        cur.execute("UPDATE clientes SET name = ? WHERE id = ?", (y,x))
        connection.commit()

        z.open = False
        self.all_data.controls.clear()
        self.render_all()
        self.page.update()

    # Criando a função para abrir as ações
    def abrir_acoes(self, e):
        id_user = e.control.subtitle.value
        self.edit_data.value = e.control.title.value
        self.update()
        alert_dialog = AlertDialog(
            title=Text(f"editar ID {id_user}"),
            content=self.edit_data,

            # botoes de ação
            actions=[
                ElevatedButton(
                    'Deletar',
                    color='white', bgcolor='red',
                    on_click= lambda e: self.delete(id_user, alert_dialog)
                ),
                ElevatedButton(
                    'Atualizar',
                    on_click=lambda e: self.atualizar(id_user
                    ,self.edit_data.value, alert_dialog)

                )
            ],
        )
        self.page.dialog = alert_dialog
        alert_dialog.open = True
        #atualizar a página
        self.page.update()
    # READ: Mostrar todos os dados do banco
    def render_all(self):
        cur.execute("SELECT * FROM clientes")
        connection.commit()

        all_data = cur.fetchall()

        for data in all_data:
            self.all_data.controls.append(
                ListTile(
                    subtitle=Text(data[0]),
                    title=Text(data[1]),
                    on_click=self.abrir_acoes
                )
            )
        self.update()

    def ciclo(self):
        self.render_all()


    # Criar um dado dentro do Banco de dados (CREATE)
    def add_new_data(self, e):
        cur.execute("INSERT INTO clientes (name) VALUES (?)", [self.
        add_product.value])
        connection.commit()

        self.all_data.controls.clear()
        self.render_all()
        self.page.update()


    def build(self):
        return Column([
            Text("CRUD OM SQLITE", size=20, ),
            self.add_product,
            ElevatedButton(
                'Adicionar dado',
                on_click=self.add_new_data,
            ),
            self.all_data
        ])


def main(page: Page):
    page.update()
    minha_aplicação = App()

    page.add(
        minha_aplicação,
    )


app(target=main)
