class csync2::key (
  $keyfile = 'puppet:///files/csync2/csync2.key'
  ) {
	file { '/etc/csync2.key' :
			source	=>  $keyfile,
			ensure	=> file,
			mode	=> 600,
			require	=> Class['csync2::install'],
	}
}
