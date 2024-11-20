# Redes-TP2-SDN

Trabajo Práctico 2 de la materia Redes (TA048) - Software-Defined Networks

## Instalacion de dependecias

### mininet

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


    
