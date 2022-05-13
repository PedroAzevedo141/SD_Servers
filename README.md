# SD_Servers

## Primeira execução

    Server:
        - cd server
        - python3 server.py --n_max 10 (linux)
        - py server.py --n_max 10 (Windows)

    Server Partner:
        - cd server
        - python3 server_partner.py --n_max 10 (linux)
        - py server_partner.py --n_max 10 (Windows)

    Client:
        - cd client
        - python3 client.py (linux)
        - py client.py (Windows)
## Realizado

    - Server que recebe informações dos clientes
    - Clientes que envia as matrizes para o server
    - Server se comunicando via UDP com os clientes.
    - O cliente esta enviando quando matriz quadradas forem solicitadas pelo usuario
    - O server esta lendo todas as matrizes enviadas pelo user.
    - Desenvolver a multiplicação das matrizes nos servidores
        - Possivel fazer com o NUMPY
    - Enviar as respostas para o client.
    - ArgParser inserido no projeto, para passar argumentos por linha de comandos via terminal.
    - Criar threads para a comunicacao dos clients com o server UDP
    - Limitando o acesso ao servidor principal.
    - Desenvolver uma comunicação do server UDP com outros servers TCP.
    - Criar subprocess para a comunicacao do server UDP com o server TCP
    - Realizar as multiplicacoes nos servidores parceiros.
    

## Não Realizado

    - Realizar a conexcao de N servers parceiros. (Esta setado apenas no primeiro server conectado).

## Desenvolvido

    - Pedro Azevedo Abrantes de Oliveira
    - Jederilson S. Luz
    - Elievelto E Silva