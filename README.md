# Redes-TP2-SDN

Trabajo Práctico 2 de la materia Redes (TA048) - Software-Defined Networks

## Instalacion de dependecias

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

## Utilizacion del programa

### 1. Levantar controlador de POX

Se debe copiar el codigo de firewall como un complemento externo de pox

    cp firewall.py pox/ext

y luego ejecutar pox de siguendo l2 learning:

    ./pox/pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning firewall

### 2. Levantar la topologia con mininet

Primero se debe levantar la topologia y escribir en la terminal desde la carpeta padre:

    sudo mn --custom topology.py --topo mytopo,ammount_switches=5,ip2=10.0.0.23  --mac  --arp --switch ovsk --controller remote

ammount_switches es la cantidad de switches en la topologia. Para definir la ip del host n escribir ipn=[ip deseada]

### 3. Probar reglas del Firewall

    - Regla 1: Descartar mensajes con puerto destino 80
    
        h3 iperf -u -c h2 -p 80 -> No recibe paquetes
        h3 iperf -u -c h2 -p 100 (contraejemplo) 

    - Regla 2: Descartar mensajes desde el host 1 al puerto 5001 usando UDP 
    
        h4 iperf -u -s -p 5001 &
        h1 iperf -u -c h4 -5001 
    
    - Regla 3: Bloqueo de comunicacion entre 2 hosts cualquiera (bilateral).
    
        h2 iperf -u -c h4 -p 1000
        h4 iperf -u -c h2 -p 1000
