# = Class: rsyslog::common
#
# * Installs the rsyslog package
#
# === Parameters:
#
# None.
# Class: rsyslog::common
# install rsyslog package
#
class rsyslog::common {
    if ($lsbdistcodename == 'hardy') {
		include apt::abono
		package { 'rsyslog': 
			ensure => latest,
			require => Class["apt::abono"]
		} 
		#fake upstart dependency (for logrotate and stuff)
		file { '/usr/local/sbin/reload':
			ensure => present,
			mode => '755',
			owner => 'root',
			group => 'root',
			content => "#!/bin/bash\n#Script to simulate upstart compatibility.\n/etc/init.d/\$1 reload\n"
		}

	} else {
		package { 'rsyslog': ensure => present }
	}

	service { 'rsyslog':
		ensure		=> running,
		enable		=> true,
		hasrestart	=> true,
	}
}

# = Class: rsyslog::client
#
# * Configures rsyslog as a client for sending logs to a centralised rsyslog server
#
# === Parameters:
#
# $rsyslog_server:: The server hostname/ip address [default: localhost]
# $rsyslog_send_everything:: If set to yes, every log (*.*) is sent. Else, by default, only the auth.* is sent.
#
class rsyslog::client inherits rsyslog::common {
	if ! $rsyslog_server { $rsyslog_server = "localhost" }
	file { "/etc/rsyslog.d/send-remote-logs.conf" :
                ensure	=> file,
                group	=> root,
		owner	=> root,
		content	=> template("rsyslog/send-remote-logs.erb"),
		notify	=> Service['rsyslog'],
		require	=> Package['rsyslog'],
        }

	@@file { "${hostname}_rsyslog_remote":
        path	=> "/etc/rsyslog.d/20-${hostname}.remote.conf",
        ensure	=> present,
        group	=> root,
        owner	=> root,
		tag  	=> "rsyslog::client::${environment}",
        content	=> template("rsyslog/receive-remote-logs.erb"),
        notify	=> Service['rsyslog'],
        require	=> Package['rsyslog']
	}
}
	
# = Class: rsyslog::server
#
# * Configures rsyslog as a centralised server for receiving logs
#
# === Parameters:
#
# none
#
class rsyslog::server inherits rsyslog::common {
	
    file { "/etc/rsyslog.conf" :
        ensure  => file,
        group   => root,
        owner   => root,
        source  => "puppet:///modules/rsyslog/rsyslog.conf",
        notify  => Service['rsyslog'],
        require => Package['rsyslog'],
        }
	
    file { "/etc/logrotate.d/rsyslog-remote" :
                ensure  => file,
				mode => 755,
                group => root,
        owner => root,
        source => "puppet:///modules/rsyslog/rsyslog-remote",
        }

	File <<| tag == "rsyslog::client::${environment}" |>> {
	}
}
	
