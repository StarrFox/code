cmake_minimum_required(VERSION 3.27.7)

project(test_project C)

add_executable(test src/main.c)

install(TARGETS test DESTINATION bin)
