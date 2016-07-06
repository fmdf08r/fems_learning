cmake_minimum_required(VERSION 3.3)

project(testVEGA) 

set(SOURCE_FILES
    test.cpp
    )

#set(HEADER_FILES volumetricMesh.h)

include_directories(${testVEGA_SOURCE_DIR}/.)
include_directories($ENV{VEGA_DIR}/libraries/include)
link_directories($ENV{VEGA_DIR}/libraries/lib/)
add_executable(testVEGA ${SOURCE_FILES})

target_link_libraries(testVEGA 
camera
clothBW
configFile
corotationalLinearFEM
elasticForceModel
forceModel
getopts
graph
imageIO
integrator
integratorSparse
isotropicHyperelasticFEM
lighting
loadList
massSpringSystem
matrixIO
minivector
objMesh
objMeshGPUDeformer
polarDecomposition
sceneObject
sparseMatrix
sparseSolver
stvk
volumetricMesh
insertRows
)


