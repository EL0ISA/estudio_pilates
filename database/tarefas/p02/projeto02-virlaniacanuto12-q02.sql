-- Issue: #57 Quantidade aulas realizadas.
-- Função 2: Retorna o valor total das contas a receber de um aluno com status pendente (status = FALSE).CREATE OR REPLACE FUNCTION calcular_total_divida_aluno(p_aluno_id INT)

CREATE OR REPLACE FUNCTION quantidade_aulas_realizadas(p_aluno_id INT)
RETURNS INT AS $$
BEGIN
    RETURN (
        SELECT COUNT(*)
        FROM aula_aluno aa
        JOIN aula a ON a.id = aa.aula_id
        WHERE aa.aluno_id = p_aluno_id AND a.frequencia = TRUE
    );
END;
$$ LANGUAGE plpgsql;