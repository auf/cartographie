# = Class: apt::kubuntu_ppa_backports
#
# Include kubuntu ppa backport to our repository list.
# Was used for Amarok 2.3.1 initialy
class apt::ppa::kubuntu_ppa_backports {
	apt::repo::ppa { "kubuntu-ppa-backports" : repo => 'kubuntu-ppa/backports'}
}

