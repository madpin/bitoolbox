# Arquivo de ajuda para lidar com a VM Python

Endereço:
http://vm-tmb-bi01.servers


```
export REPO=package
mkdir -p /data/python/$REPO
mkdir -p /data/git.repos/$REPO.git
cd /data/git.repos/$REPO.git

git init --bare
cd hooks

cat >post-receive <<EOL
#!/bin/bash
TRAGET="/data/python/extensions"
GIT_DIR="/data/git.repos/$REPO.git"
BRANCH="master"

while read oldrev newrev ref
do
    # only checking out the master (or whatever branch you would like to deploy)
    if [[ \$ref = refs/heads/\$BRANCH ]];
    then
        echo "Ref \$ref received. Deploying \${BRANCH} branch to production..."
        git --work-tree=\$TRAGET --git-dir=\$GIT_DIR checkout -f
    else
        echo "Ref $ref received. Doing nothing: only the \${BRANCH} branch may be deployed on this server."
    fi
done
EOL

chmod +x post-receive

```

Precisa subistituir esse: $REPO
ssh://thiagopinto@vm-tmb-bi01.servers/data/git.repos/$REPO.git
