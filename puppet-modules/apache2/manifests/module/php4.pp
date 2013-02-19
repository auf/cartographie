class apache2::module::php4 inherits apache2 {
	package { [ "php4", "php4-cli", "php4-gd", "php4-mysql", "php4-mcrypt", "php4-cgi" ] : ensure => present }
	package { [ "libapache2-mod-php4" ] : ensure => absent }

	realize(Apache2::Module['actions'])

	file { "${apache_root_path}/conf.d/php4-cgi.conf":
		ensure	=> file,
		mode	=> '0755',
		source	=> "puppet:///modules/apache2/php4-cgi.conf",
		require => Package['apache2'],
		notify	=> Exec['reload-apache2']
	}
}
