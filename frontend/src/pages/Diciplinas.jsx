import React, { useState, useEffect } from 'react';
import DiciplinaForm from '../components/DiciplinaForm';
import {
  getDiciplinas,
  addDiciplina,
  deleteDiciplina,
} from '../api/diciplinaApi';

const Disciplinas = () => {
  const [diciplinas, setDiciplinas] = useState([]);
  const [editingDiciplina, setEditingDiciplina] = useState(null);
  const [showForm, setShowForm] = useState(false); 

  const fetchDiciplinas = async () => {
    try {
      const data = await getDiciplinas();
      setDiciplinas(data);
    } catch (error) {
      console.error("Erro ao buscar disciplinas:", error);
      alert("Erro ao buscar disciplinas. Verifique o console para mais detalhes.");
    }
  };

  useEffect(() => {
    fetchDiciplinas();
  }, []);

  const handleAddEditDiciplina = async (diciplinaData) => {
    try {
      if (editingDiciplina) {
        alert("Funcionalidade de edição (PUT) para Disciplinas não implementada na API. As alterações não serão salvas.");
        console.warn("Tentativa de editar disciplina, mas não há rota PUT no backend:", diciplinaData);
      } else {
        const added = await addDiciplina(diciplinaData);
        console.log("Disciplina adicionada:", added);
        alert("Disciplina adicionada com sucesso!");
      }
      fetchDiciplinas(); 
      setShowForm(false);
      setEditingDiciplina(null);
    } catch (error) {
      console.error("Erro ao adicionar/editar disciplina:", error);
      alert(`Erro: ${error.message}. Verifique o console para mais detalhes.`);
    }
  };

  const handleDeleteDiciplina = async (codigo) => {
    if (window.confirm(`Tem certeza que deseja deletar a disciplina com código ${codigo}?`)) {
      try {
        await deleteDiciplina(codigo);
        alert("Disciplina deletada com sucesso!");
        fetchDiciplinas(); 
      } catch (error) {
        console.error("Erro ao deletar disciplina:", error);
        alert(`Erro: ${error.message}. Verifique o console para mais detalhes.`);
      }
    }
  };

  return (
    <div>
      <h1>Gerenciamento de Disciplinas</h1>

      <button onClick={() => { setShowForm(true); setEditingDiciplina(null); }} style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', marginBottom: '20px' }}>
        Adicionar Nova Disciplina
      </button>

      {showForm && (
        <DiciplinaForm
          initialData={editingDiciplina}
          onSubmit={handleAddEditDiciplina}
          onCancel={() => { setShowForm(false); setEditingDiciplina(null); }}
        />
      )}

      <h2>Lista de Disciplinas</h2>
      {diciplinas.length === 0 ? (
        <p>Nenhuma disciplina cadastrada.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Código</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Nome</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Carga Horária</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Descrição</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {diciplinas.map((diciplina) => (
              <tr key={diciplina.codigo}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{diciplina.codigo}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{diciplina.nome}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{diciplina.cargaHoraria}h</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{diciplina.descricao}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  <button onClick={() => { setEditingDiciplina(diciplina); setShowForm(true); }} style={{ marginRight: '10px', padding: '8px 12px', backgroundColor: '#ffc107', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Ver Detalhes
                  </button>
                  <button onClick={() => handleDeleteDiciplina(diciplina.codigo)} style={{ padding: '8px 12px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Deletar
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

export default Disciplinas;