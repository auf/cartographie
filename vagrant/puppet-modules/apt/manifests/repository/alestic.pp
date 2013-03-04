# = Class: apt::alestic
#
# Include alestic ppa to our repository list
class apt::ppa::alestic {
        apt::repo::ppa { "alestic" : repo => 'alestic'}
}

