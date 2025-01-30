# The debug symbol table at higher -g levels becomes so
# huge that even the biggest builders run out of space
%global optflags %{optflags} -g1

Name:		mame
Version:	0.273
Release:	1
Source0:	https://github.com/mamedev/mame/archive/refs/tags/mame%(echo %{version}|sed -e 's,\.,,g').tar.gz
Summary:	Emulator for a wide range of Arcade machines
URL:		https://mamedev.org/
License:	GPL-2.0
Group:		Emulators
BuildRequires:	dos2unix
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(asio)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(libutf8proc)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_ttf)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(RapidJSON)
BuildRequires:	pkgconfig(pugixml)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)

%rename xmame
%rename sdlmame

%patchlist
mame-0.273-sqlite.patch

%description
MAME's purpose is to preserve decades of software history. As electronic
technology continues to rush forward, MAME prevents this important "vintage"
software from being lost and forgotten. This is achieved by documenting the
hardware and how it functions. The source code to MAME serves as this
documentation. The fact that the software is usable serves primarily to
validate the accuracy of the documentation (how else can you prove that you
have recreated the hardware faithfully?). Over time, MAME (originally stood
for Multiple Arcade Machine Emulator) absorbed the sister-project MESS (Multi
Emulator Super System), so MAME now documents a wide variety of (mostly
vintage) computers, video game consoles and calculators, in addition to the
arcade video games that were its initial focus.

%prep
%autosetup -p1 -n mame-mame%(echo %{version}|sed -e 's,\.,,g')

%conf
# remove internal copies of libraries
# we either get from the system or don't need at all
rm -rf \
	3rdparty/asio \
	3rdparty/compat \
	3rdparty/dxsdk \
	3rdparty/expat \
	3rdparty/glm \
	3rdparty/flac \
	3rdparty/libjpeg \
	3rdparty/portaudio \
	3rdparty/portmidi \
	3rdparty/pugixml \
	3rdparty/rapidjson \
	3rdparty/sqlite3 \
	3rdparty/tap-windows6 \
	3rdparty/utf8proc \
	3rdparty/zlib \
	3rdparty/zstd \
	docs/themes

%build
#	CC="%{__cc}" \
#	CXX="%{__cxx}" \
%make_build all TARGET=mame \
	NOWERROR=1 \
	QT_HOME=%{_libdir}/qt6 \
	NO_USE_QTDEBUG=1 \
	NO_DEBUGGER=1 \
	USE_SYSTEM_LIB_ASIO=1 \
	USE_SYSTEM_LIB_EXPAT=1 \
	USE_SYSTEM_LIB_FLAC=1 \
	USE_SYSTEM_LIB_GLM=1 \
	USE_SYSTEM_LIB_JPEG=1 \
	USE_SYSTEM_LIB_PORTAUDIO=1 \
	USE_SYSTEM_LIB_PORTMIDI=1 \
	USE_SYSTEM_LIB_PUGIXML=1 \
	USE_SYSTEM_LIB_RAPIDJSON=1 \
	USE_SYSTEM_LIB_SQLITE3=1 \
	USE_SYSTEM_LIB_UTF8PROC=1 \
	USE_SYSTEM_LIB_ZLIB=1 \
	USE_SYSTEM_LIB_ZSTD=1 \
	LDOPTS="%{build_ldflags}" \
	OPT_FLAGS="%{optflags}" \
	VERBOSE=1 \
	PYTHON_EXECUTABLE=python \
	TOOLS=1

%install
# create directories
install -d %{buildroot}%{_sysconfdir}/%{name}
for folder in cfg comments diff inp
do
	install -d %{buildroot}%{_sysconfdir}/skel/.config/%{name}/$folder
done
for folder in memcard nvram snap sta
do
	install -d %{buildroot}%{_sysconfdir}/skel/.local/state/%{name}/$folder
done
for folder in roms
do
	install -d %{buildroot}%{_sysconfdir}/skel/.local/share/%{name}/$folder
done
 
install -d %{buildroot}%{_bindir}
for folder in artwork bgfx chds cheats ctrlr effects fonts hash language \
	plugins keymaps roms samples shader
do
	install -d %{buildroot}%{_datadir}/%{name}/$folder
done
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man6
 
cat >%{buildroot}%{_sysconfdir}/%{name}/%{name}.ini <<EOF
# Define multi-user paths
artpath			%{_datadir}/%{name}/artwork;%{_datadir}/%{name}/effects
bgfx_path		%{_datadir}/%{name}/bgfx
cheatpath		%{_datadir}/%{name}/cheat
crosshairpath		%{_datadir}/%{name}/crosshair
ctrlrpath		%{_datadir}/%{name}/ctrlr
fontpath		%{_datadir}/%{name}/fonts
hashpath		%{_datadir}/%{name}/hash
languagepath		%{_datadir}/%{name}/language
pluginspath		%{_datadir}/%{name}/plugins
rompath			%{_datadir}/%{name}/roms;%{_datadir}/%{name}/chds;\$HOME/.local/share/%{name}/roms;\$XDG_DATA_HOME/%{name}/roms
samplepath		%{_datadir}/%{name}/samples
 
# Allow user to override ini settings
inipath			\$XDG_CONFIG_HOME/%{name};\$HOME/.config/%{name};\$HOME/.%{name}/ini;%{_sysconfdir}/%{name}
 
# Set paths for local storage
cfg_directory		\$XDG_CONFIG_HOME/%{name}/cfg;\$HOME/.config/%{name}/cfg;\$HOME/.%{name}/cfg
comment_directory	\$XDG_CONFIG_HOME/%{name}/comments;\$HOME/.config/%{name}/comments;\$HOME/.%{name}/comments
diff_directory		\$XDG_CONFIG_HOME/%{name}/diff;\$HOME/.config/%{name}/diff;\$HOME/.%{name}/diff
input_directory		\$XDG_CONFIG_HOME/%{name}/inp;\$HOME/.config/%{name}/inp;\$HOME/.%{name}/inp
nvram_directory		\$XDG_STATE_HOME/%{name}/nvram;\$HOME/.local/state/%{name}/nvram;\$HOME/.%{name}/nvram
snapshot_directory	\$XDG_STATE_HOME/%{name}/snap;\$HOME/.local/state/%{name}/snap;\$HOME/.%{name}/snap
state_directory		\$XDG_STATE_HOME/%{name}/sta;\$HOME/.local/state/%{name}/sta;\$HOME/.%{name}/sta
 
# OpenMandriva custom defaults
autosave		1
EOF

%if %{with debug}
install -pm 755 %{name}d %{buildroot}%{_bindir}/%{name}d
%else
install -pm 755 %{name} %{buildroot}%{_bindir}/%{name}
%endif
install -pm 755 castool chdman floptool imgtool jedutil ldresample ldverify \
	nltool nlwav pngcmp romcmp unidasm %{buildroot}%{_bindir}
for tool in regrep split srcclean; do
	install -pm 755 $tool %{buildroot}%{_bindir}/%{name}-$tool
done
pushd artwork
	find -type d -exec install -d %{buildroot}%{_datadir}/%{name}/artwork/{} \;
	find -type f -exec install -pm 644 {} %{buildroot}%{_datadir}/%{name}/artwork/{} \;
popd
pushd bgfx
	find -type d -a ! -wholename \*dx\* -a ! -wholename \*metal\* -exec install -d %{buildroot}%{_datadir}/%{name}/bgfx/{} \;
	find -type f -a ! -wholename \*dx\* -a ! -wholename \*metal\* -exec install -pm 644 {} %{buildroot}%{_datadir}/%{name}/bgfx/{} \;
popd
install -pm 644 hash/* %{buildroot}%{_datadir}/%{name}/hash
install -pm 644 keymaps/* %{buildroot}%{_datadir}/%{name}/keymaps
pushd language
	find -type d -exec install -d %{buildroot}%{_datadir}/%{name}/language/{} \;
	find -type f -name \*.mo -exec install -pm 644 {} %{buildroot}%{_datadir}/%{name}/language/{} \;
	# flag the translation files as %%lang
	grep -r --include=*.po \"Language: | sed -r 's@(.*)/strings\.po:"Language: ([[:alpha:]]{2}(_[[:alpha:]]{2})?)\\n"@%lang(\2) %{_datadir}/%{name}/language/\1@' > ../%{name}.lang
popd
pushd plugins
	find -type d -exec install -d %{buildroot}%{_datadir}/%{name}/plugins/{} \;
	find -type f -exec install -pm 644 {} %{buildroot}%{_datadir}/%{name}/plugins/{} \;
popd
pushd src/osd/modules/opengl
	install -pm 644 shader/*.?sh %{buildroot}%{_datadir}/%{name}/shader
popd
pushd docs/man
install -pm 644 castool.1 chdman.1 imgtool.1 floptool.1 jedutil.1 ldresample.1 \
	ldverify.1 romcmp.1 %{buildroot}%{_mandir}/man1
install -pm 644 mame.6 %{buildroot}%{_mandir}/man6
popd
 
# Make sure only html documentation is installed
rm -f docs/.buildinfo
rm -rf docs/build/html/_sources

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/skel/.config/%{name}
%{_sysconfdir}/skel/.local/state/%{name}
%{_sysconfdir}/skel/.local/share/%{name}
%{_bindir}/%{name}
%{_mandir}/man6/mame.6*
 
# Tools
%{_bindir}/castool
%{_bindir}/chdman
%{_bindir}/floptool
%{_bindir}/imgtool
%{_bindir}/jedutil
%{_bindir}/ldresample
%{_bindir}/ldverify
%{_bindir}/nltool
%{_bindir}/nlwav
%{_bindir}/pngcmp
%{_bindir}/%{name}-regrep
%{_bindir}/romcmp
%{_bindir}/%{name}-split
%{_bindir}/%{name}-srcclean
%{_bindir}/unidasm
%{_mandir}/man1/castool.1*
%{_mandir}/man1/chdman.1*
%{_mandir}/man1/floptool.1*
%{_mandir}/man1/imgtool.1*
%{_mandir}/man1/jedutil.1*
%{_mandir}/man1/ldresample.1*
%{_mandir}/man1/ldverify.1*
%{_mandir}/man1/romcmp.1*
 
%doc README.md
%license COPYING docs/legal/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/artwork
%{_datadir}/%{name}/bgfx
%{_datadir}/%{name}/chds
%{_datadir}/%{name}/cheats
%{_datadir}/%{name}/effects
%{_datadir}/%{name}/fonts
%{_datadir}/%{name}/keymaps
%dir %{_datadir}/%{name}/language
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/roms
%{_datadir}/%{name}/samples
%{_datadir}/%{name}/shader
 
%{_datadir}/%{name}/hash
