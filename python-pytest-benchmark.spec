#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests [very sensitive to pytest output]

Summary:	py.test fixture for benchmarking code
Summary(pl.UTF-8):	Wyposażenie py.testa do testowania wydajności kodu
Name:		python-pytest-benchmark
Version:	3.4.1
Release:	7
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-benchmark/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-benchmark/pytest-benchmark-%{version}.tar.gz
# Source0-md5:	7fa3588a1a94fc2bbf42b377d6bdb946
Patch0:		%{name}-tests.patch
URL:		https://github.com/ionelmc/pytest-benchmark
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
#BuildRequires:	python-aspectlib >= 1.4.2
# for storage tests
#BuildRequires:	python-elasticsearch >= 5.3.0
BuildRequires:	python-freezegun >= 0.3.8
BuildRequires:	python-pathlib >= 1.0.1
BuildRequires:	python-py-cpuinfo
# for histogram tests
#BuildRequires:	python-pygal >= 2.2.1
#BuildRequires:	python-pygaljs >= 1.0.1
BuildRequires:	python-pytest >= 3.8
BuildRequires:	python-statistics >= 1.0.3.5
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_py3doc_enhanced_theme
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A py.test fixture for benchmarking code. It will group the tests into
rounds that are calibrated to the chosen timer.

%description -l pl.UTF-8
Wyposażenie (fixture) modułu py.test do testowania wydajności kodu.
Grupuje testy w rundy, które są kalibrowane do wybranego stopera.

%package apidocs
Summary:	API documentation for Python pytest_benchmark module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest_benchmark
Group:		Documentation

%description apidocs
API documentation for Python pytest_benchmark module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest_benchmark.

%prep
%setup -q -n pytest-benchmark-%{version}
%patch -P 0 -p1

# (mostly temporarily disabled tests)
# requires elasticsearch
%{__rm} tests/test_elasticsearch_storage.py
# no py.test-benchmark program before install
%{__rm} tests/test_cli.py
# requires pygal for histograms
%{__rm} tests/test_storage.py
# require aspectlib
%{__rm} tests/test_with_testcase.py
%{__rm} tests/test_with_weaver.py
# a few too depending on git, one elasticsearch
%{__rm} tests/test_utils.py

%build
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif

%if %{with doc}
cd docs
PYTHONPATH=$(pwd)/../src \
sphinx-build-2 -b html . _build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/py.test-benchmark{,-2}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pytest-benchmark{,-2}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/py.test-benchmark-2
%attr(755,root,root) %{_bindir}/pytest-benchmark-2
%{py_sitescriptdir}/pytest_benchmark
%{py_sitescriptdir}/pytest_benchmark-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,*.html,*.js}
%endif
