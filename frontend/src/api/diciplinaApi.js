
const API_BASE_URL = 'http://localhost:8080'; 
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || `Erro na requisição: ${response.status}`);
  }
  return response.json();
};


export const getDiciplinas = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/diciplinas`);
    return handleResponse(response);
  } catch (error) {
    console.error("Erro ao buscar disciplinas:", error);
    throw error;
  }
};

export const getDiciplinaByCodigo = async (codigo) => {
  try {
    const response = await fetch(`${API_BASE_URL}/diciplinas/${codigo}`);
    return handleResponse(response);
  } catch (error) {
    console.error(`Erro ao buscar disciplina com código ${codigo}:`, error);
    throw error;
  }
};

export const addDiciplina = async (diciplinaData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/diciplinas`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(diciplinaData),
    });
    return handleResponse(response);
  } catch (error) {
    console.error("Erro ao adicionar disciplina:", error);
    throw error;
  }
};

export const deleteDiciplina = async (codigo) => {
  try {
    const response = await fetch(`${API_BASE_URL}/diciplinas/${codigo}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      const errorData = response.status === 204 ? null : await response.json();
      throw new Error(errorData?.message || `Erro ao deletar: ${response.status}`);
    }
    return true; 
  } catch (error) {
    console.error(`Erro ao deletar disciplina com código ${codigo}:`, error);
    throw error;
  }
};
export const addPrerequisito = async (diciplinaCodigo, prereqCodigo) => {
  try {
    const response = await fetch(`${API_BASE_URL}/diciplinas/${diciplinaCodigo}/prerequisitos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ codigo: prereqCodigo }),
    });
    return handleResponse(response);
  } catch (error) {
    console.error(`Erro ao adicionar pré-requisito ${prereqCodigo} à disciplina ${diciplinaCodigo}:`, error);
    throw error;
  }
};

export const deletePrerequisito = async (diciplinaCodigo, prereqCodigo) => {
  try {
    const response = await fetch(`${API_BASE_URL}/diciplinas/${diciplinaCodigo}/prerequisitos/${prereqCodigo}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      const errorData = response.status === 204 ? null : await response.json();
      throw new Error(errorData?.message || `Erro ao deletar pré-requisito: ${response.status}`);
    }
    return true;
  } catch (error) {
    console.error(`Erro ao deletar pré-requisito ${prereqCodigo} da disciplina ${diciplinaCodigo}:`, error);
    throw error;
  }
};

export const getPrerequisitos = async (diciplinaCodigo) => {
  try {
    const response = await fetch(`${API_BASE_URL}/diciplinas/${diciplinaCodigo}/prerequisitos`);
    return handleResponse(response);
  } catch (error) {
    console.error(`Erro ao buscar pré-requisitos da disciplina ${diciplinaCodigo}:`, error);
    throw error;
  }
};

export const getTurmasDaDiciplina = async (diciplinaCodigo) => {
  try {
    const response = await fetch(`${API_BASE_URL}/diciplinas/${diciplinaCodigo}/turmas`);
    return handleResponse(response);
  } catch (error) {
    console.error(`Erro ao buscar turmas da disciplina ${diciplinaCodigo}:`, error);
    throw error;
  }
};