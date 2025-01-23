%global package_speccommit 568771e8be262d8ff0d739ab760ad6c8a808e81f
%global usver 2.28.1
%global xsver 4
%global xsrel %{xsver}.1%{?xscount}%{?xshash}
# When bootstrapping Python, we cannot test this yet
%bcond_with tests

Name:           python-requests
Version:        2.28.1
Release: %{?xsrel}%{?dist}
Summary:        HTTP library, written in Python, for human beings

License:        ASL 2.0
URL:            https://pypi.io/project/requests
Source0: requests-v2.28.1.tar.gz
Patch0: requests-2.28.1-system-certs.patch
Patch1: requests-2.28.1-tests_nonet.patch
Patch2: CVE-2023-32681.patch
BuildArch:      noarch

Source1: pyproject_wheel.py

%description
Most existing Python modules for sending HTTP requests are extremely verbose and
cumbersome. Python’s built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.

%package -n python%{python3_pkgversion}-requests
Summary: HTTP library, written in Python, for human beings

%{?python_provide:%python_provide python%{python3_pkgversion}-requests}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros

%if 0%{?xenserver} < 9
BuildRequires:  python3-wheel
%endif

%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-httpbin)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(trustme)
%endif


%description -n python%{python3_pkgversion}-requests
Most existing Python modules for sending HTTP requests are extremely verbose and
cumbersome. Python’s built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.

%pyproject_extras_subpkg -n python%{python3_pkgversion}-requests security socks

%generate_buildrequires
%if %{with tests}
%pyproject_buildrequires -r
%else
%pyproject_buildrequires
%endif


%prep
%autosetup -p1 -n requests-%{version}

# env shebang in nonexecutable file
sed -i '/#!\/usr\/.*python/d' requests/certs.py

# Some doctests use the internet and fail to pass in Koji. Since doctests don't have names, I don't
# know a way to skip them. We also don't want to patch them out, because patching them out will
# change the docs. Thus, we set pytest not to run doctests at all.
sed -i 's/ --doctest-modules//' pyproject.toml


%build
%if 0%{?xenserver} < 9
echo "from setuptools import setup

setup(name=\"%{name}\",
      version='%{version}',
     )" > ./setup.py
/usr/bin/python3 -Bs %{SOURCE1} %{_builddir}/requests-%{version}/pyproject-wheeldir
%else
%pyproject_wheel
%endif


%install
%if 0%{?xenserver} < 9
/usr/bin/python3 -m pip install --root %{buildroot} --prefix /usr --no-deps --disable-pip-version-check --verbose --ignore-installed --no-index --no-cache-dir --find-links %{_builddir}/requests-%{version}/pyproject-wheeldir
%else
%pyproject_install
%pyproject_save_files requests
%endif

%if 0%{?xenserver} < 9
# Copy source files to buildroot manually
mkdir -p %{buildroot}%{python3_sitelib}/requests
cp -r %{_builddir}/requests-%{version}/requests %{buildroot}%{python3_sitelib}/
find %{buildroot}%{python3_sitelib}/requests
%endif


%if %{with tests}
%check
# Omitted tests use a TARPIT server so require network connection
%pytest -v -k "not (test_connect_timeout or test_total_timeout_connect)"
%endif


%if 0%{?xenserver} < 9
%files -n python%{python3_pkgversion}-requests
%dir %{python3_sitelib}/requests
%dir %{python3_sitelib}/requests/__pycache__
%{python3_sitelib}/requests/__init__.py
%{python3_sitelib}/requests/__pycache__/__init__.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/__version__.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/_internal_utils.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/adapters.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/api.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/auth.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/certs.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/compat.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/cookies.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/exceptions.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/help.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/hooks.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/models.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/packages.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/sessions.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/status_codes.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/structures.cpython-*.pyc
%{python3_sitelib}/requests/__pycache__/utils.cpython-*.pyc
%{python3_sitelib}/requests/__version__.py
%{python3_sitelib}/requests/_internal_utils.py
%{python3_sitelib}/requests/adapters.py
%{python3_sitelib}/requests/api.py
%{python3_sitelib}/requests/auth.py
%{python3_sitelib}/requests/certs.py
%{python3_sitelib}/requests/certs.py.orig
%{python3_sitelib}/requests/compat.py
%{python3_sitelib}/requests/cookies.py
%{python3_sitelib}/requests/exceptions.py
%{python3_sitelib}/requests/help.py
%{python3_sitelib}/requests/hooks.py
%{python3_sitelib}/requests/models.py
%{python3_sitelib}/requests/packages.py
%{python3_sitelib}/requests/sessions.py
%{python3_sitelib}/requests/status_codes.py
%{python3_sitelib}/requests/structures.py
%{python3_sitelib}/requests/utils.py
%license LICENSE
%doc README.md HISTORY.md
%else
%files -n python%{python3_pkgversion}-requests -f %{pyproject_files}
%license LICENSE
%doc README.md HISTORY.md
%endif


%changelog
* Thu Jan 23 2025 Yann Dirson <yann.dirson@vates.tech> - 2.28.1-4.1
- Fix build invocation using hardcoded (and buggy) paths

* Mon Aug 19 2024 Marcus Granado <marcus.granado@cloud.com> - 2.28.1-4
- Bump release and rebuild

* Fri Aug 09 2024 Marcus Granado <marcus.granado@cloud.com> - 2.28.1-3
- Bump release and rebuild

* Fri Jul 07 2023 Tim Smith <tim.smith@citrix.com> - 2.28.1-1
- First imported release

