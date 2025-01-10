#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.12.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kalarm
Summary:	kalarm
Name:		ka6-%{kaname}
Version:	24.12.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	08479b3128848c3d21a3592d92521153
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	ka6-akonadi-devel >= 18.04.0
BuildRequires:	ka6-kcalutils-devel >= %{kdeappsver}
BuildRequires:	ka6-kimap-devel >= %{kdeappsver}
BuildRequires:	ka6-mailcommon-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kauth-devel >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kcodecs-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kholidays-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kjobwidgets-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	ka5-%{kaname} < %{version}
ExcludeArch:	x32 i686
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KAlarm is a personal alarm message, command and email scheduler.

Features

• Display alarms using your own text message, the text generated by a
command, or a text or image file. • Audible alarm using a sound file •
Recurring alarm on an hours/minutes, daily, weekly, monthly or annual
basis, or set it to trigger every time you log in. • Display alarms
color and font customization • Support for multiple alarm calendars,
which for example enables you to share alarms between a laptop and
desktop computer.

%description -l pl.UTF-8
KAlarm jest osobistym budzikiem i harmonogramem.

Własciwości

• Wyświetla własne wiadomości tekstowe, lub tekst wygenerowany przez
program, lub wyświetla plik tekstowy bądź obrazek • Dźwiękowe
powiadomomienia • Powtarzalne alarmy, o określonej godzinie/minucie,
dzienne, tygodniowe, miesięczne lub roczne a także wyzwalane wtedy gdy
się zalogujesz • Możliwość konfiguracji koloru i rodzaju czcionki •
Wsparcie dla wielu kalendarzy powiadomień, co pozwala na przykład
współdzielić alarmy między laptopem a komputerem stacjonarnym

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
/etc/xdg/autostart/kalarm.autostart.desktop
%attr(755,root,root) %{_bindir}/kalarm
%attr(755,root,root) %{_bindir}/kalarmautostart
%attr(755,root,root) %{_libdir}/libkalarmcalendar.so.*.*
%ghost %{_libdir}/libkalarmcalendar.so.6
%attr(755,root,root) %{_libdir}/libkalarmplugin.so.*.*
%ghost %{_libdir}/libkalarmplugin.so.6
%dir %{_libdir}/qt6/plugins/pim6/kalarm
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/kalarm/akonadiplugin.so
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/kalarm_helper
%{_desktopdir}/org.kde.kalarm.desktop
%{_datadir}/config.kcfg/kalarmconfig.kcfg
%{_datadir}/dbus-1/interfaces/org.kde.kalarm.kalarm.xml
%{_datadir}/dbus-1/system-services/org.kde.kalarm.rtcwake.service
%{_datadir}/dbus-1/system.d/org.kde.kalarm.rtcwake.conf
%{_iconsdir}/hicolor/128x128/apps/kalarm.png
%{_iconsdir}/hicolor/16x16/apps/kalarm.png
%{_iconsdir}/hicolor/22x22/apps/kalarm.png
%{_iconsdir}/hicolor/32x32/apps/kalarm.png
%{_iconsdir}/hicolor/48x48/apps/kalarm.png
%{_iconsdir}/hicolor/64x64/apps/kalarm.png
%{_datadir}/kalarm
%{_datadir}/knotifications6/kalarm.notifyrc
%{_datadir}/metainfo/org.kde.kalarm.appdata.xml
%{_datadir}/polkit-1/actions/org.kde.kalarm.rtcwake.policy
%{_datadir}/qlogging-categories6/kalarm.categories
%{_datadir}/qlogging-categories6/kalarm.renamecategories
%attr(755,root,root) %{_libdir}/kconf_update_bin/kalarm-3.10.0-run_mode
%{_datadir}/kconf_update/kalarm.upd
