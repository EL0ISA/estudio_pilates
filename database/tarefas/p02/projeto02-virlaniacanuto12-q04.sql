-- Issue: #57 Registrar Acesso de Funcionário
-- Procedimento 2: Esse procedimento atualiza o campo ultimo_acesso do funcionário com o timestamp atual, sempre que ele faz login no sistema. 
CREATE OR REPLACE PROCEDURE renovar_plano_aluno(
    p_aluno_id INT,
    p_novo_plano_id INT,
    p_data_inicio DATE,
    p_data_fim DATE,
    p_valor NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE aluno
    SET plano_id = p_novo_plano_id,
        data_inicio_plano = p_data_inicio,
        data_fim_plano = p_data_fim
    WHERE id = p_aluno_id;

    INSERT INTO conta_receber (aluno_id, valor, data_vencimento, status)
    VALUES (p_aluno_id, p_valor, p_data_inicio + INTERVAL '1 day', FALSE);
END;
$$;
