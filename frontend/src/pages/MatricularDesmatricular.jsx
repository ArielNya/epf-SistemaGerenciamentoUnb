
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import {
  getAlunoByMatricula,
  getTurmas,
  getTurmasDoAluno,
  matricularAlunoEmTurma,
  desmatricularAlunoDeTurma,
} from '../api/alunoApi'; 

const MatricularDesmatricular = () => {
  const { matricula } = useParams(); 
  const navigate = useNavigate();

  const [aluno, setAluno] = useState(null);
  const [turmasDisponiveis, setTurmasDisponiveis] = useState([]);
  const [turmasDoAluno, setTurmasDoAluno] = useState([]);
  const [selectedTurmaId, setSelectedTurmaId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAlunoAndTurmas = async () => {
    setLoading(true);
    setError(null);
    try {
      const alunoData = await getAlunoByMatricula(parseInt(matricula));
      setAluno(alunoData);

      const allTurmas = await getTurmas();
      setTurmasDisponiveis(allTurmas);

      const alunoTurmas = await getTurmasDoAluno(parseInt(matricula));
      setTurmasDoAluno(alunoTurmas);

    } catch (err) {
      console.error("Erro ao buscar dados de matrícula/desmatrícula:", err);
      setError(err.message || "Erro ao carregar dados.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlunoAndTurmas();
  }, [matricula]);

  const handleMatricular = async () => {
    if (!selectedTurmaId) {
      alert("Selecione uma turma para matricular.");
      return;
    }
    try {
      await matricularAlunoEmTurma(parseInt(selectedTurmaId), parseInt(matricula));
      alert("Aluno matriculado com sucesso!");
      setSelectedTurmaId(''); // Limpa a seleção
      fetchAlunoAndTurmas(); // Atualiza as listas
    } catch (err) {
      console.error("Erro ao matricular aluno:", err);
      alert(`Erro ao matricular: ${err.message}.`);
    }
  };

  const handleDesmatricular = async (turmaId) => {
    if (window.confirm(`Tem certeza que deseja desmatricular o aluno da turma ${turmaId}?`)) {
      try {
        await desmatricularAlunoDeTurma(turmaId, parseInt(matricula));
        alert("Aluno desmatriculado com sucesso!");
        fetchAlunoAndTurmas(); // Atualiza as listas
      } catch (err) {
        console.error("Erro ao desmatricular aluno:", err);
        alert(`Erro ao desmatricular: ${err.message}.`);
      }
    }
  };

  if (loading) {
    return <div>Carregando informações do aluno e turmas...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Erro: {error}</div>;
  }

  if (!aluno) {
    return <div>Aluno não encontrado.</div>; 
  }


  const turmasParaMatricular = turmasDisponiveis.filter(
    (turma) => !turmasDoAluno.some((t) => t.id === turma.id)
  );


  return (
    <div>
      <h1>Gerenciar Matrículas e Desmatrículas para: {aluno.nome} (Matrícula: {aluno.matricula})</h1>

      <button onClick={() => navigate('/alunos')} style={{ marginBottom: '20px', padding: '10px 15px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
        Voltar para a Lista de Alunos
      </button>

      <div style={{ display: 'flex', gap: '40px', marginTop: '20px' }}>
        <div style={{ flex: 1, border: '1px solid #ccc', padding: '20px', borderRadius: '8px' }}>
          <h2>Matricular em Turma</h2>
          {turmasParaMatricular.length === 0 ? (
            <p>Não há turmas disponíveis para matrícula ou o aluno já está matriculado em todas.</p>
          ) : (
            <>
              <label htmlFor="select-turma" style={{ display: 'block', marginBottom: '5px' }}>Selecione uma Turma:</label>
              <select
                id="select-turma"
                value={selectedTurmaId}
                onChange={(e) => setSelectedTurmaId(e.target.value)}
                style={{ width: '100%', padding: '8px', margin: '10px 0', border: '1px solid #ccc', borderRadius: '4px' }}
              >
                <option value="">-- Selecione --</option>
                {turmasParaMatricular.map((turma) => (
                  <option key={turma.id} value={turma.id}>
                    {turma.nome} ({turma.anoSemestre}) - Disc: {turma.disciplinaId}
                  </option>
                ))}
              </select>
              <button onClick={handleMatricular} style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
                Matricular
              </button>
            </>
          )}
        </div>

        <div style={{ flex: 1, border: '1px solid #ccc', padding: '20px', borderRadius: '8px' }}>
          <h2>Turmas Matriculadas</h2>
          {turmasDoAluno.length === 0 ? (
            <p>Este aluno não está matriculado em nenhuma turma.</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {turmasDoAluno.map((turma) => (
                <li key={turma.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid #eee' }}>
                  <span>{turma.nome} ({turma.anoSemestre}) - Disc: {turma.disciplinaId}</span>
                  <button onClick={() => handleDesmatricular(turma.id)} style={{ backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px', padding: '5px 10px', cursor: 'pointer' }}>
                    Desmatricular
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default MatricularDesmatricular;