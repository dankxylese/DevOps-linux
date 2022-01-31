# What is DevOps
## Why DevOps

### Benefits of DevOps

**Four pillars of DevOps best practice**
- Ease of Use (Human interaction)
- Flexibility (When client wants more features at the end of a sprint,, we are flexible to add these)
- Robustness - Faster delivery of product
- Cost - Cost Effective (minimising cost by automating, CI/CD etc..)

### Monolith, 2 tier and Microservices Architectures
Monolith  
(One box that has the front end, back end, database)  
(Everytime you add a feature, you have to restart the entire program)  
(Uptime, responce time, etc..)  

2 tier  
(breaking it down into smaller things with AWS)

Microservices  
(Separating it into even smaller things for improved uptime, and easier updating)


## Installing Vagrant

Download [Normal installers for] Vagrant, VirtualBox, Ruby one-click installer  
Make a folder for Vagrant. Inside of the folder make a "vagrantfile" file, without extensions.
Inside of it, add:  
  
```
Vagrant.configure("2") do |config|  
config.vm.box = "ubuntu/xenial64"  
end  
```

Then, launch gitbash in the same folder as "vagrantfile"
And do "vagrant up" command to start downloading Ubuntu.

Once its up, do "vagrant ssh", and use logout to leave VM
"vagrant halt" stops the vm
