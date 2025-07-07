// src/api/alunoApi.js
const API_BASE_URL = 'http://localhost:8080'; // Altere se o seu backend estiver em outra porta/endereço

// Função genérica para lidar com respostas da API
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || `Erro na requisição: ${response.status}`);
  }
  return response.json();
};

// --- Funções para Alunos ---

export const getAlunos = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/alunos`);
    return handleResponse(response);
  } catch (error) {
    console.error("Erro ao buscar alunos:", error);
    throw error;
  }
};

export const getAlunoByMatricula = async (matricula) => {
  try {
    const response = await fetch(`${API_BASE_URL}/alunos/${matricula}`);
    return handleResponse(response);
  } catch (error) {
    console.error(`Erro ao buscar aluno com matrícula ${matricula}:`, error);
    throw error;
  }
};


export const addAluno = async (alunoData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/alunos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(alunoData),
    });
    return handleResponse(response);
  } catch (error) {
    console.error("Erro ao adicionar aluno:", error);
    throw error;
  }
};

// Se você tiver uma rota PUT para atualizar alunos, adicione aqui.
// Pelo seu AlunoView.py, parece que não há um PUT para alunos, apenas POST, GET, DELETE.
// Se precisar de edição, o backend precisará de uma rota PUT.
// export const updateAluno = async (matricula, alunoData) => {
//   try {
//     const response = await fetch(`${API_BASE_URL}/alunos/${matricula}`, {
//       method: 'PUT',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(alunoData),
//     });
//     return handleResponse(response);
//   } catch (error) {
//     console.error(`Erro ao atualizar aluno com matrícula ${matricula}:`, error);
//     throw error;
//   }
// };


export const deleteAluno = async (matricula) => {
  try {
    const response = await fetch(`${API_BASE_URL}/alunos/${matricula}`, {
      method: 'DELETE',
    });
    // DELETE pode não retornar JSON, apenas um status 200/204
    if (!response.ok) {
      const errorData = response.status === 204 ? null : await response.json(); // Se 204 (No Content), não tente ler JSON
      throw new Error(errorData?.message || `Erro ao deletar: ${response.status}`);
    }
    return true; // Sucesso na exclusão
  } catch (error) {
    console.error(`Erro ao deletar aluno com matrícula ${matricula}:`, error);
    throw error;
  }
};

// --- Funções para Matrícula/Desmatrícula (assumindo rotas no TurmasView) ---
// No TurmasView.py, as rotas são:
// self.app.route('/turmas/<turmaId:int>/matricular', method='POST', callback=self.matricularAluno)
// self.app.route('/turmas/<turmaId:int>/desmatricular', method='POST', callback=self.desmatricularAluno)
// self.app.route('/turmas/<turmaId:int>/alunos', method='GET', callback=self.listarAlunos) -> Lista alunos matriculados na turma
// self.app.route('/turmas/<alunoId:int>/turmas', method='GET', callback=self.listarTurmasAluno) -> Lista turmas que o aluno está matriculado

// Para a matricula e desmatricula, precisamos enviar o alunoId no corpo da requisição POST
export const matricularAlunoEmTurma = async (turmaId, alunoId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/turmas/${turmaId}/matricular`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ alunoId: alunoId }), // Envia o alunoId no corpo
    });
    return handleResponse(response);
  } catch (error) {
    console.error(`Erro ao matricular aluno ${alunoId} na turma ${turmaId}:`, error);
    throw error;
  }
};

export const desmatricularAlunoDeTurma = async (turmaId, alunoId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/turmas/${turmaId}/desmatricular`, {
      method: 'POST', // O método no seu backend é POST, não DELETE para desmatricular
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ alunoId: alunoId }), // Envia o alunoId no corpo
    });
    return handleResponse(response);
  } catch (error) {
    console.error(`Erro ao desmatricular aluno ${alunoId} da turma ${turmaId}:`, error);
    throw error;
  }
};

// Para listar as turmas que um aluno está matriculado
export const getTurmasDoAluno = async (alunoId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/turmas/${alunoId}/turmas`);
    return handleResponse(response);
  } catch (error) {
    console.error(`Erro ao buscar turmas do aluno ${alunoId}:`, error);
    throw error;
  }
};

// Para listar todas as turmas disponíveis (assumindo que há uma rota em TurmasView.py)
export const getTurmas = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/turmas`); // Rota '/turmas' GET
    return handleResponse(response);
  } catch (error) {
    console.error("Erro ao buscar turmas:", error);
    throw error;
  }
};