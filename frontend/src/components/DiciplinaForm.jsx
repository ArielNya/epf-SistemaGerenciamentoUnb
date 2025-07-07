import React, { useState, useEffect } from 'react';

const DiciplinaForm = ({ initialData, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    nome: '',
    codigo: '', 
    cargaHoraria: '',
    descricao: '',
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {
      setFormData({
        nome: initialData.nome || '',
        codigo: initialData.codigo || '',
        cargaHoraria: initialData.cargaHoraria || '',
        descricao: initialData.descricao || '',
      });
    } else {
      setFormData({ 
        nome: '',
        codigo: '',
        cargaHoraria: '',
        descricao: '',
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const validateForm = () => {
    let newErrors = {};
    if (!formData.nome.trim()) {
      newErrors.nome = 'Nome é obrigatório.';
    }
    if (!formData.cargaHoraria || isNaN(formData.cargaHoraria) || parseInt(formData.cargaHoraria) <= 0) {
      newErrors.cargaHoraria = 'Carga horária deve ser um número positivo.';
    }
    if (!formData.descricao.trim()) {
      newErrors.descricao = 'Descrição é obrigatória.';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      const dataToSubmit = { ...formData };
      if (!initialData) {
        delete dataToSubmit.codigo; 
      }
      onSubmit(dataToSubmit);
    }
  };

  return (
    <div style={{
      border: '1px solid #ccc',
      padding: '20px',
      borderRadius: '8px',
      margin: '20px 0',
      backgroundColor: '#f9f9f9'
    }}>
      <h2>{initialData ? 'Detalhes da Disciplina' : 'Adicionar Nova Disciplina'}</h2>
      <form onSubmit={handleSubmit}>
        {initialData && ( // Exibe o código apenas em modo de visualização/edição
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="codigo" style={{ display: 'block', marginBottom: '5px' }}>Código:</label>
            <input
              type="text"
              id="codigo"
              name="codigo"
              value={formData.codigo}
              disabled // O código não é editável, apenas visualizável
              style={{ width: '100%', padding: '8px', boxSizing: 'border-box', backgroundColor: '#e9ecef' }}
            />
          </div>
        )}
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="nome" style={{ display: 'block', marginBottom: '5px' }}>Nome:</label>
          <input
            type="text"
            id="nome"
            name="nome"
            value={formData.nome}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
          {errors.nome && <p style={{ color: 'red', fontSize: '0.8em' }}>{errors.nome}</p>}
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="cargaHoraria" style={{ display: 'block', marginBottom: '5px' }}>Carga Horária:</label>
          <input
            type="number"
            id="cargaHoraria"
            name="cargaHoraria"
            value={formData.cargaHoraria}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
          {errors.cargaHoraria && <p style={{ color: 'red', fontSize: '0.8em' }}>{errors.cargaHoraria}</p>}
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="descricao" style={{ display: 'block', marginBottom: '5px' }}>Descrição:</label>
          <textarea
            id="descricao"
            name="descricao"
            value={formData.descricao}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box', minHeight: '80px' }}
          ></textarea>
          {errors.descricao && <p style={{ color: 'red', fontSize: '0.8em' }}>{errors.descricao}</p>}
        </div>
        <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', marginRight: '10px' }}>
          {initialData ? 'Salvar Detalhes' : 'Adicionar Disciplina'}
        </button>
        <button type="button" onClick={onCancel} style={{ padding: '10px 20px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
          Cancelar
        </button>
      </form>
    </div>
  );
};

export default DiciplinaForm;