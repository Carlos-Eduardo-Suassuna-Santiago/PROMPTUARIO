# Guia de Contribuição

Obrigado por considerar contribuir com o **Promptuario**! Este documento fornece diretrizes para ajudá-lo a contribuir de forma eficaz.

## Como Contribuir

Existem várias maneiras de contribuir para este projeto:

- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Submeter correções de código
- Adicionar testes

## Processo de Desenvolvimento

Siga estas etapas para contribuir com código:

### 1. Fork e Clone

Faça um fork do repositório e clone-o localmente:

```bash
git clone https://github.com/seu-usuario/promptuario.git
cd promptuario
```

### 2. Configure o Ambiente

Execute o script de setup para configurar o ambiente de desenvolvimento:

```bash
./setup.sh
```

### 3. Crie uma Branch

Crie uma nova branch para sua funcionalidade ou correção:

```bash
git checkout -b feature/nome-da-funcionalidade
```

Use prefixos descritivos:
- `feature/` - para novas funcionalidades
- `bugfix/` - para correções de bugs
- `docs/` - para melhorias na documentação
- `test/` - para adição de testes

### 4. Faça suas Alterações

Desenvolva sua funcionalidade ou correção seguindo as diretrizes de código abaixo.

### 5. Execute os Testes

Certifique-se de que todos os testes passam:

```bash
pytest
```

### 6. Verifique a Qualidade do Código

Execute as ferramentas de linting:

```bash
black .
flake8 .
isort .
```

### 7. Commit suas Alterações

Escreva mensagens de commit claras e descritivas:

```bash
git commit -m "Adiciona funcionalidade X que faz Y"
```

### 8. Push para seu Fork

```bash
git push origin feature/nome-da-funcionalidade
```

### 9. Abra um Pull Request

Abra um Pull Request no repositório original, descrevendo suas alterações de forma clara.

## Diretrizes de Código

- **Estilo:** Siga o PEP 8 para Python. Use Black para formatação automática.
- **Documentação:** Documente funções e classes usando docstrings.
- **Testes:** Adicione testes para novas funcionalidades.
- **Commits:** Faça commits pequenos e focados.

## Reportando Bugs

Ao reportar um bug, inclua:

- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. comportamento atual
- Versão do Python e Django
- Logs de erro (se aplicável)

## Sugerindo Funcionalidades

Ao sugerir uma nova funcionalidade:

- Descreva o problema que ela resolve
- Explique como você imagina que ela funcionaria
- Considere o impacto em outras partes do sistema

## Código de Conduta

Seja respeitoso e profissional em todas as interações. Contribuições que não sigam este princípio não serão aceitas.

## Dúvidas?

Se tiver dúvidas sobre como contribuir, abra uma issue ou entre em contato com os mantenedores do projeto.

Obrigado por contribuir! 🎉
