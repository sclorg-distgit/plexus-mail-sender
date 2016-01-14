%global pkg_name plexus-mail-sender
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global namedversion 1.0-alpha-2

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.0
Release:        1.a2.25.13%{?dist}
Epoch:          0
Summary:        Plexus Mail Sender
License:        MIT and ASL 1.1
URL:            http://plexus.codehaus.org/
# svn export http://svn.codehaus.org/plexus/tags/PLEXUS_MAIL_SENDER_1_0_ALPHA_2/
# Note: Exported revision 8188.
# mv PLEXUS_MAIL_SENDER_1_0_ALPHA_2/ plexus-mail-sender-1.0-a2
# tar czf plexus-mail-sender-1.0-a2-src.tar.gz plexus-mail-sender-1.0-a2
Source0:        plexus-mail-sender-%{version}-a2-src.tar.gz

# http://jira.codehaus.org/browse/PLX-417
# http://fisheye.codehaus.org/rdiff/plexus?csid=8336&u&N
Patch0:         %{pkg_name}-clarifylicense.patch

BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}maven-compiler-plugin
BuildRequires:  %{?scl_prefix}maven-install-plugin
BuildRequires:  %{?scl_prefix}maven-jar-plugin
BuildRequires:  %{?scl_prefix}maven-javadoc-plugin
BuildRequires:  %{?scl_prefix}maven-resources-plugin
BuildRequires:  %{?scl_prefix}maven-site-plugin
BuildRequires:  %{?scl_prefix}maven-surefire-plugin
BuildRequires:  %{?scl_prefix}maven-doxia-sitetools
BuildRequires:  %{?scl_prefix}saxon
BuildRequires:  %{?scl_prefix}saxon-scripts
BuildRequires:  %{?scl_prefix_java_common}javamail


BuildArch:      noarch


%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.  This
Plexus component provides SMTP transport.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.


%prep
%setup -q -n %{pkg_name}-%{version}-a2
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%patch0 -p3

mv release-pom.xml pom.xml

pushd plexus-mail-senders
mv release-pom.xml pom.xml
%pom_disable_module plexus-mail-sender-test
for mod in javamail simple test;do
    pushd %{pkg_name}-$mod
    mv release-pom.xml pom.xml
    popd
done
popd

mv %{pkg_name}-api/release-pom.xml %{pkg_name}-api/pom.xml
find . -iname 'pom.xml' -exec sed -i \
       's:<groupId>plexus</groupId>:<groupId>org.codehaus.plexus</groupId>:g' \{\} \;
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_package ":*senders" __noinstall
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc


%changelog
* Thu Jan 15 2015 Michal Srb <msrb@redhat.com> - 0:1.0-1.a2.25.13
- Fix directory ownership

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.12
- Rebuild to fix provides

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:1.0-1.a2.25.11
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0:1.0-1.a2.25.10
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.9
- Mass rebuild 2014-05-26

* Fri Mar 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.8
- Add BR on javamail

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.7
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.6
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.5
- Remove requires on java

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.4
- Rebuild to fix incorrect auto-requires

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-1.a2.25.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.0-1.a2.25
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.a2.25
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-0.a2.24
- Fix release tag

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.0-0.a2.24
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 24 2013 Michal Srb <msrb@redhat.com> - 0:1.0-0.a2.23
- Build with xmvn
- Fixed pom_ macro

* Thu Oct 11 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.22
- Do not build test submodule to simplify dependencies

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.a2.21.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar  2 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> 0:1.0-0.a2.21
- Fix build and install proper pom files

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.a2.20.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 7 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.20
- Fix up according to latest guidelines

* Sun Jun 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.a2.19
- Build with maven 3.x

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.a2.18.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.18
- Add update_maven_depmap execution to post/postun (#669495)

* Thu Dec 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.17
- Add maven metadata

* Mon Dec 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.a2.16
- Fix FTBFS.
- Adapt to current guidelines.

* Wed Sep  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.0-0.a2.15
- Add maven-site-plugin to BR
- Update maven-plugin BR names

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.a2.14
- Remove dummy things from the depmap.
- Remove workaround for old javadoc plugin.

* Mon Nov 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.a2.13
- BR maven-doxia-sitetools.

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.a2.12
- Force OpenJDK

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.a2.11
- Add BRs on maven2-plugin-{compiler,surefire,jar,install.javadoc}

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.a2.10
- Add BR on maven2-plugin-resources

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.a2.9
- Remove gcj support
- Remove javadoc post scriplet
- Add patch to clarify license (http://jira.codehaus.org/browse/PLX-417)
- Fix license
- Use tarball with versioned directory

* Sun May 17 2009 Fernando Nasser <fnasser@redhat.com> - 0:1.0-0.a2.8
- Fix license

* Tue Apr 30 2009 Yong Yang <yyang@redhat.com> - 0:1.0-0.a2.7
- Don't run the tests as they reqyuire access to the net
- Add BRs maven-doxia*
- Rebuild with new maven2 2.0.8 built in non-bootstrap mode

* Tue Mar 17 2009 Yong Yang <yyang@redhat.com> - 0:1.0-0.a2.6
- rebuild with new maven2 2.0.8 built in bootstrap mode

* Thu Feb 05 2009 Yong Yang <yyang@redhat.com> - 0:1.0-0.a2.5
- Fix release tag

* Wed Jan 14 2009 Yong Yang <yyang@redhat.com> - 0:1.0-0.a2.4jpp
- Import from dbhole's maven packages, initial building

* Tue May 15 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a2.3jpp
- Make Vendor, Distribution based on macro

* Thu Mar 15 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a2.2jpp
- Add dumbster BR

* Wed Sep 13 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a2.1jpp
- First JPP-1.7 release
- Add post/postun Requires for javadoc
- Add gcj_support option
