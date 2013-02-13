Explication de la présence de dossiers non communs à un projet Django
=====================================================================

viewModels
----------

C'est une class qui fait le lien entre la *view* et le *template*. Elle contient
les données qui seront utilisés dans le template.

L'idée est d'amincir nos *views* pour qu'on puisse y voir la logique d'affaire
d'un seul coup d'oeil.

Le *viewModel* s'occupe des points suivants:

* d'obtenir les données des *models*
* de les formater selon les nécessités du *template*

Cette séparation permet de réutiliser des *viewModels* dans d'autres *views*
lorsque nécessaire.

Elle pertmet également d'écrire des UnitTests spécifiques à l'obtention et
au formatage des données.

Références *Model-View-ViewModel*: http://en.wikipedia.org/wiki/Model_View_ViewModel