# Oxyscan 
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/burgeridiot/oxyscan/blob/master/README.md) [![pt-pt](https://img.shields.io/badge/lang-pt--pt-green.svg)](https://github.com/burgeridiot/oxyscan/blob/master/README-pt-pt.md)


O Oxyscan é uma aplicação simples feita em Python com a biblioteca Flet, construida para ser usada em hospitais que fazem uso frequente de garrafas de oxigénio, e que não conseguem gerir-las todas. Ela permite que:
- Possa-se adicionar garrafas de oxigénio, com o seu ID, o lote, a localização atual e até o utente a uma lista.
- Guarde-se esta lista localmente, e que depois se possa partilhar para uma base de dados.
- Deixar de haver preocupações com o facto de estar a fazer sempre um setup complicado só para ter uma lista atual de garrafas, bastando simplesmente ligar á base de dados e transferir a lista de garrafas.
- Se hospede um servidor completamente privado e único, em base no SQL.

Esta aplicação precisa de Android 4.0 +.


## Compilação
*nota:* Esta aplicação requer que a compiles manualmente. Porque? Tem a haver com o ultimo ponto: a opção de ter um servidor privado e exclusivo, sendo que o Oxyscan não vem incluído com um servidor principal ou um "browser" de servidores, pois isto iria permitir que se podesse aceder a servidores de maneria ilegita mais facilmente. Daí, ter de compilar manualmente. (porque tem que se alterar as configurações do servidor..)

Para compilar, será preciso:

  - Flet + PyMySQL
  - Flutter
  - Android Studio (No Windows, não sei o programa necessário no MacOS/Linux)
  - Qualquer outra coisa que o Flutter Doctor solicitar durante a compilação. (Para verificar sem precisar de compilar, faz o download do Flutter e executa o comando `flutter doctor -v`).

Basta fazer o download de oxyscan.py, extraí-lo para uma pasta, abrir o terminal na mesma pasta e escrever: `flet build apk --module-name oxyscan.py`. Este processo leva cerca de um minuto, mas se tiver todos os requisitos instalado, deve finalizar com sucesso. Depois disso, está pronto para ser instalado em qualquer aparelho.

## Configuração de um servidor

Para configurar um servidor, só é preciso:

  - MySQL e os seus pré-requisitos (se for novo, sugiro também fazer o download do MySQL Workbench, pois com uma interface visual é mais fácil de trabalhar).

Para quem é especialista em MySQL, isso deve ser uma tarefa fácil, mas se for a sua primeira vez:

  - Se ainda não instalou o MySQL, configure um utilizador adicional chamado "oxyscan_release" e conceda-lhe permissões de Admin do DB durante a instalação.
  - Anote a porta que escolheu durante a instalação do MySQL e o IP da sua máquina, além da password e do utilizador que criou no passo anterior.
  - Inicie o MySQL e crie uma base de dados chamada oxyscan.
  - Substitua o `user` e `password` de exemplo no ficheiro Python pelos que criou, bem como o `ip` e o `port`.
  - Dentro da base de dados, crie uma tabela chamada "garrafas" e adicione as colunas: `garrafa_ID (INT)`, `garrafa_Lote` (INT), `garrafa_Localizacao` (usei LONGTEXT, mas pode-se usar VARCHAR() também) e `garrafa_Utente` (VARCHAR(120)).

E é tudo o que é preciso fazer.

Progresso Atual: 35%
