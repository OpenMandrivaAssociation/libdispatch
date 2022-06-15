%define major 0
%define libdispatch %mklibname dispatch %{major}
%define libBlocksRuntime %mklibname BlocksRuntime %{major}
%define devname %mklibname dispatch -d


Name:		libdispatch
Version:	5.5
Release:	1
Summary:	Apple's Grand Central Dispatch library
Group:		System/Libraries
License:	ASL 2.0
URL:		https://github.com/apple/swift-corelibs-libdispatch
Source0:	https://github.com/apple/swift-corelibs-libdispatch/archive/refs/tags/swift-corelibs-libdispatch-swift-%{version}-RELEASE.tar.gz
#Patch0:		asprintf.patch
Patch1:		libdispatch-versioning.patch
BuildRequires:	clang
BuildRequires:	libbsd-devel
BuildRequires:	ninja
BuildRequires:	cmake
BuildRequires:	chrpath
Provides:	libblocksruntime = %{EVRD}

%description
Grand Central Dispatch (GCD or libdispatch) provides 
comprehensive support for concurrent code execution on 
multicore hardware.

libdispatch is currently available on all Darwin platforms. 
This project aims to make a modern version of libdispatch 
available on all other Swift platforms. To do this, we will 
implement as much of the portable subset of the API as 
possible, using the existing open source C implementation.

libdispatch on Darwin is a combination of logic in the xnu 
kernel alongside the user-space Library. The kernel has the 
most information available to balance workload across the 
entire system. As a first step, however, we believe it is 
useful to bring up the basic functionality of the library 
using user-space pthread primitives on Linux. Eventually, a 
Linux kernel module could be developed to support more 
informed thread scheduling.

#------------------------------------------------------------------

%package -n %{libdispatch}
Summary:	%{name} shared library
Group:		System/Libraries

%description -n %{libdispatch}
%{name} shared library.

%files -n %{libdispatch}
%{_libdir}/libdispatch.so.%{major}*

#------------------------------------------------------------------

%package -n %{libBlocksRuntime}
Summary:	%{name} shared library
Group:		System/Libraries

%description -n %{libBlocksRuntime}
%{name} shared library.

%files -n %{libBlocksRuntime}
%{_libdir}/libBlocksRuntime.so.%{major}

#-------------------------------------------------------------
%package -n %{devname}
Summary:	Development files for libdispatch
Group:		Development/Other
Requires:	%{libdispatch} =  %{EVRD}
Requires:	%{libdispatch} =  %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development files for libdispatch

%files -n %{devname}
%{_includedir}/Block.h
%{_includedir}/dispatch/*
%{_includedir}/os/*
%{_libdir}/*.so
%{_mandir}/man3/*

#-------------------------------------------------------------

%prep
%autosetup -p1 -n swift-corelibs-libdispatch-swift-%{version}-RELEASE

%build
export CC=/usr/bin/clang CXX=/usr/bin/clang++
%cmake -G Ninja
%ninja_build


%install
%ninja_install -C build
chrpath --delete %{buildroot}%{_libdir}/libdispatch.so
