from data.database import initDb, getDb
from services.AlunoService import AlunoService
from controllers.AlunoController import AlunoController

class App:
    def __init__(self):
        initDb()
        self.session = next(getDb())
        self.alunoService = AlunoService(self.session)
        self.alunoController = AlunoController(self.alunoService)

    def run(self):
        lista = self.alunoController.listarAlunos()
        print(f"{lista}")

    def sample(self):
        self.alunoController.addAluno('Ariel', 123456)
        self.alunoController.addAluno('Gabi', 1234)
        self.alunoController.addAluno('', 8520)

    def reset(self):
        self.alunoService.limparLista()


if __name__ == "__main__":
    app = App()
    #app.reset()
    app.sample()
    
    app.run()