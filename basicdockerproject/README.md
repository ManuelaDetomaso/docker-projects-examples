# TO RUN THE APPLICATION LOCALLY 

In the terminal submit:

```
export FLASK_APP=app.py
flask run
```
The app.py should be considered as the Web Server in the Web Cycle Development

# API ELEMENTS
- RESOURCE 

    Often the piece of code to execute

- METHODS

    * A GET request does not require e massage body, just gives the source which is asked
    * A POST requests needs a message body to give the source which is asked. It is meant for creating something (e.g. create a recod)
    * A PUT requests needs a message body to give the source which is asked. It is meant for updating something (e.g. update a record)

- PATH OR ENDPOINT

    Where the resource is located.
- USED FOR

    It's a description for what this method is going to do 
- PARAMETERS

    Parameters required by the method
- ERROR / STATUS CODES

  For instance:
    * 200 OK <br />
    * 301 INVALID PARAMETERS <br />
    * 302 INCORRECT OR MISSING PARAMETERS <br />
    * 400 NO URL PROVIDED <br />
    * 404 NOT FOUND <br />
    * 405 METHOD NOT ALLOWED <br />
    * 500 INTERNAL SERVER ERROR <br />

### INSTALL POSTMAN
In order to send message bodies for a POST, you can do it either from terminal, using curl, or with IDE, like Postman.

Intall Postman in Ubuntu running in the terminal the following commands:
```
wget https://dl.pstmn.io/download/latest/linux64 -O postman.tar.gz
sudo tar -xzf postman.tar.gz -C /opt
rm postman.tar.gz
sudo ln -s /opt/Postman/Postman /usr/bin/postman
```
### Install additional dependencies (optionally needed)

```
sudo apt-get install ca-certificates fonts-liberation libappindicator3-1 libasound2t64 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils

sudo apt install libsecret-1-dev
```
then launch the command:

```
postman
```

If you get the error "Could not get the lock, quitting", kill running postman before relaunching:
```
pkill -fi Postman
```

## RESTFul APIs

RESTFUL APIs are API based on http (web) requests and responses

# DOCKER

A DOCKER ENGINE is an abstraction layer between applications and the Operating System

A Docker Engine can host several applications.

Applications are called CONTAINER, because they can actually host really application or simple services like a database.

IMAGES are the instructions to create the container, including the operating system, the language, the dependencies etc. So images indicate how the environment should look like. 

Images must be created for each application (or container).

Docke-Compose is useful to handle multiple containers and to make containers communicate with the others. 

## Install Docker locally

See: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository

1. Set up Docker's apt repository.
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

1. Set up Docker's apt repository.
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

```
2. Install the Docker packages.

```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

3. Verify that the installation is successful by running the hello-world image:
```
sudo docker run hello-world
```

If you don't want to preface the docker command with sudo, create a Unix group called docker and add users to it. When the Docker daemon starts, it creates a Unix socket accessible by members of the docker group. On some Linux distributions, the system automatically creates this group when installing Docker Engine using a package manager. In that case, there is no need for you to manually create the group.

https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user

4. Add your user to the docker group.
```
sudo usermod -aG docker $USER
```
Log out and log back in so that your group membership is re-evaluated.
Verify that you can run docker commands without sudo.

```
docker run hello-world
```

### Docker Hub

On Docker Hub you can find pre-existing docker images: https://hub.docker.com/

### Dockerfile and dependencies

From the terminal in the web folder run:
```
sudo touch Dockerfile
```
Tne save. In case of permission denied errors while saving, do:
```
sudo chmod 777 -R folder
```

Then type in the terminal:
```
sudo touch requirements.txt
```

Docker file explaination:

```
#take python 3 + ubuntu OS image
FROM python:3 
# crate a working directry named app at this path
WORKDIR /usr/src/app 
# copy the requirements file into the current working directory
COPY requirements.txt . 
#install requirements
RUN pip install --no-cache-dir -r  requirements.txt 
# copy the app file and the requirements file into the current working directory
COPY . . 
# run python app.py
CMD ["python", "app.py"]
```

### Docker-compose
At the main folder lever create the **docker-compose.yaml** file:
```
sudo touch docker-compose.yaml
```

Build container(s) for the first time:
```
sudo docker-compose build --no-cache
```

In case of command not found error on the previous command, run:
```
sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```
And check with:
```
docker-compose --version
```

After the building process is completed, run:
```
sudo docker-compose up
```
Whit above command, Docker runs your container in the foreground, meaning you’ll see all the logs and outputs directly in your terminal. If you close the terminal, the container stops running.
If you want the container to keep running even after you close the terminal, you can run it in detached mode using:
```
sudo docker-compose up -d
```
In case of error with previous building, before rebuilding do:
```
docker system prune
```
What docker system prune does:
- Removes unused containers: Stopped containers that aren't part of a running service or a network.
- Removes unused networks: Networks not associated with any containers.
- Removes dangling images: Images that are no longer tagged or are orphaned (i.e., not associated with any container).
- Removes dangling build cache: Unused build cache files.
- By default, does not remove volumes, but you can add --volumes to include them.

In case of error on already allocated port, it may be that another container is running on the same port, so do:
```
docker container ls
docker rm -f <container-id>
```
Stop and remove old containers and volumes
```
docker-compose down -v  
```
When you run docker-compose down, it:
- Stops all running services (containers) created by the docker-compose.yml.
- Removes the containers associated with the Compose project.
- Removes any networks created by docker-compose up.
When you add the -v flag (docker-compose down -v):
- It also removes the volumes that were created by Compose.

Stop the Background Container with the commands:
```
docker stop mycontainer
docker rm mycontainer
```
Rebuild and restart
```
docker-compose up --build 
```
Check a container:
```
docker inspect <container_id>
# To see if app is a bind mount:
#Find the "Mounts" section and look for "Source": "/your/local/path" → "Destination": "/app".
#If it's missing, check your docker-compose.yml again.
#or
docker-compose exec app ls -l /app # check if you see your app.py and other files.
```

# Mongo DB
## Install MongoDB with Docker

```
sudo docker run -d p 27017:27017 --name=mongo-example mongo:latest
```
See running container:
```
docker ps
```
Access the container:
```
sudo docker exec -it mongo-example bash
```
Call mongo servicedb:
```
mongosh
```

By default the "test" db is created. Useful inspection commands:
```
db.help()
db.stats()
db.version()
```

Create and delete a db:
```
# rename test into mydb or use another db
use mydb 
#display the current db name
db 
# it does not display anything until at least a record is created
show dbs
# insert a record (document)
db.movie.insert({"name":"Titanic"})
#delete the current database
db.dropDatabase() 
```

Create and delete a collection:
```
#create
db.createCollection("mycollection") 

db.createCollection("mybigcollection", {capped:true, autoIndexId: true, size: 6142800, max: 1000})
# capped means a fixed size collection
# size is the max size in bytes for a capped collection, it must be specified if capped is true
# max specifies the max number of documents (rows)
# autoIndexId automatically creates an index on _id field

#create and insert in 1 command
db.magicalCollection.insert({"name": "Pippo!"}) 

# see collections
show collections

#drop collection
db.mybigcollection.drop()
```

Data types in a Mongo DB: 
- string
- integer
- boolean
- double
- min / max keys
- arrays
- timestamp
- object
- null
- symbol (specific languages)
- date
- object ID
- binary data
- code (JavaScript)
- regexuse 

Insert a document:
```
use mycollection
db.mycollection.insert({ title: "MongoDb Overview", description: "My Mongo DB nosql database", tags: ["mongodb", "database", "nosql"], likes: 100 })

db.mycollection.insertMany([{ title: "MongoDb Overview", description: "My Mongo DB nosql database", tags: ["mongodb", "database", "nosql"], likes: 100 }, { title: "OpenSearch Overview", description: "My Opensearch DB nosql database", tags: ["opensearch", "database", "nosql"], likes: 200 }])
```

Query documents:
```
# display the first document
db.mycollection.find({}).pretty() #findOne({})

# equal to  
db.mycollection.find({"title": "MongoDb Overview"}).pretty()

#less then
db.mycollection.find({"likes": {$lt:150}}).pretty()

#less then or equal to
db.mycollection.find({"likes": {$lte:100}}).pretty()

#greater then
db.mycollection.find({"likes": {$gt:150}}).pretty()

#greater then or equal to
db.mycollection.find({"likes": {$gte:100}}).pretty()

#not equal to
db.mycollection.find({"likes": {$ne:90}}).pretty()

# and 
db.mycollection.find({$and: [{"likes": {$gt:90}}, {"likes": {$lt:200}}]}).pretty()

# or 
db.mycollection.find({$or: [{"likes": {$lt:30}}, {"title": "MongoDb Overview"}]}).pretty()
 
# update (inplace replacement) - single document
db.mycollection.update({"title": "MongoDb Overview"}, {$set: {"title": "New MongoDb Overview"}})
# update (inplace replacement) - multiple document
db.mycollection.update({"title": "MongoDb Overview"}, {$set: {"title": "New MongoDb Overview"}}, {multi:true})
db.mycollection.find({})
# save (replace the document)

# As of today insert and update methods are deprecated and have been replaced by insert_one and update_one

# remove a document
db.mycollection.remove({"title": "New MongoDb Overview"})

# projections: return with 1 only the wanted fields
db.mycollection.find({}, {"title":1,"_id":0})

# limiting records
db.mycollection.find({}).limit(1)

#sort records in asending order
db.mycollection.find({}).sort({"likes":1})

#sort records in descending order
db.mycollection.find({}).sort({"likes":-1})
```

# Encrypting app passwords

Generate and hased password, in the terminal:

```
pip install bcrypt
python3
import bcrypt
hashed = bcrypt.hashpw("123xyz".encode('utf8'), bcrypt.gensalt())
bcrypt.hashpw("123xyz".encode('utf8'), hashed)==hashed # this should give True
```