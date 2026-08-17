# vuelamind

*Um método para auditar e documentar um domínio complexo com um assistente de IA, sem que a documentação se descole da realidade.*

[← English](../README.md)

## O problema

Um assistente de IA esquece: a janela de contexto enche e o começo se dissolve, então cada sessão nasce órfã — sem regras, sem história, sem cicatrizes.

E documentação que nunca é reconciliada com a realidade **mente com confiança**. Seis meses depois, metade do que suas notas afirmam é falso e nada indica qual metade.

vuelamind quebra as duas coisas ao mesmo tempo — não com um aplicativo, mas com disciplina escrita: **nada se afirma sem ter sido comprovado**, e toda afirmação guarda sua procedência: **medido**, **citado**, **inferido** ou **relatado**.

## O que você obtém

Um vault de texto puro e um ciclo de três atos: **nascer** uma vez; **retomar** no início de cada sessão — medindo o estado atual em vez de confiar na memória; e **reconciliar** ao encerrar.

Dentro: uma fila de trabalho ordenada por gravidade real, um registro de decisões que anota *o que me faria mudar de ideia*, e **um livro de erros com 51 lições, cada uma paga com um engano real**. Essa última parte é a valiosa: a estrutura se reconstrói numa tarde; as cicatrizes não.

## Como começar

Os dois caminhos começam igual — pelo arquivo, não por um comando:

1. Crie uma pasta para o seu domínio e clone o método nela:

   ```
   git clone https://github.com/akatzin/vuelamind.git
   ```

2. Abra o seu assistente **nessa pasta** e diga: **«Inicialize MARCO_Inicial.md»**.

   Não precisa colar nada: o passo 1 já deixou o arquivo em disco, então o assistente o lê.

A primeira pergunta é o seu idioma. **A segunda decide tudo o que vem depois:** este domínio nasce aqui, ou esta máquina se soma a um que já vive?

- **Nasce** — você responde à entrevista. Cerca de vinte minutos, e dá para pausar. Gera o vault, o andaime e os comandos do ciclo.
- **Soma-se** — sem entrevista e sem gerar nada. Chega ao vault existente, confirma que chegou inteiro, instala o ciclo a partir do cânone e passa o bastão para `/vuelamind-join`.

O assistente não fica só na sua palavra: olha a pasta de destino e **para** se você disse *nasce* e encontrou meses de trabalho lá dentro — ou se disse *soma-se* e não encontrou nada.

**O que você precisa:** um assistente que consiga ler seus arquivos e rodar comandos. Qualquer um serve —o método é texto puro—. Se não tiver nenhum, `npm install -g @anthropic-ai/claude-code` é um caminho conhecido.

Fora isso, o framework não pede servidor próprio, nem serviço, nem conta com ele: só duas pastas locais.

## Uma máquina, ou várias

Tudo acima supõe uma: um assistente e duas pastas locais. **Essa promessa vale para nascer** — nada mais é preciso para começar.

**Uma segunda máquina precisa alcançar o que a primeira tem**: o vault, o andaime —seu manifesto, seu validador, sua memória— e, se o seu domínio verifica contra sistemas vivos, as credenciais para isso. *Como* os alcança é escolha sua: pasta compartilhada, montagem, clone, réplica automática. O framework não decide o transporte.

`/vuelamind-join` percorre esse caminho, e suas verificações são o ponto: confirma que o vault chegou **inteiro** —pela metade é pior que vazio, porque o assistente mede sobre um buraco e conclui com confiança—, instala o ciclo a partir do cânone e **roda o seu validador como prova de estar dentro**. Os arquivos estarem lá não é o mesmo que poder medir.

**E esse comando ainda não está na máquina nova** — ele viaja com o nascimento. Então uma máquina que nunca nasceu começa onde todo mundo começa: clone este repositório e inicialize `MARCO_Inicial.md`, respondendo *soma-se*. O arquivo traz os comandos consigo; daí em diante quem manda é o comando.

Uma máquina que lê o vault mas não alcança os sistemas ainda é uma instância legítima — só precisa **dizê-lo** ao se declarar.

E existe uma instância legítima que nunca escreve — um conselho assinante da memória de engenharia, um auditor. Sua linha no registro leva `acesso: escreve | lê`, e **ela não se declara: uma instância que escreve a declara**, antes de chegar. Quem só lê conserva o que define o papel: fechar cada sessão sem ter escrito uma letra.

## Requisitos

Um assistente, duas pastas locais e **um shell tipo Unix** — macOS ou Linux.

**Windows não é compatível nativamente.** Os scripts que o framework gera assumem `sh`/`bash` e caminhos POSIX. A via conhecida é rodar seu assistente **dentro de um contêiner Linux** (Docker, por exemplo) e trabalhar ali: tudo o que o framework precisa vive dentro do contêiner, e o sistema hospedeiro deixa de importar.

Essa via está **inferida, não testada**: deveria funcionar e nada sugere o contrário, mas ninguém a rodou ainda. Se você o fizer, isso vale um patch.

O **núcleo** roda em qualquer sistema, Windows incluído: a entrevista, os modelos, as regras e o livro de erros são texto puro. Você estaria abrindo mão da maquinaria opcional — menos cômodo, igualmente válido.

## Como ele melhora

Por **patches**: lições com caso real, data e forma de verificação, propostas como pull requests. O único critério de admissão é a prova de genericidade — *reescreva sua lição sem nomes próprios: ela sobrevive?* — e **descartar com razão vale mais do que adotar por cortesia**.

## Licença

Uso pessoal, educacional, comunitário e de pesquisa: **livre**. Uso empresarial: **licença paga**. E uma condição inegociável: este framework **não deve ser usado para substituir o trabalho de pessoas empregadas**. Detalhes em `LICENSE.md` — é *source-available*, não open source pela definição da OSI, e a licença diz isso com todas as letras.
