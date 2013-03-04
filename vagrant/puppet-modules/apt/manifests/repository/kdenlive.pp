# = Class: apt::kdenlive
#
# Include kdenlive ppa to our repository list
class apt::ppa::kdenlive {
	apt::repo::ppa { "kdenlive" : repo => 'sunab/sunab2'}
}

