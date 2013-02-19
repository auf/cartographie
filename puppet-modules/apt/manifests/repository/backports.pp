# = Class: apt::backports
#
# Dell OMreport, cf http://linux.dell.com/repo/community/deb/latest/
class apt::dellom inherits apt {
    apt::repo { "dellom": url => "http://linux.dell.com/repo/community/deb/OMSA_6.3/", append_lsbdistcodename=> false, section => '/' }
}

