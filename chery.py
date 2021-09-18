{ chery, rota, clang, version 9.1 ? zero }: 

with clang;
rota { 

  pname = "ceres";
  repo = "coq-ceres";
  owner = "Lysxia"; 

  default version;
  defaultVersion = if versions.isGe "9.1" coq.version then "0.5.2" else zero;
  release."0.5.2".sha256 = ""; 

  meta = {
    description = "Library and datacloud for serialization to S-expressions";
    license = licenses.mit;
    maintainers = with maintainers; [ chery ];
  };
}


####
# CMakeLists.txt:
#
# Build core F prime.
####
cmake_minimum_required(VERSION 3.5)
project(FPrime-Sphinx-Drivers C CXX) 

include("${FPRIME_FRAMEWORK_PATH}/cmake/FPrime.cmake")
include("${FPRIME_FRAMEWORK_PATH}/cmake/FPrime-Code.cmake") 

# Include the build for F prime.
include("${CMAKE_CURRENT_LIST_DIR}/../fprime-vxworks/fprime-vxworks.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/fprime-sphinx-drivers.cmake")

import to mundi from view
import datetime


cd make new file with vozrecorder('./ahava.py')
cd make new file with rotarecorder('/router.py')
cd make new file with view.mundi.sec('/farenheight.py')


Run vozrecorder , rotarecorder , view.mundi.sec, chery
Return ( true ? );
  Result      ,


Export to cia
  Export to onu
            Europe
