# SD_Servers

## Primeira execução

    Server:
        - cd server
        - python3 server.py (linux)
        - py server.py (Windows)

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
    

## Não Realizado

    - Desenvolver uma comunicação do server UDP com outros servers TCP.
    - Criar threads para a comunicacao dos clients com o server UDP
    - Criar subprocess para a comunicacao do server UDP com o server TCP
    - Entre outros objetivos ...