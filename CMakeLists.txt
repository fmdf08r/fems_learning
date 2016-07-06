cmake_minimum_required(VERSION 3.3)

project(LearningFEMs) 

set(SOURCE_FILES
    fem_simulator.cpp
    )

#set(HEADER_FILES volumetricMesh.h)

include_directories(${testVEGA_SOURCE_DIR}/.)
include_directories($ENV{VEGA_DIR}/libraries/include)
link_directories($ENV{VEGA_DIR}/libraries/lib/)
add_executable(LearningFEMs ${SOURCE_FILES})

target_link_libraries(LearningFEMs 
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


