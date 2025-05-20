-- Issue: #57 Registrar Acesso de Funcionário
-- Procedimento 1: 
CREATE OR REPLACE PROCEDURE registrar_acesso_funcionario(p_funcionario_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE studio_funcionario
    SET ultimo_acesso = CURRENT_TIMESTAMP
    WHERE id = p_funcionario_id;
END;
$$;
