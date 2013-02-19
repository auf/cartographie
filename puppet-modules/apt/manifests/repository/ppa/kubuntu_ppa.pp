# = Class: apt::kubuntu_ppa
#
# Include kubuntu ppa to our repository list.
# Mainly used to get an up to date KDE version (stable)
class apt::ppa::kubuntu_ppa {
	apt::repo::ppa { "kubuntu-ppa" : repo => 'kubuntu-ppa/ppa'}
}

