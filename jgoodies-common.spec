%global shortname common

Name:           jgoodies-common
Version:        1.8.0
Release:        1
Summary:        Common library shared by JGoodies libraries and applications

Group:          Development/Java
License:        BSD
URL:            https://www.jgoodies.com/
Source0:        http://www.jgoodies.com/download/libraries/%{shortname}/%{name}-%(tr "." "_" <<<%{version}).zip

BuildRequires:  java-devel
BuildRequires:  fontconfig
BuildRequires:  jpackage-utils
BuildRequires:  maven-local
BuildRequires:  maven-clean-plugin
BuildRequires:  maven-dependency-plugin
BuildRequires:	fonts-ttf-dejavu

Requires:       java
Requires:       jpackage-utils
BuildArch:      noarch

%description
The JGoodies Common library provides convenience code for other JGoodies
libraries and applications.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q

# Unzip source and test files from provided JARs
mkdir -p src/main/java/ src/test/java/
pushd src/main/java/
jar -xf ../../../%{name}-%{version}-sources.jar
popd
pushd src/test/java/
jar -xf ../../../%{name}-%{version}-tests.jar
popd

# Delete prebuild JARs
find -name "*.jar" -exec rm -f {} \;

# Remove DOS line endings
for file in LICENSE.txt RELEASE-NOTES.txt; do
  sed 's|\r||g' $file > $file.new && \
  touch -r $file $file.new && \
  mv $file.new $file
done


%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt README.html RELEASE-NOTES.txt


%files javadoc -f .mfiles-javadoc


%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 1.1.1-4
+ Revision: 734048
- rebuild
- imported package jgoodies-common

