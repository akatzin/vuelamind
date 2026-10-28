# vuelamind

*Um método para auditar e documentar um domínio complexo com um assistente de IA, sem que a documentação se descole da realidade.*

[← English](../README.md)

> O framework em si está escrito em espanhol — mas isso importa menos do que parece. **A pergunta zero da entrevista é em que idioma você quer trabalhar**, e tudo o que o assistente produz a partir daí —seu vault, suas notas, seus relatórios— fica no seu idioma.

---

## O problema

Um assistente de IA esquece: a janela de contexto enche e o começo se dissolve, então cada sessão nasce órfã — sem regras, sem história, sem cicatrizes.

E documentação que nunca é reconciliada com a realidade **mente com confiança**. Seis meses depois, metade do que suas notas afirmam é falso e nada indica qual metade.

vuelamind é um método que quebra as duas coisas ao mesmo tempo — não com um aplicativo, mas com disciplina escrita: **nada se afirma sem ter sido comprovado**, e toda afirmação guarda sua procedência: **medido**, **testemunhado**, **citado**, **inferido** ou **relatado**.

## O que você obtém

Um vault de arquivos de texto puro e um ciclo de quatro atos:

- **Nascer**, uma vez — uma entrevista que produz a certidão de nascimento do seu domínio, com as suas palavras.
- **Retomar**, no início de cada sessão — o assistente mede o estado atual em vez de confiar no que lembra.
- **Reconciliar**, ao encerrar — o que envelheceu é corrigido, o que se aprendeu é escrito.
- **Somar-se**, quando outra máquina entra — o primeiro passo de uma colmeia.

Dentro: uma fila de trabalho ordenada por gravidade real, um registro de decisões que anota *o que me faria mudar de ideia*, e **um livro de erros com 51 lições, cada uma paga com um engano real**.
E o método não só diz que funciona: **dez execuções completas roteirizadas, todas limpas** — veja [PRUEBAS.md](../PRUEBAS.md).
Essa última parte é a valiosa: a estrutura se reconstrói numa tarde; as cicatrizes não.

## Como começar

**Passo 0 — instale um assistente** (pule se já tiver um):

- **macOS / Linux** — o instalador nativo:

  ```
  curl -fsSL https://claude.ai/install.sh | bash
  ```


Com um assistente em mãos, os dois caminhos começam igual — pelo arquivo, não por um comando:

1. Crie uma pasta para o seu domínio e clone o método nela:

   ```
   git clone https://github.com/akatzin/vuelamind.git
   ```

2. Abra o seu assistente **nessa pasta** e diga: **«Inicialize MARCO_Inicial.md»**.

   Não precisa colar nada: o passo 1 já deixou o arquivo em disco, então o assistente o lê.

A primeira pergunta é o seu idioma. **A segunda decide tudo o que vem depois:** este domínio nasce aqui, ou esta máquina se soma a um que já vive?

> Onde o cânone vive —repositório, branch, site— é declarado uma única vez em
> [`config.yml`](../config.yml). Todo o resto remete a esse arquivo em vez de repeti-lo, e uma
> verificação faz o build falhar se alguma cópia se afastar dele.

- **Nasce** — você responde à entrevista. De vinte minutos a uma hora e meia, conforme o quanto você quiser contar, e dá para pausar. Gera o vault, o andaime e os comandos do ciclo.
- **Soma-se** — sem entrevista e sem gerar nada. Chega ao vault existente, confirma que chegou inteiro, instala o ciclo a partir do cânone e passa o bastão para `/vuelamind-join`.

O assistente não fica só na sua palavra: olha a pasta de destino e **para** se você disse *nasce* e encontrou meses de trabalho lá dentro — ou se disse *soma-se* e não encontrou nada.

**O que você precisa:** um assistente que consiga ler seus arquivos e rodar comandos. Qualquer um serve —o método é texto puro—. Se não tiver nenhum, `npm install -g @anthropic-ai/claude-code` é um caminho conhecido.

Fora isso, o framework não pede servidor próprio, nem serviço, nem conta com ele: só duas pastas locais.

Os comandos do ciclo em `skills/` foram escritos para o Claude Code, mas o método é texto puro e não depende de qual modelo o lê.

## Uma máquina, ou várias

Tudo acima supõe uma: um assistente e duas pastas locais. **Essa promessa vale para nascer** — nada mais é preciso para começar.

**Uma segunda máquina precisa alcançar o que a primeira tem**: o vault, o andaime —seu manifesto, seu validador, sua memória— e, se o seu domínio verifica contra sistemas vivos, as credenciais para isso. *Como* os alcança é escolha sua: pasta compartilhada, montagem, clone, réplica automática. O framework não decide o transporte.

`/vuelamind-join` percorre esse caminho, e suas verificações são o ponto: confirma que o vault chegou **inteiro** —pela metade é pior que vazio, porque o assistente mede sobre um buraco e conclui com confiança—, instala o ciclo a partir do cânone e **roda o seu validador como prova de estar dentro**. Os arquivos estarem lá não é o mesmo que poder medir.

**E esse comando ainda não está na máquina nova** — ele viaja com o nascimento. Então uma máquina que nunca nasceu começa onde todo mundo começa: clone este repositório e inicialize `MARCO_Inicial.md`, respondendo *soma-se*. O arquivo traz os comandos consigo; daí em diante quem manda é o comando.

Uma máquina que lê o vault mas não alcança os sistemas ainda é uma instância legítima — só precisa **dizê-lo** ao se declarar, porque daí em diante ela documenta sem verificar.

E existe uma instância legítima que nunca escreve — um conselho assinante da memória de engenharia, um auditor. Sua linha no registro leva `acceso: escribe | lee`, e **ela não se declara: uma instância que escreve a declara**, antes de chegar. Quem só lê conserva o que define o papel: fechar cada sessão sem ter escrito uma letra.

## Requisitos

Um assistente, duas pastas locais e **um shell tipo Unix** — macOS ou Linux.

**Windows não é compatível nativamente.** Os scripts que o framework gera assumem `sh`/`bash` e caminhos POSIX. A via conhecida é rodar seu assistente **dentro de um contêiner Linux** (Docker, por exemplo) e trabalhar ali: tudo o que o framework precisa vive dentro do contêiner, e o sistema hospedeiro deixa de importar.

Essa via do contêiner está **medida, não inferida** — em 2026-08-13. Foi construída e executada com uma imagem que este repositório costumava trazer, com o método já embutido em `/opt/vuelamind`. Dentro dela, os quatro quadrantes da pergunta nascer/somar-se foram percorridos de ponta a ponta, e o assistente parou onde devia parar. **Desde 2026-10-01 essa imagem não vive mais aqui**: qualquer contêiner Linux com o assistente instalado e este repositório clonado dentro serve para o mesmo fim.

O que esse teste **não** cobriu: alcançar sistemas vivos de dentro do contêiner. Uma máquina que lê o vault mas não alcança o que documenta ainda é uma instância legítima — só precisa dizê-lo.

O **núcleo** roda em qualquer sistema, Windows incluído: a entrevista, os modelos, as regras e o livro de erros são texto puro. Você estaria abrindo mão da maquinaria opcional e fazendo à mão o que ela faria — menos cômodo, igualmente válido.

> **De onde isto veio** — uma página conta, no seu próprio repositório (`akatzin/vuelamind-web`): a conversa
> de fevereiro de 2026 com uma IA sobre as suas próprias correntes, e como a resposta a *«sou amnésico
> por design»* virou este método. Dez idiomas. É um ensaio, não documentação — leia se quiser o
> porquê antes do como.

---

## Como fica — um domínio pequeno, de ponta a ponta

*Um exemplo com formato real, condensado. Nada aqui é inventado em tempo de execução: este é o
formato da saída de verdade.*

**A entrevista** pergunta o que é o domínio, onde fica a sua fronteira e —o bloco que mais
importa— **o que conta como verdade aqui**. Alguém que documenta a restauração de uma casa
antiga responde: *a fatura e a foto contam como fonte primária; o que o empreiteiro disse ao
telefone é relatado, e é rotulado como tal.*

**A Fase 1 gera** o vault. A nota panorama, a fila, o registro de decisões, o livro de erros
semeado com as lições herdadas, uma nota por peça do domínio.

**Um mês depois**, a fila tem um item como este:

```markdown
### - [ ] #7 · The bathroom pipework is of unknown age
severidad:: media · the leak risk sits above the finished ceiling

The 2019 invoice covers the kitchen only (measured: invoice read).
The previous owner said "it was all redone" — reported, unverified,
and it contradicts the invoice.

Closing test written in advance: an endoscope photo of the run above
the ceiling, or an invoice naming the bathroom.
```

Repare no que esse item faz: separa **o que foi medido** do **que alguém disse**, registra a
contradição em vez de resolvê-la por palpite, e **escreve o teste que o fecharia antes de o
trabalho começar** — para que ninguém o declare feito depois por intuição.

**No encerramento da sessão**, o assistente mede de novo o que mudou, propõe as edições, espera
um sim, e só então escreve. Se algo que afirmou no mês passado se revelou falso, diz isso
explicitamente em vez de corrigir em silêncio.

---

## Como ele melhora

O método aprende por **patches**: lições com caso real, data e forma de verificação. **Ficam
no domínio que as aprendeu**: o cânone não aceita contribuições, e quem o mantém é o seu dono.

Cada instância que adota um patch o julga contra a sua própria evidência, com três veredictos
possíveis — e **descartar com razão vale mais do que adotar por cortesia**.

Alguém julga o que entra no cânone. Esse papel tem nome e uma definição própria —o que vigia,
o que mede, como julga e o que não é da sua conta— em `WATCHER.md`. Ele vigia **o que entra no
cânone, nunca quem o usa**: não há registro de instalações, e não haverá.

E um domínio nascido sobre uma linha de base mais antiga não fica para trás: **os upgrades de
versão maior têm cerimônia própria** — pequena por design, o conteúdo fica onde está, e um
preflight que aborta em vez de quebrar. As instruções estáveis vivem em `UPGRADE.md`; os
patches do dia a dia nunca passam por ali.

## Licença

Uso pessoal, educacional, comunitário e de pesquisa: **livre**. Uso empresarial: **licença
paga**. E uma condição inegociável: este framework **não deve ser usado para substituir o
trabalho de pessoas empregadas** — ele existe para que as pessoas trabalhem melhor com um
assistente, não para que deixem de ser necessárias.

Detalhes em `LICENSE.md`. Isso o torna **source-available, não open source** pela definição da
OSI, e a licença diz isso com todas as letras em vez de esconder.
