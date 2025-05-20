-- Issue: #57 Calcular divida total do aluno.
-- Função 1: Retorna o valor total das contas a receber de um aluno com status pendente (status = FALSE).CREATE OR REPLACE FUNCTION calcular_total_divida_aluno(p_aluno_id INT)

CREATE OR REPLACE FUNCTION calcular_total_divida_aluno(p_aluno_id INT)
RETURNS NUMERIC AS $$
BEGIN
    RETURN (
        SELECT COALESCE(SUM(valor), 0)
        FROM conta_receber
        WHERE aluno_id = p_aluno_id AND status = FALSE
    );
END;
$$ LANGUAGE plpgsql;
