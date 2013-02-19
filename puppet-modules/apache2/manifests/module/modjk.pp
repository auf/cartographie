#
# To serve mod_jk:
# - workers could be set (by default: ["localhost"] )
# - this class (apache2::module::modjk) has to be include
# - the website must define the jkmountfile (like "/etc/libapache2-mod-jk/uriworkermap.properties")
# - the file "/etc/libapache2-mod-jk/uriworkermap.properties" must contains the url, like "/toto/*=loadbalancer\n"
#
class apache2::module::modjk inherits apache2 {
    realize(Apache2::Module['jk'])
    if ! $workers { $workers=['localhost'] }
    file {
        "/etc/libapache2-mod-jk/workers.properties":
            path     => "/etc/libapache2-mod-jk/workers.properties",
            ensure   => file,
            checksum => md5,
            owner    => root,
            group    => root,
            mode     => '0644',
            content  => template("apache2/workers.properties.erb"),
            require => Package["libapache2-mod-jk"],
            notify  => Exec['reload-apache2']
    }
}