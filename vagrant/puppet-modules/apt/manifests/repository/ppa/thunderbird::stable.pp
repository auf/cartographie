# = Class: apt::ppa::thunderbird::stable
#
# Include thunderbird stable ppa
class apt::ppa::thunderbird::stable inherits apt {
	apt::repo::ppa { "thunderbirdstable": repo  => "mozillateam/thunderbird-stable" }
}

