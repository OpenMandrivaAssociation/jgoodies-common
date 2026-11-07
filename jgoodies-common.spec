Name:		jgoodies-common
Version:	1.8.1
Release:	1
Summary:	Shared code for JGoodies libraries
Group:		Development/Java
License:	BSD
URL:		https://www.jgoodies.com/
Source0:	https://www.jgoodies.com/download/libraries/common/jgoodies-common-1_8_1.zip#/jgoodies-common-%{version}.zip

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name jgoodies-common

Obsoletes:	%{name}-javadoc < %{version}-%{release}

%description
JGoodies Common is shared convenience code for the other JGoodies
libraries. 1.8.1 marks ArrayListModel and LinkedListModel final and
replaces package.html with package-info.java. The upstream archive
ships prebuilt jars; this package compiles the sources instead.
The compiler source level is 1.8. Tests are skipped.

%prep
%autosetup -n jgoodies-common-%{version}
rm -rf docs
python - <<'PY'
import zipfile
from pathlib import Path

dest = Path("src/main/java")
dest.mkdir(parents=True)
with zipfile.ZipFile("jgoodies-common-%{version}-sources.jar") as archive:
    archive.extractall(dest)
meta = dest / "META-INF"
if meta.exists():
    for child in meta.rglob("*"):
        if child.is_file():
            child.unlink()
    for child in sorted(meta.rglob("*"), reverse=True):
        if child.is_dir():
            child.rmdir()
    meta.rmdir()
for jar in Path(".").glob("*.jar"):
    jar.unlink()

java_files = list(Path("src/main/java").rglob("*.java"))
if len(java_files) != 36:
    raise SystemExit("java files " + str(len(java_files)))
if list(Path(".").rglob("*.jar")):
    raise SystemExit("prebuilt jar remains")
Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.jgoodies</groupId>
  <artifactId>jgoodies-common</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>JGoodies Common</name>
  <description>Convenience code shared by JGoodies libraries.</description>
  <url>https://www.jgoodies.com/</url>
  <licenses>
    <license>
      <name>BSD</name>
      <url>https://www.jgoodies.com/</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
  </properties>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <source>1.8</source>
          <target>1.8</target>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
for needle in (
    "<artifactId>jgoodies-common</artifactId>",
    "<version>%{version}</version>",
    "<source>1.8</source>",
    "<target>1.8</target>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
for needle in ("junit", "oss-parent", "<source>1.6</source>", "SNAPSHOT", "<release>"):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/jgoodies-common-%{version}.jar --describe-module jgoodies.common > module-describe.txt
# A versioned jar prints "name@version ... automatic", not "name automatic".
grep -q '^jgoodies.common' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }

%files -f .mfiles
%doc LICENSE.txt README.html RELEASE-NOTES.txt
