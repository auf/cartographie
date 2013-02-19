# = Class: apt::ppa::winhq
#
# Include winehq ppa - These are dev release and should be considered as such
class apt::ppa::winehq {
	apt::repo::ppa { "winehq" : repo => 'ubuntu-wine/ppa'}
}

