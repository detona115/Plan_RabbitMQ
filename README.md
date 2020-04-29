# Plan_RabbitMQ

App que consome dados de um arquivo .csv e os transferem em um pipeline no RabbitMQ

## Propósito 🚀

A idea do sistema consiste em transferir dados atraves do serviço Rabbit, onde em um primeiro momento temos 
um serviço (send.py) que lê um arquivo .csv, converte cada linha do arquivo em dados no formato json e finaliza
em enviar cada linha convertida em um pipeline previamente criado no servidor Rabbit.
Em último momento temos um serviço (receive.py) que recebe cada linha enviado no pipeline e os salvam separadamente
em arquivos .json.

### Pré-requisitos 📋

Para o bom funcionamento desta app as seguintes bibliotecas são necessárias. 
No entanto nenhuma instalação manual é requerida, tudo é feito automaticamente com o docker.

Python 3.5 ou superior

pika

### Instalação e Execução 🔧

#### Após baixar , descompactar e acessar a pasta com os arquivos

N.B: Esta versão foi testada somente com ubuntu

- Em um terminal, execute o seguinte comando para construir as imagem e os containers   
- Antes da execução é necessário ter as portas 5672 e 15672 desocupadas no host para que Rabbit possa funcionar

```
docker-compose up
```         

## Dados gerados 📦

* O arquivo docker-compose foi configurado de tal forma que os arquivos criados pelo receive.py possam ser
acessados e recolhidos caso necessário. Se no momento baixar e descompactar a pasta deste projeto, nenhum nome
for alterado, o nome do volume onde estarão salvos os arquivo .json deve ser
/var/lib/docker/volumes/plan_rabbitmq-master_receiverdata/_data ou similar

## Autor ✒️

* **Andy Kiaka** - *Job Completo* - [detona115](https://github.com/detona115)

---
⌨️ com ❤️ por [detona115](https://github.com/detona115) 😊



