%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global _with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

Name:           python-requests
Version:        0.13.1
Release:        2%{?dist}
Summary:        HTTP library, written in Python, for human beings

License:        ISC and MIT
URL:            http://pypi.python.org/pypi/requests
Source0:        http://pypi.python.org/packages/source/r/requests/requests-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel

Requires:       ca-certificates

%description
Most existing Python modules for sending HTTP requests are extremely verbose and 
cumbersome. Python’s built-in urllib2 module provides most of the HTTP 
capabilities you should need, but the API is thoroughly broken. This library is 
designed to make HTTP requests easy for developers.

%if 0%{?_with_python3}
%package -n python3-requests
Summary: HTTP library, written in Python, for human beings
BuildRequires: python3-devel
Requires: python3-chardet
%description -n python3-requests
Most existing Python modules for sending HTTP requests are extremely verbose and
cumbersome. Python’s built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.
%else
Requires: python-chardet
%endif


%prep
%setup -q -n requests-%{version}

%build
%{__python} setup.py build
%if 0%{?_with_python3}
%{__python3} setup.py build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%if 0%{?_with_python3}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%endif

 
%files
%defattr(-,root,root,-)
%doc NOTICE LICENSE README.rst HISTORY.rst
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/requests
%{python_sitelib}/requests/*

%if 0%{?_with_python3}
%files -n python3-requests
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/requests/
%endif


%changelog
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Arun S A G <sagarun@gmail.com> 0.13.1-1
- Updated to latest upstream release 0.13.1
- Use system provided ca-certificates
- No more async requests use grrequests https://github.com/kennethreitz/grequests
- Remove gevent as it is no longer required by requests

* Sun Apr 01 2012 Arun S A G <sagarun@gmail.com> 0.11.1-1
- Updated to upstream release 0.11.1

* Thu Mar 29 2012 Arun S A G <sagarun@gmail.com> 0.10.6-3
- Support building package for EL6

* Tue Mar 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.6-2
- +python3-requests pkg

* Sat Mar 3 2012 Arun SAG <sagarun@gmail.com> - 0.10.6-1
- Updated to new upstream version

* Sat Jan 21 2012 Arun SAG <sagarun@gmail.com> - 0.9.3-1
- Updated to new upstream version 0.9.3
- Include python-gevent as a dependency for requests.async
- Clean up shebangs in requests/setup.py,test_requests.py and test_requests_ext.py

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Arun SAG <sagarun@gmail.com> - 0.8.2-1
- New upstream version
- keep alive support
- complete removal of cookiejar and urllib2

* Thu Nov 10 2011 Arun SAG <sagarun@gmail.com> - 0.7.6-1
- Updated to new upstream release 0.7.6

* Thu Oct 20 2011 Arun SAG <sagarun@gmail.com> - 0.6.6-1
- Updated to version 0.6.6

* Fri Aug 26 2011 Arun SAG <sagarun@gmail.com> - 0.6.1-1
- Updated to version 0.6.1

* Sat Aug 20 2011 Arun SAG <sagarun@gmail.com> - 0.6.0-1
- Updated to latest version 0.6.0

* Mon Aug 15 2011 Arun SAG <sagarun@gmail.com> - 0.5.1-2
- Remove OPT_FLAGS from build section since it is a noarch package
- Fix use of mixed tabs and space
- Remove extra space around the word cumbersome in description

* Sun Aug 14 2011 Arun SAG <sagarun@gmail.com> - 0.5.1-1
- Initial package
