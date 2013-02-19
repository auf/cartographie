# = Class: apt::gosa
#
# Include gosa repository
class apt::gosa inherits apt::main {
	apt::repo { "gosa": url => 'http://oss.gonicus.de/pub/gosa/debian-lenny/', append_lsbdistcodename => false, section => './' }
}

