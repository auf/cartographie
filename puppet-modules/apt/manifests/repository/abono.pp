# = Class: apt::abono
#
# Include abono repository for rsyslog
class apt::repository::abono (
  $stage = pre
){
  apt::repo { "abono": 
    url => "http://ppa.launchpad.net/a.bono/rsyslog/ubuntu", 
    append_lsbdistcodename => true, 
    section => 'main' 
  }
  apt::key { "abono": keyid => 'C0061A4A' }
}
