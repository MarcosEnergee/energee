
-- Despejando dados para a tabela `distribuidoras_distribuidoras`
--

INSERT INTO `distribuidoras_distribuidoras` (`id`, `nome`, `status`, `cliente_id`) VALUES
(1, 'Copel', 1, 1),
(2, 'Celesc', 1, 1);

--
-- Despejando dados para a tabela `administradores_administradores`
--

INSERT INTO `administradores_administradores` (`id`, `nome`, `end`, `fone`, `distribuidora_id`, `senha`, `uc`) VALUES
(1, 'Marcos', 'end ficticio tv.44', '897577899', 1, '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '84683481000177'),
(2, 'ENCANTO', 'nao cadastrado', '999999999', 2, '1234', '84683481000177');

-- --------------------------------------------------------
