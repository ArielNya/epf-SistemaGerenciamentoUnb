from data.database import initDb, getDb
from services.AlunoService import AlunoService
from controllers.AlunoController import AlunoController
from services.DiciplinaService import DiciplinaService


class App:
    def __init__(self):
        initDb()
        self.session = next(getDb())
        self.alunoService = AlunoService(self.session)
        self.alunoController = AlunoController(self.alunoService)
        self.diciplinaService = DiciplinaService(self.session)

    def run(self):
        lista = self.alunoController.listarAlunos()
        print(f"{lista}")
        completas = self.alunoService.listarConcluidas(123456)
        print(f'{completas}')

        diciplinas = self.diciplinaService.listarDiciplinas()
        print(f'{diciplinas}')

    def sample(self):
        #self.alunoController.addAluno('Ariel', 123456, 'Eng. Software')
        #self.alunoController.addAluno('Gabi', 1234, 'Filosofia')
        #self.alunoController.addAluno('Lully', 8520, 'Filosofia')
        #self.alunoService.concluir(123, 123456)

        #self.diciplinaService.criarDiciplina('uwu', 12311, None, 120)
        self.diciplinaService.deleteDiciplina(12311)

        self.alunoController.deleteAluno(1234)

    def reset(self):
        self.alunoService.limparLista()


if __name__ == "__main__":
    app = App()
    # app.reset()
    app.sample()
    
    app.run()