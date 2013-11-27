AUF - Cartographie des formations
===

Comment construire le projet
---

1.a Rouler les commandes suivantes:

    $ git clone https://github.com/auf/cartographie.git
    $ cd cartographie
    $ python bootstrap.py
    $ bin/buildout -c devel.cfg

Si la commande `bin/buildout` échoue avec le message d'erreur:

    AttributeError: 'NoneType' object has no attribute 'location'

1.b nettoyez le projet, puis installez un virtualenv ainsi que distribute:

    $ rm -rf rm -rf bin/ develop-eggs/ eggs/ lib/ parts/
    $ virtualenv2 --distribute .
    $ pip install distribute
    $ python bootstrap.py
    $ bin/buildout -c devel.cfg

2. Créer le fichier conf.py à partir de conf.py.edit et y copier les
informations de connexion à la BD

    $ cd cartographie
    $ cp conf.py.edit conf.py

    # base de données mysql
    # user: root
    # pwd:

Comment synchroniser la base de données avec les Models
---

    $ bin/django syncdb --migrate

Comment importer les données pour la base de données *datamaster*
---

    $ mysql -h localhost -u root datamaster < mysql-dumps/datamaster.sql

Comment ajouter les utilisateurs de l'AUF dans la table des users django
---

    $ bin/django import_auf_employees

Comment créer les données de configuration de base pour les fiches formation
---

    $ bin/django import_config_models

Créer les jetons d'accès (token) pour tous les établissements membres de l'AUF
---

    $ bin/django jetonizer

Comment rouler le server Django de dév.
---

    $ bin/django runserver

Comment rouler le server Django de dév. dans une VM Vagrant
---

    $ bin/django runserver [::]:8000

Cela indique à Django de permettre les connexions de n'importe où sur le réseau
actuel

Exécuter les tests de l'app
---

Il existe des TestCases pour les commandes propres à l'app

    $ bin/django test formation

La gestion des CSS de l'app Formation
---

LessCSS est utilisé pour rassembler le CSS de Twitter Bootstrap en un seul
fichier.

**Installation de ces dépendances**

    $ apt-get install ruby-full rubygems
    $ gem install therubyracer
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
