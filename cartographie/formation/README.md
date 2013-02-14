App Formation
=============

Application de création et d'édition de fiche de formation pour les établissements membre de l'AUF.

Explication de la présence de dossiers non communs à un projet Django
---------------------------------------------------------------------

data
####

Ce dossier contient les CSVs de données de configuration initial pour les formations. Les *Models* qui sont utilisés pour peupler la base de données
se retrouvent dans le fichier */formation/models/configuration.py*

viewModels
##########

C'est une class qui fait le lien entre la *view* et le *template*.

L'idée est d'amincir nos *views* pour qu'on puisse y voir la logique d'affaire
d'un seul coup d'oeil.

Les rôles du *viewModel* sont:

* d'obtenir les données des *models*
* et de les formater selon les nécessités du *template*

Cette séparation permet de réutiliser des *viewModels* dans d'autres *views*
lorsque nécessaire.

Elle permet également d'écrire des UnitTests spécifiques à l'obtention et
au formatage des données.

Références *Model-View-ViewModel*: http://en.wikipedia.org/wiki/Model_View_ViewModel