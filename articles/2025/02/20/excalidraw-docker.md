---
title: Installation excalidraw
date: 2025-02-20
tags: Docker, linux, logiciel
abstract: Tuto rapide sur comment installer excalidraw via Docker pour une utilisation locale
---

Excalidraw est un excellent logiciel permettant de rapidement faire des dessins techniques. Il est simple et intuitif.
L'url officielle est https://excalidraw.com

On peut réaliser une installation locale via docker.

# Installer docker
## Installer la clé docker
hello1
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
hello2
## Ajouter docker dans les sources pour apt
```bash
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
## Installer docker
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
## Pour utiliser docker sans être root
```bash
sudo usermod -aG docker $USER
```
Redemarrer

# Installer excalidraw via docker
Téléchargement de l'image docker
```bash
docker pull excalidraw/excalidraw:latest
```

Création et démarrage du container :
```bash
docker run -d -p 8768:80 --name excalidraw excalidraw/excalidraw:latest
```
Excalidraw est maintenant accessible en local sur le port 8888

# Arrêt / marche
Pour arrêter le container
```bash
docker stop excalidraw-instance
```

Pour démarrer le container
```bash
docker start excalidraw-instance
```
Lancer un navigateur sur http://localhost:8768/

Pour vérifier que le container est running
```bash
docker ps
CONTAINER ID   IMAGE                          COMMAND                  CREATED         STATUS                            PORTS                                     NAMES
26c80ff5278d   excalidraw/excalidraw:latest   "/docker-entrypoint.…"   2 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:8768->80/tcp, [::]:8768->80/tcp   excalidraw
```
