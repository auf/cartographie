# = Class: apt::reductivelabs
#
# Include Reductive Labs to our repository list
class apt::puppetlabs inherits apt {
	apt::repo { 'puppetlabs': url  => "http://apt.puppetlabs.com/ubuntu", section => 'main' }
	apt::key { 'puppetlabs': keyid  => "4BD6EC30", ensure => present }
}

