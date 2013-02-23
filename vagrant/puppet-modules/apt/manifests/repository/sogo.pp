# = Class: apt::sogo
#
# Include sogo repository
class apt::sogo inherits apt::main {
	apt::repo { "sogo": url => 'http://inverse.ca/ubuntu', section => 'main' }
}

