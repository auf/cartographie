AUF - Cartographie des formations
===

Comment construire le projet
---

> git clone https://github.com/auf/cartographie.git
> cd cartographie
> python bootstrap.py
> bin/buildout -c devel.cfg
> créer fichier conf.py à partir de conf.py.edit
> bin/django syncdb migrate
> bin/django runserver

La gestion des CSS de l'app Formation
---

LessCSS est utilisé pour rassembler le CSS de Twitter Bootstrap en un seul fichier.

**Installation de ces dépendances**

> [vous vous]$ apt-get install ruby-full rubygems
> [vous vous]$ gem install less

**Compilation d'un fichier .less**

> lessc -x fichier.less > fichier.css