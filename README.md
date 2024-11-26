# Redes-TP2-SDN

Trabajo Práctico 2 de la materia Redes (TA048) - Software-Defined Networks

- [Redes-TP2-SDN](#redes-tp2-sdn)
  - [Instalación](#instalación)
    - [Mininet](#mininet)
    - [Conda](#conda)
      - [Download](#download)
      - [Activation](#activation)
      - [Enviroment creation](#enviroment-creation)
    - [POX](#pox)
    - [iPerf](#iperf)
  - [Uso](#uso)
    - [1.Controller](#1controller)
    - [2.Topology](#2topology)
    - [3.Test](#3test)
      - [Instructivo para iPerf](#instructivo-para-iperf)
      - [Reglas por default en config.json](#reglas-por-default-en-configjson)

## Instalación

### Mininet

    sudo apt install mininet

### Conda

#### Download

    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm ~/miniconda3/miniconda.sh

#### Activation

    source ~/miniconda3/bin/activate    
    conda init --all

#### Enviroment creation

    conda create --name py_2.7 python=2.7
    conda activate py_2.7

### POX

Se necesita como maximo version 3.9 de python, para esto crearemos un ambiente de conda.

    git clone http://github.com/noxrepo/pox
    cd pox
    git checkout ichthyosaur

### iPerf

Herramienta para pruebas de rendimiento

    sudo apt-get install iperf3

## Uso

### 1.Controller

Se debe copiar el codigo de firewall como un complemento externo de pox

    cp firewall.py pox/ext

y luego ejecutar pox de siguendo l2 learning:

    ./pox/pox.py forwarding.l2_learning firewall

### 2.Topology

Luego se debe levantar la topologia y escribir en la terminal desde la carpeta padre:

    sudo mn --custom topology.py --topo mytopo,ammount_switches=5 --mac --arp --switch ovsk --controller remote

- ammount_switches:  cantidad de switches en la topologia
- ipn=[ip deseada]:  define la ip del host n

### 3.Test

#### Instructivo para iPerf

- **Server**

    [host] iperf -s -p [port] &

- **Client**

    [src_host] iperf -c [dst_host] -p [port]

- **Flags**:
  - c : client
  - s : server
  - p : port
  - u : UDP

#### Reglas por default en config.json

- **Regla 1**: Descartar mensajes con puerto destino 80  

    No recibe paquetes

        h3 iperf -c h2 -p 80 

    Recibe paquetes

        h3 iperf -c h2 -p 100 

- **Regla 2**: Descartar mensajes desde el host 1 al puerto 5001 usando UDP  

        h4 iperf -u -s -p 5001 &
        h1 iperf -u -c h4 -5001

- **Regla 3**: Bloqueo de comunicacion entre 2 hosts cualquiera (bilateral entre host2 y host4)

        h2 iperf -c h4 -p 1000
        h4 iperf -c h2 -p 1000
