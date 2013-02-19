# Variable $configclasses is for dependencies (subscribe service).
# Change it if you are not using all the config classes (or your own)
class shinken::server (
  $configclasses = [
    'shinken::config',
    'shinken::config::notificationcommands',
    'shinken::config::commands',
    'shinken::config::hostgroups',
    'shinken::config::servicegroups',
    'shinken::config::timeperiods',
    'shinken::config::contacts',
    'shinken::config::contactgroups'
  ] ) {
    
  include shinken::variables
  
  service { 'shinken':
    ensure    => running,
    require   => Class['shinken::install'],
  }
  
  service { 'shinken-arbiter':
    ensure    => running,
    require   => Class['shinken::install'],
    subscribe => Class[$configclasses]
  } 
}
