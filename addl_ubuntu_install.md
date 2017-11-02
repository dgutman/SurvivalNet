Requirements.txt for SurvivalNet
——————————————————

$ apt-get update
$ apt-get install git -y
$ apt-get install wget -y

$ apt-get install libboost-dev cmake cmake-curses-gui g++ -y
$ apt-get install python-dev python-numpy -y

$ git clone https://github.com/rmcantin/bayesopt
$ apt-get install cmake -y
$ apt-get install make -y

$ cd bayesopt
$ cmake -DBAYESOPT_PYTHON_INTERFACE=ON .
$ make
$ sudo make install

export PYTHONPATH=$PYTHONPATH:/usr/local/include                  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/include/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
