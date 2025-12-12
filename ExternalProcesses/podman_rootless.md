# This part is only here if you want to run dockerized process through CWL in rootless environment

In my case I am in a podman rootless environment, so I will talk about that.
But it should also work in the case of rootless docker. 

If you are not rootless, you can skip this document, as it does not apply to you.

### Steps to configure examind for rootless

1. Create a `docker` file when you have your `docker-compose.yml`
2. Write this inside :
    ```bash
    #!/bin/sh
    
    # If the command is 'run', inject the security flag
    if [ "$1" = "run" ]; then
        shift
        # We call /usr/bin/docker (or /usr/bin/podman) assuming that is where the real binary lives
        # explicitly disable SELinux labeling for the sibling container
        exec /usr/bin/docker run --security-opt=label=disable "$@"
    else
        # Pass all other commands (pull, inspect, etc) through unchanged
        exec /usr/bin/docker "$@"
    fi
    ```
3. Run `chmod +x docker`
4. In the `docker-compose.yml`, add :
   - In volumes : (replace 5024 by your user id (`id` in terminal))
     ```yml
     - "./docker:/custom-bin/docker:ro"
     - "/run/user/5024/podman/podman.sock:/var/run/docker.sock:Z"
     ```
   - In environment :
      ```yml
      PATH: "/custom-bin:/usr/local/tomcat/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
   ```