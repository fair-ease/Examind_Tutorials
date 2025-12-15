---
title: Configure Examind for CWL Processes
---

To run CWL processes in Examind, you need to configure and edit some configuration files, Docker images, and docker compose files.

### A. Dockerfile of Examind-Community

First we need to install cwltool and cwl-runner inside the Examind-Community Docker image.

The Dockerfile is located in this folder in the Examind Community repository:
`examind-community/modules/bundles/exa-bundle/src/docker`

```dockerfile
# previous content of the Dockerfile
# > LABEL description="Docker image of Examind Community"

# Lines to add
RUN apt-get update && \
    apt-get install -y python3 python3-pip docker.io && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir cwltool --break-system-packages && \
    pip3 install --no-cache-dir cwlref-runner --break-system-packages

# next content of the Dockerfile
# > COPY ./examind /usr/local/tomcat/webapps/examind
```

### B. Edit setenv.sh

Next we need to edit the `setenv.sh`

The setenv.sh is located in this folder in the Examind Community repository:
`examind-community/modules/bundles/exa-bundle/src/docker/conf/tomcat/bin`

Add this at the end of the file `setenv.sh`:
```bash
JAVA_OPTS="${JAVA_OPTS} --add-opens java.base/java.net=ALL-UNNAMED"
export JAVA_OPTS
```

### C. Edit the docker-compose.yml

Finally, we need to edit the `docker-compose.yml` file.

The docker-compose is located in this folder in the Examind Community repository:
`/examind-community/docker`

**If you are using docker in root mode**, you can add the following volume to the examind service:
```yaml
    volumes:
       - "/var/run/docker.sock:/var/run/docker.sock"
       - "/usr/bin/docker:/usr/bin/docker"
```

**If you are using podman in rootless mode** , you can add the following volume to the examind service (cf : [Podman Rootless Conf](./podman_rootless.md)):
```yaml
    volumes:
         - "/run/user/<num_user>/podman/podman.sock:/var/run/docker.sock"
```
*Replace `<num_user>` by your user id (you can get it by running the command `id -u` in a terminal)*

---

Always in the volume section you have to add a volume for the CWL processes. This volume have to point a folder with the same path inside and outside the container.
Example for me :
```yaml
    volumes:
       - "/home/qbialota/.local/share/exa-cwl-shared:/home/qbialota/.local/share/exa-cwl-shared"
```

**Warning** : If you are on SELinux system (like Fedora, CentOS, RHEL...), you have to add the option `:z` at the end of the volume path to avoid permission issues.
Example for me on SELinux system :
```yaml
    volumes:
       - "/home/qbialota/.local/share/exa-cwl-shared:/home/qbialota/.local/share/exa-cwl-shared:Z"
       - "/run/user/<num_user>/podman/podman.sock:/var/run/docker.sock:Z"
```

---

Finaly you have to set an environment variable with the same path as the volume for CWL processes.
Example for me :
```yaml
  EXAMIND_CWL_SHARED_DIR: "/home/qbialota/.local/share/exa-cwl-shared"
```

### D. Build examind-community

To build examind-community with the modified Dockerfile, you have to run the following command at the root of the examind-community repository:
```bash
mvn install -DskipTests -Pdocker -f pom.xml
```