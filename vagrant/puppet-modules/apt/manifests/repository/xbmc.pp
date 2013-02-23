# = Class: apt::xbmc
#
# Include XBMC Team ppa
class apt::ppa::xbmc {
	apt::repo::ppa { "xbmc-ppa" : repo => 'team-xbmc/ppa'}
}

