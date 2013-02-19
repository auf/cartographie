# internal class: do not use directly
class apache2::variables {
  case $::osfamily {
    'Debian': {
      $apache_package_name = 'apache2'
      $apache_service_name = 'apache2'
      $apache_root_path = '/etc/apache2'
      $apache_log_path = '/var/log/apache2'
      $apache_doc_path = '/var/www'
      $apache_user = 'www-data'
      $apache_group = 'www-data'
      $apache_log_group = 'adm'
    }
    'RedHat': {
      $apache_package_name = 'httpd'
      $apache_service_name = 'httpd'
      $apache_root_path = '/etc/httpd'
      $apache_log_path = '/var/log/httpd'
      $apache_doc_path = '/var/www/vhosts'
      $apache_user = 'apache'
      $apache_group = 'apache'
      $apache_log_group = 'root'
    }
    default: {
      fail('Unsupported OS')
    }

  }
  $logrotate_conf_path  = '/etc/logrotate.d'
}
