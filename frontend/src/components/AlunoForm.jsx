
import React, { useState, useEffect } from 'react';

const AlunoForm = ({ initialData, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    nome: '',
    dataNascimento: '',
    curso: '',
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {

      const formattedDate = initialData.dataNascimento ? new Date(initialData.dataNascimento).toISOString().split('T')[0] : '';
      setFormData({
        nome: initialData.nome || '',
        dataNascimento: formattedDate,
        curso: initialData.curso || '',
      });
    } else {
      setFormData({
        nome: '',
        dataNascimento: '',
        curso: '',
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
    if (!formData.dataNascimento) {
      newErrors.dataNascimento = 'Data de nascimento é obrigatória.';
    } else {
      const today = new Date();
      const birthDate = new Date(formData.dataNascimento);
      if (birthDate >= today) {
        newErrors.dataNascimento = 'Data de nascimento não pode ser no futuro ou hoje.';
      }
    }
    if (!formData.curso.trim()) {
      newErrors.curso = 'Curso é obrigatório.';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      const dataToSubmit = initialData ? { ...formData, matricula: initialData.matricula } : formData;
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
      <h2>{initialData ? 'Editar Aluno' : 'Adicionar Novo Aluno'}</h2>
      <form onSubmit={handleSubmit}>
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
          <label htmlFor="dataNascimento" style={{ display: 'block', marginBottom: '5px' }}>Data de Nascimento:</label>
          <input
            type="date"
            id="dataNascimento"
            name="dataNascimento"
            value={formData.dataNascimento}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
          {errors.dataNascimento && <p style={{ color: 'red', fontSize: '0.8em' }}>{errors.dataNascimento}</p>}
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="curso" style={{ display: 'block', marginBottom: '5px' }}>Curso:</label>
          <input
            type="text"
            id="curso"
            name="curso"
            value={formData.curso}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
          {errors.curso && <p style={{ color: 'red', fontSize: '0.8em' }}>{errors.curso}</p>}
        </div>
        <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', marginRight: '10px' }}>
          {initialData ? 'Salvar Edição' : 'Adicionar Aluno'}
        </button>
        <button type="button" onClick={onCancel} style={{ padding: '10px 20px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
          Cancelar
        </button>
      </form>
    </div>
  );
};

export default AlunoForm;