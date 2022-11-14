## HW №2. Docker & docker-compose

***
**Task condition։** look 02_docker.md

All services are connected via mac vlan. Access from the host machine to the API service is carried out through the 
default bridge of the network. All parameters are stored in the configuration files of each service.
Macvlan parameters: parent=eth0, subnet="172.31.96.0/20", gateway="172.31.96.1".

To run on another machine, you will need to change them in the docker-compose.yaml file,
and if you need to change the database parameters (for example, the port),
you will have to redo the config files a little. 

The data pack is attached as volume, respectively,
you can easily change the contents of the data.csv file without reassembling.