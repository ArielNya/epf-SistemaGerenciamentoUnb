
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import AlunoForm from '../components/AlunoForm'; 


 import {
   getAlunos,
   addAluno,
   deleteAluno,
 } from '../api/alunoApi';

const Alunos = () => {
  const [alunos, setAlunos] = useState([]);
  const [editingAluno, setEditingAluno] = useState(null); 
  const [showForm, setShowForm] = useState(false); 
  const navigate = useNavigate();

  
  const fetchAlunos = async () => {
    try {
      const data = await getAlunos();
      setAlunos(data);
    } catch (error) {
      console.error("Erro ao buscar alunos:", error);
      alert("Erro ao buscar alunos. Verifique o console para mais detalhes.");
    }

    setAlunos([
      { matricula: 1, nome: "João Silva", dataNascimento: "2000-01-15", curso: "Engenharia de Software" },
      { matricula: 2, nome: "Maria Oliveira", dataNascimento: "1999-05-20", curso: "Ciência da Computação" },
    ]);
  };

  useEffect(() => {
    fetchAlunos();
  }, []);

  const handleAddEditAluno = async (alunoData) => {
    console.log("Dados do aluno para adicionar/editar:", alunoData);

    if (editingAluno) {
        return
    } else {
      try {
        await addAluno(alunoData);
        alert("Aluno adicionado com sucesso!");
        fetchAlunos(); // Atualiza a lista
        setShowForm(false);
      } catch (error) {
        console.error("Erro ao adicionar aluno:", error);
        alert("Erro ao adicionar aluno. Verifique o console.");
      }
    }
    setShowForm(false);
    setEditingAluno(null);
  };

  const handleDeleteAluno = async (matricula) => {
    if (window.confirm(`Tem certeza que deseja deletar o aluno com matrícula ${matricula}?`)) {
      console.log("Deletar aluno com matrícula:", matricula);
      try {
        await deleteAluno(matricula);
        alert("Aluno deletado com sucesso!");
        fetchAlunos(); 
      } catch (error) {
        console.error("Erro ao deletar aluno:", error);
        alert("Erro ao deletar aluno. Verifique o console.");
      }
    }
  };

  const handleMatricularDesmatricular = (matricula) => {
    navigate(`/alunos/matricular-desmatricular/${matricula}`);
  };

  return (
    <div>
      <h1>Gerenciamento de Alunos</h1>

      <button onClick={() => { setShowForm(true); setEditingAluno(null); }}>
        Adicionar Novo Aluno
      </button>

      {showForm && (
        <AlunoForm
          initialData={editingAluno}
          onSubmit={handleAddEditAluno}
          onCancel={() => { setShowForm(false); setEditingAluno(null); }}
        />
      )}

      <h2>Lista de Alunos</h2>
      {alunos.length === 0 ? (
        <p>Nenhum aluno cadastrado.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Matrícula</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Nome</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Data de Nascimento</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Curso</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {alunos.map((aluno) => (
              <tr key={aluno.matricula}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{aluno.matricula}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{aluno.nome}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{aluno.dataNascimento}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{aluno.curso}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  <button onClick={() => { setEditingAluno(aluno); setShowForm(true); }} style={{ marginRight: '10px' }}>
                    Editar
                  </button>
                  <button onClick={() => handleDeleteAluno(aluno.matricula)} style={{ marginRight: '10px' }}>
                    Deletar
                  </button>
                  <button onClick={() => handleMatricularDesmatricular(aluno.matricula)}>
                    Matricular/Desmatricular
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Alunos;