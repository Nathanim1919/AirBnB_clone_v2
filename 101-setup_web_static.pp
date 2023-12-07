# Setup web server for deployment
package { 'nginx':
  ensure => installed,
}

exec { 'mkdirs':
  command => 'mkdir -p "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/"'
  path    => '/usr/bin:/bin'
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
  mode    => '0664',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => Exec['mkdirs'],
}

$target='/data/web_static/releases/test/'
$link='/data/web_static/current'
exec { 'link_&_ownership':
  command => "rm ${link} && sudo ln -s ${target} ${link} && sudo chown -R ubuntu:ubuntu /data",
  path    => '/usr/bin:/bin',
  require => Exec['mkdirs'],
}

$location="\n\tlocation /hbnb_static {\n\
\t\talias /data/web_static/current/;\n\t}"
exec { 'edit_config_file':
  command => "sudo sed -i \"/server_name _;/a \\ ${location}\" /etc/nginx/sites-available/default",
  path    => '/usr/bin:/bin',
}

exec { 'restart_Nginx':
  command => 'sudo service nginx restart > /dev/null',
  path    => '/usr/bin:/bin',
}
