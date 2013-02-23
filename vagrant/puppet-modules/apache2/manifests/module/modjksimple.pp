# To serve mod_jk:
# - apache2_modjksimple_worker ('localhost' by default) should point to hostname of the appserver
# - apache2_modjksimple_path ('/' by default) should point to the url set with jkmountfile
# - apache2_modjksimple_jkmountfile must be set to jkmountfile of the website (like "/etc/libapache2-mod-jk/uriworkermap.properties")
class apache2::module::modjksimple inherits apache2 {
  realize(Apache2::Module['jk'])
  if ! $apache2_modjksimple_worker { $apache2_modjksimple_worker='localhost' }
  if ! $apache2_modjksimple_path { $apache2_modjksimple_worker='/' }
  if ! $apache2_modjksimple_jkmountfile { $apache2_modjksimple_jkmountfile='/etc/libapache2-mod-jk/uriworkermap.properties' }

  file {
        "/etc/libapache2-mod-jk/workers.properties":
            path     => "/etc/libapache2-mod-jk/workers.properties",
            ensure   => file,
            owner    => root,
            group    => root,
            mode     => '0644',
            content  => "worker.list=appserver\nworker.appserver.type=ajp13\nworker.appserver.host=localhost\nworker.appserver.port=8009",
            require => Package["libapache2-mod-jk"],
            notify  => Exec['reload-apache2']
  }
  file {
        "$apache2_modjksimple_jkmountfile":
            path     => "/apache2_modjksimple_jkmountfile",
            ensure   => file,
            owner    => root,
            group    => root,
            mode     => '0644',
            content  => "$apache2_modjksimple_path/*=appserver",
            require => Package["libapache2-mod-jk"],
            notify  => Exec['reload-apache2']
  }
}