#global git 605247a3e219f0ebf43beee3b37ec6af41d1eba4

Name:           php-fkooman-sqlite-migrate
Version:        0.1.1
Release:        3%{?dist}
Summary:        Simple SQLite Migrations

License:        MIT
URL:            https://software.tuxed.net/php-sqlite-migrate
%if %{defined git}
Source0:        https://git.tuxed.net/fkooman/php-sqlite-migrate/snapshot/php-sqlite-migrate-%{git}.tar.xz
%else
Source0:        https://software.tuxed.net/php-sqlite-migrate/files/php-sqlite-migrate-%{version}.tar.xz
Source1:        https://software.tuxed.net/php-sqlite-migrate/files/php-sqlite-migrate-%{version}.tar.xz.asc
Source2:        gpgkey-6237BAF1418A907DAA98EAA79C5EDD645A571EB2
%endif

BuildArch:      noarch

BuildRequires:  gnupg2
BuildRequires:  php-fedora-autoloader-devel
BuildRequires:  %{_bindir}/phpab
#    "require-dev": {
#        "phpunit/phpunit": "^4|^5|^6|^7"
#    },
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
BuildRequires:  phpunit7
%global phpunit %{_bindir}/phpunit7
%else
BuildRequires:  phpunit
%global phpunit %{_bindir}/phpunit
%endif
#    "require": {
#        "ext-pcre": "*",
#        "ext-pdo": "*",
#        "ext-spl": "*",
#        "php": ">= 5.4"
#    },
BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-pcre
BuildRequires:  php-pdo
BuildRequires:  php-spl

#    "require": {
#        "ext-pcre": "*",
#        "ext-pdo": "*",
#        "ext-spl": "*",
#        "php": ">= 5.4"
#    },
Requires:       php(language) >= 5.4.0
Requires:       php-pcre
Requires:       php-pdo
Requires:       php-spl

Provides:       php-composer(fkooman/sqlite-migrate) = %{version}

%description
Library written in PHP that can assist with SQLite database migrations.

%prep
%if %{defined git}
%autosetup -n php-sqlite-migrate-%{git}
%else
gpgv2 --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -n php-sqlite-migrate-%{version}
%endif

%build
%{_bindir}/phpab -t fedora -o src/autoload.php src

%install
mkdir -p %{buildroot}%{_datadir}/php/fkooman/SqliteMigrate
cp -pr src/* %{buildroot}%{_datadir}/php/fkooman/SqliteMigrate

%check
%{_bindir}/phpab -t fedora -o tests/autoload.php tests
cat <<'AUTOLOAD' | tee -a tests/autoload.php
require_once 'src/autoload.php';
AUTOLOAD

%{phpunit} tests --verbose --bootstrap=tests/autoload.php

%files
%license LICENSE
%doc composer.json CHANGELOG.md README.md
%dir %{_datadir}/php/fkooman
%{_datadir}/php/fkooman/SqliteMigrate

%changelog
* Sun Sep 09 2018 François Kooman <fkooman@tuxed.net> - 0.1.1-3
- merge dev and prod spec files in one
- cleanup requirements

* Sat Sep 08 2018 François Kooman <fkooman@tuxed.net> - 0.1.1-2
- move some stuff around to make it consistent with other spec files

* Thu Jul 26 2018 François Kooman <fkooman@tuxed.net> - 0.1.1-1
- initial package
