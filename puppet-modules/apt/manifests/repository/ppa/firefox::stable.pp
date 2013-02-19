# = Class: apt::ppa::firefox::stable
#
# Include firefox stable ppa
class apt::ppa::firefox::stable inherits apt {
	apt::repo::ppa { "firefoxstable": repo  => "mozillateam/firefox-stable" }
}

