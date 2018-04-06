cmake_minimum_required(VERSION 2.8.3)
project(modem)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  diagnostic_msgs
)

add_message_files(
  FILES
  target.msg
  dataMessage.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs  # Or other packages containing msgs
  diagnostic_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs
  DEPENDS Boost)
include_directories(
  ${catkin_INCLUDE_DIRS}
)
