Webhop - PHP7 Ansible Role
==========================

Installs the latest PHP7 and associated packages on an ubuntu host.
Automatically dimension max_children limit on startup time.

## Role Variables

##### Defaults

- `php_version` - The version of PHP to install. (**7.2**)
- `php_post_max_size` - Max size (in Mb) for POST requests. (**30**)
- `php_upload_max_filesize` - Max size (in Mb) for uploads. (**30**)
- `php_pm_max_children` - FPM max children. (**10**)
- `create_virtualenv` - Create a virtualenv (**true**)
- `scripts_dir` - Path to install scripts into (**/opt/beamly/scripts**)
- `virtualenv_dir` - Path to create virtualenv in (**/opt/beamly/virtualenvs**)
- `scripts_owner` - User to chown the scripts (**ubuntu**)
- `scripts_group` - Group to chown the scripts (**ubuntu**)
- `fpm_total_ram_slice` - Ratio/slice of memory allocated to PHP-FPM (**0.4**)
- `fpm_confpath` - PHP-FPM configuration file path (**/etc/php/7.2/fpm/pool.d/www.conf**)
- `fpm_avgmem` - Average memory footprint of a PHP-FPM child thread (**128**)
- `enable_fpm_stats` - Enables the fpm status endpoint (**true**)
- `php_pm_status_path` - Endpoint to expose fpm stats on (**/fpm-status**)

Usage
-----

```yaml
roles:
    - { role: webhop.php7, fpm_avgmem: 90 }
```

To enable FPM stats:

```yaml
roles:
    - { role; webhop.php7, enable_fpm_stats: True }
```

**Note** - You will also need to add the following snippet to your apache vhost (or nginx equivalent) to expose the status endpoint:

```text
<LocationMatch '/fpm-status'>
    SetHandler php7-fcgi-virt
    Action php7-fcgi-virt /php7-fcgi virtual
</LocationMatch>

```

Author Information
-------------------

* Chris Warren - chris@beamly.com
* Neil Saunders - neil@beamly.com
* Mariano Barcia - mariano.barcia@beamly.com
* Vik Bhatti - vik@beamly.com
