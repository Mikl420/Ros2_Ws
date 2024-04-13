# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_vl53l1x_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED vl53l1x_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(vl53l1x_FOUND FALSE)
  elseif(NOT vl53l1x_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(vl53l1x_FOUND FALSE)
  endif()
  return()
endif()
set(_vl53l1x_CONFIG_INCLUDED TRUE)

# output package information
if(NOT vl53l1x_FIND_QUIETLY)
  message(STATUS "Found vl53l1x: 0.1.2 (${vl53l1x_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'vl53l1x' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${vl53l1x_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(vl53l1x_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${vl53l1x_DIR}/${_extra}")
endforeach()
