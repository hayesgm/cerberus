# cerberus

## Packer-based Provisioner for Automated Docker Deployments

Cerberus is a set of Cloud Images for automated Docker deployments.  A developer can run a Cerberus AMI, for instance, on AWS with user data specifying a Docker repo in the Docker index.  The Cerberus instance will automatically run the Docker repo on boot (via Upstart) and poll for updates to the image.  When the Docker image is updated in the Docker Index, that Cerberus instance will hot swap in the new build.

Example Flow:

1) Create new instance on AWS using Cerberus-provisioned AMI
2) In `user data` section, use: {"docker":{"repo":"dockerfile/redis",flags:["-p 6379:6379"]}}
3) Open port 6379 in the Security Group for the instance
4) Start the instance
5) When the instance has booted, visit: `http//<public-ip>:6379`

## User Data JSON Spec

```
{
  "docker": {
    "repo": "<docker repo>",
    "flags": ["<docker run flag>"]
    "auth": "<base64 encoded docker auth>",
    "email": "<docker email for auth>",
  },

  "notifications": {
    "rest": "<http endpoint>",
    "hipchat": { "token": "<hipchat api token>", "room": "<hipchat room id>"}
  },

  "init": "#!/bin/bash
    echo 'My bash script'
  "
}
```

### Building an Image

To build an AMI, simply run: `packer build packer.json`.  This will assume you have AWS keys to build and AMI (which you will be charged for on your account).

### Public AMI Builds

TODO

