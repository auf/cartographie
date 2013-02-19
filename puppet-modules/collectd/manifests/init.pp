# Class: collectd::server
#
# This class installs and configures the collectd server
#
class collectd::common {
	if ! $collectd_log_level { $collectd_log_level = 'error' }
	package { [ 'collectd', 'collectd-utils' ]: ensure => present }

	service { 'collectd':
		ensure		=> running,
		enable		=> true,
		hasrestart	=> true,
		hasstatus	=> true,
		require		=> Package['collectd'];
	}

	file { '/etc/collectd/collectd.conf':
		ensure	=> file,
		content => template('collectd/collectd.conf.erb'),
		require => Package['collectd'],
		notify	=> Service['collectd']
	}

	file { '/etc/collectd/conf.d':
		ensure	=> directory,
		recurse	=> true,
		purge	=> true,
		require => Package['collectd'],
		notify	=> Service['collectd']
	}

	file { '/etc/logrotate.d/collectd':
			ensure	=> file,
			mode	=> 0644,
			source	=> 'puppet:///modules/collectd/logrotate-collectd'
	}
}



class collectd::plugins::network (
	$collectd_server_hostname
) {
  file { "/etc/collectd/conf.d/$order-${prefix}network.conf":
	ensure	=> file,
	content	=> template("collectd/plugins/network.conf.erb"),
	notify	=> Service['collectd'],
	require	=> Package['collectd']
  }
}



class collectd::plugins::hddtemp {
	package { 'hddtemp': ensure => present }

	file { "/etc/default/hddtemp":
		ensure	=> file,
		source	=> "puppet:///modules/collectd/plugins/hddtemp",
		require	=> Package['hddtemp'],
		notify	=> Service['hddtemp']
	}

	service { 'hddtemp':
		ensure		=> running,
		enable		=> true,
		hasrestart	=> true,
		hasstatus	=> false,
		pattern		=> 'hddtemp',
		require		=> Package['hddtemp']
	}

	collectd::plugin { 'hddtemp': }
}



define collectd::plugin($collectd_template = false, $order = 50, $prefix = '', $interface = false) {
	if ! $collectd_template { $conf_file = $name } else { $conf_file = $collectd_template }

	if $collectd_template == 'network_server' {
		$thisinterface = inline_template("<% if has_variable?('ipaddress_${name}') %><%= ipaddress_${name} %><% end %>")
	}

	file { "/etc/collectd/conf.d/$order-${prefix}${name}.conf":
		ensure	=> file,
		content	=> template("collectd/plugins/${conf_file}.conf.erb"),
		notify	=> Service['collectd'],
		require	=> Package['collectd']
	}
}



class collectd::client(
	$collectd_server_hostname
) {
	include collectd::common
	class {"collectd::plugins::network":
		collectd_server_hostname => $collectd_server_hostname
	}
	collectd::plugin { 'rrdtool': }
	collectd::plugin { 'cpu': }
	collectd::plugin { 'load': }
	collectd::plugin { 'memory': }
	collectd::plugin { 'swap': }
	collectd::plugin { 'interface': }

	if ! $ec2_instance_id and $productname != "VMware Virtual Platform" and $productname != "VirtualBox" and $productname != "Bochs" {
		include collectd::plugins::hddtemp
	}
}



class collectd::server {
	class {"collectd::client":
		collectd_server_hostname => "localhost"
	}
	$array_of_interfaces = split($interfaces, ',')

	collectd::plugin { $array_of_interfaces: collectd_template => 'network_server', order => 30 }

#	class defaultwebsite inherits apache2 {
#		include role::server::web
#		apache2::website { "collectdgraph.${domain}": client => "${client}", site_domain => "${domain}", confname => "collectdgraph", required_modules => ['php5'], documentroot_source => 'puppet:///modules/collectd/interface/collectd_graph_panel', apache2_allowoverride => ['AuthConfig', 'Limit'], has_awstats => false }
#	}
}
