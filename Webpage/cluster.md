---
title:  'Using the GPU cluster of CentraleSupelec'
author:
- Jeremy Fix
keywords: [CentraleSupelec, GPUs]
...


## For the life-long training sessions SM20

Allocation of the GPU machines are handled by a resource manager called
OAR ... but this is not very important for you because I should have
already booked the machines for you ! However, you need the following
script to easily use your GPU machine :

-   [port_forward_host.sh](data/scripts/port_forward_host.sh) : to activate
    port forwarding for Tensorboard, jupyter lab, ...

You should add the execution permission on this file :

``` console
mymachine:~:mylogin$ chmod u+x port_forward_host.sh
```

**Important** For the following, you need to know which login has been
assigned to you, and which hostname has been assigned to you. In the
following, I will denote **dummyLog** your login and **dummyGPU** your
hostname.

### Accessing jupyter lab

I started your reservations with a jupyter lab session running. To
access it. To access it locally, just execute the port\_forward\_host
script specifying the port 8888 :

``` console
mymachine:~:mylogin$ ./port_forward_host.sh dummyLog dummyGPU 8888
```

You can now open **locally** a browser and open the page :
localhost:8888 ; You should reach your jupyter lab session.

### Accessing tensorboard

I now suppose that you already started tensorboard from within a
terminal in jupyter lab. To view locally the tensorboard interface, just
run :

``` console
mymachine:~:mylogin$ ./port_forward_host.sh dummyLog dummyGPU 6006
```

You can now open **locally** a browser and open the page :
localhost:6006 ; You should reach your tensorboard session.


## For the Master (AVR, PSA) students

Allocation of the GPU machines are handled by a resource manager called
OAR ... but this is not very important for you because I should have
already booked the machines for you ! However, you need the following
script to easily use your GPU machine :

-   [port\_forward\_host\_key.sh](data/scripts/port_forward_host_key.sh) : to activate
    port forwarding for Tensorboard, jupyter lab, ...

You should add the execution permission on this file :

``` console
mymachine:~:mylogin$ chmod u+x port_forward_host_key.sh
```

**Important** For the following, you need to know which login has been
assigned to you, and which hostname has been assigned to you. In the
following, I will denote **dummyLog** your login and **dummyGPU** your
hostname. You also need to have the private SSH key, ask your teacher with its path denoted below **path/to/id_rsa**

### Setting up the key

You have to modify the permissions on the file **path/to/id_rsa**

``` console
mymachine:~:mylogin$ chmod 600 path/to/id_rsa
```


### Accessing jupyter lab

I started your reservations with a jupyter lab session running. To
access it. To access it locally, just execute the port\_forward\_host\_key
script specifying the port 8888 :

``` console
mymachine:~:mylogin$ ./port_forward_host_key.sh dummyLog dummyGPU 8888 path/to/id_rsa
```

You can now open **locally** a browser and open the page :
localhost:8888 ; You should reach your jupyter lab session.

### Accessing tensorboard

I now suppose that you already started tensorboard from within a
terminal in jupyter lab. To view locally the tensorboard interface, just
run :

``` console
mymachine:~:mylogin$ ./port_forward_host_key.sh dummyLog dummyGPU 6006 path/to/id_rsa
```

You can now open **locally** a browser and open the page :
localhost:6006 ; You should reach your tensorboard session.




## For the CentraleSupelec students

Allocation of the GPU machines are handled by a resource manager called
OAR. It can be annoying to remember the command lines to reserve a
machine and log to it. We therefore provide the scripts :

-   [book.sh](data/scripts/book.sh) : to book a GPU
-   [kill\_reservation.sh](data/scripts/kill_reservation.sh) : to free the
    reservation
-   [log.sh](data/log.sh) : to log to the booked GPU
-   [port\_forward.sh](data/scripts/port_forward.sh) : to activate port
    forwarding for Tensorboard, jupyter lab, ..
-   [port\_forward\_host.sh](data/scripts/port_forward_host.sh) : to activate
    port forwarding for Tensorboard, jupyter lab, ... if you know the
    remote hostname

After getting these scripts, please make them executables :

```console
mymachine:~:mylogin$ chmod u+x book.sh kill_reservation.sh log.sh port_forward.sh port_forward_host.sh
```

These scripts help you to make a reservation and log to the reserved
machine. These scripts must be in the **same** directory. The book.sh
script handles only one reservation, i.e. running it two times will
simply kill the first reservation.

### From within the campus

Get the scripts and run book.sh and log.sh as below. We also show a
typical output from the execution of the script.

``` console
mymachine:~:mylogin$ ./book.sh mylogin 0
Booking a node
Reservation successfull
Booking requested : OAR_JOB_ID =  99785
Waiting for the reservation to be running, might last few seconds
   The reservation is not yet running 
   The reservation is not yet running 
   The reservation is not yet running 
   The reservation is not yet running 
   [...]
   The reservation is not yet running 
   The reservation is not yet running 
   The reservation is running
The reservation is running
mymachine:~:mylogin$
```

If the reservation is successfull, you can then log to the booked GPU :

``` console
mymachine:~:mylogin$ ./log.sh mylogin 0
The file job_id exists. I am checking the reservation is still valid 
   The reservation is still running 
Logging to the booked node 
Connect to OAR job 99785 via the node sh11
sh11:~:mylogin$ 
```

You end up with a terminal logged on a the GPU machine where you can
execute your code. Your reservation will run for 24 hours. If you need
more time, you may need to tweak the bash script a little bit.

You can log any terminal you wish to the booked machine.

To get access to tensorboard, you need to log to the GPU, start
tensorboard and activate port forwarding :

``` console
[ In a first terminal ]
mymachine:~:mylogin$ ./log.sh mylogin 0
...
sh11:~:mylogin$ tensorboard --logdir path_to_the_logs

[ In a second terminal ]
mymachine:~:mylogin$ ./port_forward.sh mylogin 0 6006
...
```

You can now open a browser on your machine on the port 6006 and you
should get access to tensorboard.

Once your work is finished, just unlog from the machine and run kill_reservation.sh. Please kill your reservation as soon as your work is finished in order to allow other users to book it. 

``` console
sh11:~:mylogin$ logout
Connection to sh11 closed.
Disconnected from OAR job 99785
Connection to term2.grid closed.
  Unlogged 
mymachine:/home/mylogin:mylogin$ ./kill_reservation.sh mylogin 0
 The file job_id exists. I will kill the previous reservation in case it is running
Deleting the job = 99785 ...REGISTERED.
The job(s) [ 99785 ] will be deleted in a near future.
Waiting for the previous job to be killed
Done
mymachine:~:mylogin$
```

### From outside the campus

Get the scripts and run book.sh as below. We also show a typical output
from the execution of the script. The only difference with the calls in
the previous paragraph is the last parameter of the script : 1 instead
of 0.

``` console
mymachine:~:mylogin$ ./book.sh mylogin 1
Booking a node
Reservation successfull
Booking requested : OAR_JOB_ID =  99785
Waiting for the reservation to be running, might last few seconds
   The reservation is not yet running 
   The reservation is not yet running 
   The reservation is not yet running 
   The reservation is not yet running 
   [...]
   The reservation is not yet running 
   The reservation is not yet running 
   The reservation is running
The reservation is running
mymachine:~:mylogin$
```

If the reservation is successfull, you can then log to the booked GPU :

``` console
mymachine:~:mylogin$ ./log.sh mylogin 1
The file job_id exists. I am checking the reservation is still valid 
   The reservation is still running 
Logging to the booked node 
Connect to OAR job 99785 via the node sh11
sh11:~:mylogin$ 
```

You end up with a terminal logged on a the GPU machine where you can
execute your code. Your reservation will run for 24 hours. If you need
more time, you may need to tweak the bash script a little bit.

You can log any terminal you wish to the booked machine.

To get access to tensorboard, you need to log to the GPU, start
tensorboard and activate port forwarding :

``` console
[ In a first terminal ]
mymachine:~:mylogin$ ./log.sh mylogin 1
...
sh11:~:mylogin$ tensorboard --logdir path_to_the_logs
[ In a second terminal ]
mymachine:~:mylogin$ ./port_forward.sh mylogin 1 6006
...
```

You can now open a browser on your machine on the port 6006 and you
should get access to tensorboard.

Once your work is finished, just unlog from the machine and run
kill\_reservation.sh:

``` console
sh11:~:mylogin$ logout
Connection to sh11 closed.
Disconnected from OAR job 99785
Connection to term2.grid closed.
  Unlogged 
mymachine:/home/mylogin:mylogin$ ./kill_reservation.sh mylogin 1
 The file job_id exists. I will kill the previous reservation in case it is running
Deleting the job = 99785 ...REGISTERED.
The job(s) [ 99785 ] will be deleted in a near future.
Waiting for the previous job to be killed
Done
mymachine:~:mylogin$
```