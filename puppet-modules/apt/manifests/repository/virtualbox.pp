# = Class: apt::virtualbox
#
# Include ubuntu virtualbox to our repository list
class apt::virtualbox inherits apt {
	apt::repo { "virtualbox": url  => "http://download.virtualbox.org/virtualbox/debian", section => 'contrib non-free' }
	apt::key { "virtualbox": keyid  => "6DFBCBAE", ensure => present }
}

