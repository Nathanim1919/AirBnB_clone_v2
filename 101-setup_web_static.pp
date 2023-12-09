# Setup web server for deployment

exec { 'apt-get update':
  path => '/usr/bin:/bin',
}

package { 'nginx':
  ensure => installed,
}

exec { 'mkdirs':
  command => 'mkdir -p "/data/web_static/shared/" "/data/web_static/releases/test/"',
  path    => '/usr/bin:/bin',
}

file { 'test_index_file':
  ensure  => file,
  path    => '/data/web_static/releases/test/index.html',
  content => "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>",
  mode    => '0644',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => Exec['mkdirs'],
}

$link='/data/web_static/current'
exec { 'link_&_ownership':
  command => "rm ${link}",
  path    => '/usr/bin:/bin',
  require => Exec['mkdirs'],
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/'
}

exec { 'chown -R ubuntu:ubuntu /data/':
  path => ['/usr/bin', '/bin'],
}

$location='\n\tlocation /hbnb_static {\n\
        \talias /data/web_static/current/;\n\
        }'
exec { 'edit_config_file':
  command => "sudo sed -i '/server_name _;/a \\ ${location}' /etc/nginx/sites-available/default",
  path    => '/usr/bin:/bin',
}

exec { 'restart_Nginx':
  command => 'sudo service nginx restart > /dev/null',
  path    => '/usr/bin:/bin',
}
