# = Class: apt::medibuntu
#
# Include medibuntu to our repository list
class apt::medibuntu inherits apt {
	apt::repo { "medibuntu": url => "http://packages.medibuntu.org", section => 'free non-free' }
	apt::key { "medibuntu": keyid  => "0C5A2783", ensure => present, }
}

