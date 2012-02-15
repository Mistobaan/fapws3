# -*- coding: utf-8 -*-
from setuptools import setup, find_packages, Extension
import os
import sys
import os.path
import distutils.sysconfig
import platform

def read_file(name):
    return open(os.path.join(os.path.dirname(__file__),name)).read()

def find_file(fname, dirs):
    founded=False
    for ckdir in dirs:
        fpname=os.path.join(ckdir,fname)
        if os.path.isfile(fpname):
            founded=True
        #we don't find it, it can be located into a subdirectory ;-)
        localdirs=[]
        try:
            elems=os.listdir(ckdir)
        except:
            elems=[]
        for elem in elems:
            fpname=os.path.join(ckdir,elem)
            if os.path.isdir(fpname):
                localdirs.append(fpname)
            if elem[:len(fname)]==fname:
                founded=True
                break
        if founded:
            print "----------Find",fname," in ", ckdir
            return ckdir
        if localdirs:
            res=find_file(fname,localdirs)
            if res:
                return res
    return False            

readme = read_file('README.markdown')

if "posix" not in os.name:
    print "Are you really running a posix compliant OS ?"
    print "Be posix compliant is mandatory"
    sys.exit(1)

search_library_dirs=[]
search_include_dirs=[]
library_dirs=[]
include_dirs=[]


#we add, at the begining of the list, the existing environemental variables
if os.environ.has_key('C_INCLUDE_PATH'):
    search_include_dirs.extend(os.environ['C_INCLUDE_PATH'].split(os.pathsep))
if os.environ.has_key('LD_LIBRARY_PATH'):
    search_library_dirs.extend(os.environ['LD_LIBRARY_PATH'].split(os.pathsep))
if os.environ.has_key('LIBPATH'):
    search_library_dirs.append(os.path.join(os.environ['LIBPATH'],'lib'))
    search_include_dirs.append(os.path.join(os.environ['LIBPATH'],'include'))



#anyhow we include the standards directories
search_library_dirs.extend(['/usr/lib','/usr/local/lib','/opt/local/lib','/usr/lib64','/usr/pkg/lib/ev'])
if sys.platform == "darwin":
    search_include_dirs.extend(['/usr/local/include','/opt/local/include','/usr/pkg/include/ev'])
else:
    search_include_dirs.extend(['/usr/include','/usr/local/include','/opt/local/include','/usr/pkg/include/ev'])

version = platform.python_version_tuple()
if int(version[0])==2 and int(version[1])>=4:
    print "Find python 2.4 or higher"
else:
    print "Fapws has been developped with python 2.4 or higher (not yet python 3.X). Instead we found python %s.%s" % (version[0], version[1])
    sys.exit(1)

def assert_resource_and_append_if_found(filename, search_paths, env_name, res_list):
    res = find_file(filename, search_paths)
    if res == False:
        print "Warning: We don't find %s which is a mandatory file to compile Fapws" % filename
        print "Directory searched: %s" % '\t'.join(search_paths)
        print "Please install the sources of libev, or provide the path by setting the shell environmental variable %s "% env_name
        #sys.exit(1)
    res_list.append(res)

assert_resource_and_append_if_found('ev.h', search_include_dirs, 'C_INCLUDE_PATH', include_dirs)
assert_resource_and_append_if_found('Python.h', search_include_dirs, 'C_INCLUDE_PATH', [distutils.sysconfig.get_python_inc()])
if sys.platform == 'darwin':
    assert_resource_and_append_if_found('libev.dylib', search_include_dirs, 'DYLD_LIBRARY_PATH', library_dirs)
else:
    assert_resource_and_append_if_found('libev.a', search_include_dirs, 'LD_LIBRARY_PATH', library_dirs)
    assert_resource_and_append_if_found('libev.so', search_include_dirs, 'LD_LIBRARY_PATH', library_dirs)
               
extra_link_args=['-Wl']

setup(name='fapws3',
      version="0.10",
      description="Fast Asynchronous Python Web Server",
      long_description=readme,
classifiers=['Development Status :: 4 - Beta','Environment :: Web Environment','License :: OSI Approved :: GNU General Public License (GPL)','Programming Language :: C','Programming Language :: Python','Topic :: Internet :: WWW/HTTP :: HTTP Servers','Topic :: Internet :: WWW/HTTP :: WSGI :: Server'], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='William',
      author_email='william.os4y@gmail.com',
      url='http://www.fapws.org',
      license='GPL',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,

      packages= find_packages(),
      ext_modules = [
          Extension('fapws._evwsgi',
                  depends=['fapws/extra.h','fapws/wsgi.h','fapws/mainloop.h','fapws/common.h'],
                  sources=['fapws/extra.c', 'fapws/wsgi.c','fapws/mainloop.c','fapws/_evwsgi.c'],
                  include_dirs=include_dirs,
                  libraries=['ev'],
                  #library_dirs=library_dirs, 
                  #extra_link_args=extra_link_args, #comment this line if you prefer to play with LD_LIBRARY_PATH
                  #extra_compile_args=["-ggdb"],
                  #define_macros=[("DEBUG", "1")],
                  )
                  ]
      )


# end of file: setup.py
