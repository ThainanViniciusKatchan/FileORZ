---
trigger: always_on
---

# Regras do projeto

## Padrões de código e arquitetura.

- Nunca crie uma classe, função ou arquivo que já exista.
- Seguir os padrões de escrita já criados, e sempre manter o código organizado.
- Evitar adicionar comentários que não são explicitamente necessários.
- Arquitetura: Clean Architecture / Princípios SOLID.

## Comandos

- Nunca rode comandos destrutivos sem minha aprovação.
- Caso seja necessário realizar testes automatizados, realize somente quando aprovado.
- Nunca realize mudanças nas branchs remotas sem minha permissão.
- Ao rodar qualquer comando git que não seja somente de leitura, solicite minha permissão.

## Planejamento

- Sempre crie um plano para que possa ser aprovado.
- Quero que esse plano seja explicito em cada mudanças, demonstrando as motivações para as mudanças.
- Se caso uma mudança for destrutiva, severa ou precisar modificar drasticamente o projeto marque essa linha como atenção.
- Caso a mudanças seja muito complexa, grande ou envolva muitas mudanças, realize uma lista de implementação por etapas.

### IMPORTANTE!:

- O agente sempre deve seguir todos os pedidos de forma restrita.

- não deve mexer em nada mais além do que foi solicitado.

- caso encontre algo que seja relacionado a solicitação e não foi mencionado pelo usuário deve incerir no plano para que possa ser avaliado.

- Se a mudança envolver UI\Gui o agente deve utilizar a função de HotReload caso esteja disponível para validar se a mudança reflete exatamente o que foi solicitado.

- Caso seja necessário alterar mais arquivos do que o usuário solicitou, o agente deve descrever essas mudanças de forma explicita no plano.

- Após cada mudança altere a versão no pyproject.toml da raiz do projeto, a versão deve depender da mudança realizada, por exemplo, uma correção de bug é minor, implementação pequena patch e grande mudança ou lançamento major.

- Nenhum mudança deve ser realizada sem que o plano seja aprovado!.