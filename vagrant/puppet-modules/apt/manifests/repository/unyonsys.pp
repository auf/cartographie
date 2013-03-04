# = Class: apt::unyonsys
#
# Include ubuntu backports to our repository list
class apt::unyonsys inherits apt::main {
	apt::repo { "unyonsys": url => 'http://repository.unyonsys.com', section => 'main' }
}

