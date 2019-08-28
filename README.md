**PLEASE READ ME FIRST!**
====
usage instructions  
====
## 1.required environment
    1. python (recommended 3.7 version)
    2. docker 
    3. IDE(eg: pycharm,intellij)
## 2. announcements
   * This project mainly is a basic digital handwritten recognition program,only supports the pictures with `28*28` form.
   so make sure that you are using the right allowed pictures!
   * To run this project, there are two docker images are needed to build: one for the cassandra database,another for the application.
   What's more,to make sure that two images work smoothly,the two containers should be under the same network.
   * please keep the `same hierarchical structure` with the one on the github.
   * follow the following steps to correctly use the programme.
## 3.using steps
   * download all the files on the github's master branch.
   * open your docker application, make sure it works well.
   * open the terminal.
   * create a network for two images (run the following code in terminal,the next explanations are tha same)<br>
   `docker network create mynetwork`<br>
   * prepare the cassandra database.<br>
   `docker pull cassandra` 
   * create and start cassandra docker image <br>
   `docker run --name mycassandra --network mynetwork -p 9042:9042 -d cassandra:latest`
   * check the cassandra container's IP by using <br>
   `docker inspect <container ID> | grep IPAddress`<br>
   record the container's IP address and open the `database.py`file in your IDE, find the line<br>
   `cluster = Cluster(contact_points=['172.18.0.2'],port=9042)`<br>
   put your record address in the blank like<br>
   `contact_points=['your_container_IPaddress']`<br>
   then save it and quit.
   * now switch your terminal path to folder that contains downloaded files.(you can using `$ ls` to check the files in the folder)
   * create the app docker image<br>
   `docker build -t mnist_app .` <br>
   please make sure that your network is in good condition and wait patiently until it successfully build.
   if there is an error appeared and the reason says `time out`, it means your network is not very well.just retry this command.
   * link this two image into one network and run the newly built docekr image.<br>
   `docker run --name mnistapp --network mynetwork -p 8000:5000 -d mnist_app`
   * then the project could be checked on the link:`localhost:8000`<br>
   you can also use `docker ps`to check the port that the container is used and the address is also showed here.
   * finally, enjoy the little program.
   
   
    
      

   
   