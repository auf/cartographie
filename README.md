AUF - Cartographie des formations
===

Comment construire le projet
---

Rouler les commandes suivantes:

    $ git clone https://github.com/auf/cartographie.git
    $ cd cartographie
    $ python bootstrap.py
    $ bin/buildout -c devel.cfg

Créer fichier conf.py à partir de conf.py.edit et y copier les informations de connexion à la BD


Comment synchroniser la base de données avec les Models
---

    $ bin/django syncdb --migrate

Comment rouler le server Django de dév.
---

    $ bin/django runserver

Comment rouler le server Django de dév. dans une VM Vagrant
---

    $ bin/django runserver [::]:8000

Cela indique à Django de permettre les connexions de n'importe où sur le réseau actuel

Exécuter les tests de l'app
---

Il existe des TestCases pour les commandes propres à l'app

    $ bin/django test formation

La gestion des CSS de l'app Formation
---

LessCSS est utilisé pour rassembler le CSS de Twitter Bootstrap en un seul fichier.

**Installation de ces dépendances**

    $ apt-get install ruby-full rubygems
    $ gem install less

**Compilation d'un fichier .less**

    $ lessc -x fichier.less > fichier.css

Installation de Vagrant et démarrer la VM sous VirtualBox
---

1. Installer VirtualBox
2. Installer Vagrant

> $ sudo gem install vagrant vagrant-vbguest

3. Se rendre dans le dossier du projet cloner
4. Rouler la commande suivante pour créer la VM et la démarrer:

> $ vagrant up

5. Se connecter à la VM

> $ vagrant ssh

6. Vous devriez apercevoir le répertoire *cartographie* dans le home de la VM
7. Rouler buildout et hop !
