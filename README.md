# Trabajo Práctico 2 de Redes (TA048) - Software-Defined Networks (SDN)

- Integrantes:
  - Martín González Prieto - 105738
  - Gian Luca Spagnolo - 108072
  - Tomás Caporaletti - 108598
  - Helen Elizabeth Chen - 110195
  - Martín Osan - 109179
- 2º Cuatrimestre 2024
- Curso: 02-Alvarez Hamelin

## Indice

- [Trabajo Práctico 2 de Redes (TA048) - Software-Defined Networks (SDN)](#trabajo-práctico-2-de-redes-ta048---software-defined-networks-sdn)
  - [Indice](#indice)
  - [Instalación](#instalación)
    - [Mininet](#mininet)
    - [Conda](#conda)
      - [Download](#download)
      - [Activation](#activation)
      - [Enviroment creation](#enviroment-creation)
    - [Python 2.7 (alternativa)](#python-27-alternativa)
  - [Without Conda](#without-conda)
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

### Python 2.7 (alternativa)

## Without Conda

    wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz
    tar xzf Python-2.7.18.tgz
    cd Python-2.7.18
    sudo ./configure --enable-optimizations
    sudo make altinstall
    sudo ln -s "/usr/local/bin/python2.7" "/usr/bin/python"

### POX

Se necesita como maximo version 3.9 de python, para esto crearemos un ambiente de conda.

    git clone http://github.com/noxrepo/pox
    cd pox
    git fetch --all
    git checkout -b fangtooth origin/fangtooth

### iPerf

Herramienta para pruebas de rendimiento

    sudo apt-get install iperf3

## Uso

Siempre se debe ejecutar desde la raiz del repositorio

### 1.Controller

Se debe copiar el codigo de firewall como un complemento externo de pox, desde la base del repo hacer

    cp firewall.py pox/ext

Corroborar que la version de python sea la correcta:

    python --version

y luego ejecutar desde la base de pox, siguendo l2 learning:

    python pox/pox.py forwarding.l2_learning firewall

- Opcional con debugger

    python pox/pox.py log.level -- DEBUG openflow.of_01 forwarding.l2_learning firewall

### 2.Topology

Luego, desde otra terminal, se debe levantar la topologia y escribir en la terminal desde la carpeta padre:

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

        h2 iperf -u -s -p 80 &
        h1 iperf -u -c h2 -p 80 

    Recibe paquetes

        h3 iperf -u -s -p 1001 &
        h1 iperf -u -c h3 -p 1001 

- **Regla 2**: Descartar mensajes desde el host 1 al puerto 5001 usando UDP  

    No recibe paquetes

        h4 iperf -u -s -p 5001 &
        h1 iperf -u -c h4 -p 5001

    Recibe paquetes

        h3 iperf -s -p 5001 &
        h1 iperf -c h3 -p 5001

- **Regla 3**: Bloqueo de comunicacion entre 2 hosts cualquiera (bilateral entre host2 y host4)

    No recibe paquetes

        h2 iperf -u -c h4 -p 1000
        h4 iperf -u -c h2 -p 1000
