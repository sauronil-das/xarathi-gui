## Overview of Key Components

![Overview](https://user-images.githubusercontent.com/42113685/137575029-6f4e29bb-a613-4cb5-b161-c4cf05d8e0eb.png)


### Router

We need to set aside one IP to be static and the rest can DHCP for other devices
which can communicate with the Internet


### Windows PC/Linux/Mac OS

We can use any machine to communicate with the Server PC using terminal (CLI) as long as 
permissions are given which can be set when installing the server.

### The Server

Here we are using CentOS 7 and provided a static IP of 

`192.168.29.101` and port forwaring `X11` Port: `22` 

We have installed `KVM` and two VM with CentOS 7 

`DB-VM` 		 	`INTERFACE-VM`

IP - `192.168.110.111`   IP - `192.168.110.112`


### DB-VM

We have installed `MariaDB` as our database system with schema.sql as backup


### INTERFACE-VM

All of the python scripts are to compute and communicate with the DB-VM using 

`sqlachemy` `os` 


## Goal 

To convert the CLI interface to GUI Interface by providing packages needed to 
support GUI and Tkinter Modules
