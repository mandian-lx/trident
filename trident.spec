%{?_javapackages_macros:%_javapackages_macros}
%global debug_package %{nil}

%bcond_with test_jar

Summary:	An library for Java applications
Name:		trident
Version:	1.3
Release:	1
License:	BSD
Group:		Development/Java
URL:		https://kenai.com/projects/trident
Source0:	https://kenai.com/projects/%{name}/downloads/download/version%20%{version}%20-%20stable/%{name}-all.zip
Source1:	http://central.maven.org/maven2/org/pushingpixels/%{name}/%{version}/%{name}-%{version}.pom

BuildRequires:	maven-local
BuildRequires:	jpackage-utils
BuildRequires:	ant
BuildRequires:	eclipse-swt

Requires:	eclipse-swt

%description
The goal of this project is to provide a powerful and extensible animation
library for Java applications. It requires Java 6+ at compile and runtime,
and is available under BSD license. Use links on the left sidebar to navigate
to projects mailing lists, forums, download section, issue tracker and source
code repository.


%files -f .mfiles
%if %without test_jar
%{_javadir}/%{name}-tst.jar
%endif

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Requires:	jpackage-utils
BuildArch:	noarch

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q -c -n %{name}-%{version}
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Remove dependency from Android
rm -fr src/org/pushingpixels/trident/android

# Add pom.xml
cp %{SOURCE1} pom.xml

# Remove unused/unpackaged dependencies
%pom_remove_dep com.google.android:android
%pom_remove_dep org.eclipse.swt.gtk.linux:

# Alias
%mvn_alias org.pushingpixels:%{name} "org.pushing-pixels:%{name}"

# Fix jar name
%mvn_file :%{name} %{name}

%build
export CLASSPATH=$(build-classpath swt)
%ant -Djdk.home=/usr -Dfile.encoding=UTF-8

# javadoc
%javadoc -d doc -public \
		`find ./src/org -name '*.java'`

# index the jars (fix jar-not-indexed warning)
pushd www/webstart
%jar -i %{name}.jar
%if %without test_jar
%jar -i %{name}-tst.jar
%endif
popd

# maven artifact installation
%mvn_artifact pom.xml www/webstart/%{name}.jar

%install
%mvn_install -J doc

# test jar
%if %without test_jar
install -pm 0644 www/webstart/%{name}-tst.jar %{buildroot}%{_javadir}/
%endif

