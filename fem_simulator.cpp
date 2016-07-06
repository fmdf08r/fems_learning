#include "volumetricMeshLoader.h"
#include "corotationalLinearFEM.h"
#include "corotationalLinearFEMForceModel.h"
#include "generateMassMatrix.h"
#include "implicitBackwardEulerSparse.h"
#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

/**
 * Parameters of the simulation
 **/
//string inputFileName = "../test.veg"; // mesh file name
const string inputFileName = "../tets/small_sphere.veg"; // second mesh
//string saveFileName = "../visualizations/sphere_";
const string output_data = "../data/ss_data.csv"; // current state
const string output_labels = "../data/ss_labels.csv"; // current velocity

// Gravity constant
const double g = 9.80665;

const int totalSimSteps = 18000; // 30 t-steps = 1 second
int r = 0; // number of degrees of freedom (DOFs) (i.e., number of particles * size of state for each particle)
const double timestep = 0.0333; // simulation timestep , in seconds

// this option only affects PARDISO and SPOOLES solvers, where it is best
// to keep it at 0, which implies a symmetric, non-PD solve.
// With CG this option is ignored.
const int positiveDefiniteSolver = 0;

// constrained DOFs
const int numConstrainedDOFs = 1;

// (tangential) Rayleigh damping
const double dampingMassCoef = 0.0; // "underwater"-like damping (here turned off)
const double dampingStiffnessCoef = 0.01; // (primarily) high-frequency damping

map<int, vector<vector<double> > > eleToVecMap;

int main(){
    cout << endl;
    cout << "******* SIMULATION RUNNER ******" << endl;

    // load mesh & its material properties into memory
    VolumetricMesh *vMesh = VolumetricMeshLoader::load(inputFileName.c_str());
    if (vMesh == NULL){
        printf("Error: failed to load mesh.\n");
    } else {
        printf("Success. Number of vertices: %d . Number of elements: %d . \n", vMesh->getNumVertices(), vMesh->getNumElements());
    }

    cout << endl;
    cout << "- Initializing tet mesh...";  
    // initialize a specific 3D deformable object: this allows to compute internal forces + stiffness matrices for arbitrary deformed object configurations
    TetMesh *tMesh;
    if(vMesh->getElementType()==VolumetricMesh::TET){
        tMesh = (TetMesh*) vMesh;
    } else {
        printf("Error: not a tet mesh.\n");
        exit(1);
    }
    r = 3 * tMesh->getNumVertices(); // total number of DOFs
    cout << "completed" << endl;

    cout << "- Initializing Finite Element Model...";
    CorotationalLinearFEM *fem = new CorotationalLinearFEM(tMesh);
    cout << "completed" << endl;

    cout << "- Initializing Force Model...";
    // create the class to connect the deformable model to the integrator
    ForceModel *fm = new CorotationalLinearFEMForceModel(fem);
    cout << "completed" << endl;

    cout << "- Generating mass matrix...";
    SparseMatrix *massMatrix;
    // create consistent (non-lumped) mass matrix
    GenerateMassMatrix::computeMassMatrix(tMesh, &massMatrix, true);   
    cout << "completed" << endl;

    // Constraining vertices
    cout << "- Constraining vertices...";
    int constrainedDOFs[1] = {245};
    cout << "completed" << endl;

    cout << "- Initializing Elements Map...";
    for(int el = 0; el < vMesh->getNumElements(); el++){
        vector<vector<double> > t_steps(totalSimSteps);
        eleToVecMap[el] = t_steps;
    }
    cout << "completed" << endl;
    cout << "- Initializing Backward Euler Integrator...";
    // initialize the integrator
    ImplicitBackwardEulerSparse *implicitBackwardEulerSparse = new ImplicitBackwardEulerSparse(
            r,
            timestep,
            massMatrix, 
            fm,
            positiveDefiniteSolver,
            numConstrainedDOFs,
            constrainedDOFs,
            dampingMassCoef,
            dampingStiffnessCoef);
    cout << "completed" << endl;
    cout << "- Set up initial conditions";
    double *initials = (double*) malloc (sizeof(double) * r);
    for(int vx = 0; vx < tMesh->getNumVertices(); vx++){
        Vec3d c = *tMesh->getVertex(vx);
        initials[3*vx + 0] = c[0];
        initials[3*vx + 1] = c[1];
        initials[3*vx + 2] = c[2];
    }
    implicitBackwardEulerSparse->SetState(initials);
    cout << "... completed" << endl;
    cout << endl;

    // create gravity force. 
    double *gravity = (double*) malloc (sizeof(double) * r);
    tMesh->computeGravity(gravity, g, false);

    cout << "- Running simulation: ";
    // allocate buffer to read the resulting displacement. 
    double *q = (double*) malloc (sizeof(double) * r);
    double *q_vel = (double*) malloc (sizeof(double) * r);
    double *q_acc = (double*) malloc (sizeof(double) * r);
    double *f_ext = (double*) malloc (sizeof(double) * r);

    for(int i=0; i < totalSimSteps; i++){
        cout << i << " - " << flush;
        if(i == 0){
            //implicitBackwardEulerSparse->SetExternalForcesToZero();
            implicitBackwardEulerSparse->SetExternalForces( gravity );
            delete gravity;
        }

        implicitBackwardEulerSparse->DoTimestep();
        implicitBackwardEulerSparse->GetqState(q, q_vel, q_acc);
        implicitBackwardEulerSparse->GetExternalForces(f_ext);

        for(int k=0; k < r-1; k++){ // implement bouncing
            if( (k-1) % 3 == 0 ){
                if( q[k] <= 0 && q_vel[k] < 0){
                    q_vel[k] = -q_vel[k];
                }
            }
        }

        implicitBackwardEulerSparse->SetqState(q,q_vel,q_acc);

        for(int e = 0; e < tMesh->getNumElements(); e++){
            vector<int> elements(1, e);
            vector<int> vertices;
            tMesh->getVerticesInElements(elements, vertices);

            for(int v : vertices){
                eleToVecMap[e][i].push_back(q[3*v + 0]);
                eleToVecMap[e][i].push_back(q[3*v + 1]);
                eleToVecMap[e][i].push_back(q[3*v + 2]);
                eleToVecMap[e][i].push_back(q_vel[3*v + 0]);
                eleToVecMap[e][i].push_back(q_vel[3*v + 1]);
                eleToVecMap[e][i].push_back(q_vel[3*v + 2]);
                eleToVecMap[e][i].push_back(f_ext[3*v + 0]);
                eleToVecMap[e][i].push_back(f_ext[3*v + 1]);
                eleToVecMap[e][i].push_back(f_ext[3*v + 2]);
            }
        }
    }
    cout << "completed" << endl;

    // print everything
    cout << "- Size of Map to print: (" << eleToVecMap.size() * (totalSimSteps - 1) << " x 36)"<< endl;
    cout << "- Printing to File ";
    ofstream oData;
    ofstream oLabels;

    /**
    oData.open(output_data);
    oLabels.open(output_labels);

    for(int el = 0; el < tMesh->getNumElements(); el++){
        for(int t = 0; t < totalSimSteps - 1; t++){
            // only print velocities as labels
            oLabels << eleToVecMap[el][t+1][3] << ", " << eleToVecMap[el][t+1][4] << ", " << eleToVecMap[el][t+1][5] << ", ";
            oLabels << eleToVecMap[el][t+1][12] << ", " << eleToVecMap[el][t+1][13] << ", " << eleToVecMap[el][t+1][14] << ", ";
            oLabels << eleToVecMap[el][t+1][21] << ", " << eleToVecMap[el][t+1][22] << ", " << eleToVecMap[el][t+1][23] << ", ";
            oLabels << eleToVecMap[el][t+1][30] << ", " << eleToVecMap[el][t+1][31] << ", " << eleToVecMap[el][t+1][32];

            for(int i = 0; i < 36;i++){
                oData << eleToVecMap[el][t][i];
                //oLabels << eleToVecMap[el][t+1][i];
                if (i < 35){
                    oData << ", ";
                    //oLabels << ", ";
                }
            }
            oData << endl;
            oLabels << endl;
        }
    }
    oData.close();
    oLabels.close();
    **/
    
    // files for tet visualization
    for(int t = 0; t < totalSimSteps; t++){        
        ofstream objData;
        objData.open("../data/obj_files/obj_info_" + to_string(t) +  ".csv");
        
        // header
        objData << "el,";
        objData << "v1,v2,v3,v4,";
        objData << "t,";
        objData << "p1x,p1y,p1z,";
        objData << "p2x,p2y,p2z,";
        objData << "p3x,p3y,p3z,"; 
        objData << "p4x,p4y,p4z,"; 
        objData << "v1x,v1y,v1z,";
        objData << "v2x,v2y,v2z,";
        objData << "v3x,v3y,v3z,"; 
        objData << "v4x,v4y,v4z,";
        objData << "f1x,f1y,f1z,";
        objData << "f2x,f2y,f2z,"; 
        objData << "f3x,f3y,f3z,"; 
        objData << "f4x,f4y,f4z";  
        objData << endl;
        
        for(int el = 0; el < tMesh->getNumElements(); el++){
            objData << el << ",";
        
            // vertices
            vector<int> elements(1, el);
            vector<int> vertices;
            tMesh->getVerticesInElements(elements, vertices);
        
            for(int v : vertices){
                objData << v << ",";
            }

            objData << t << ",";
            objData << eleToVecMap[el][t][0] << "," << eleToVecMap[el][t][1] << "," << eleToVecMap[el][t][2] << ","; // p1
            objData << eleToVecMap[el][t][9] << "," << eleToVecMap[el][t][10] << "," << eleToVecMap[el][t][11] << ","; // p2
            objData << eleToVecMap[el][t][18] << "," << eleToVecMap[el][t][19] << "," << eleToVecMap[el][t][20] << ","; // p3
            objData << eleToVecMap[el][t][27] << "," << eleToVecMap[el][t][28] << "," << eleToVecMap[el][t][29] << ","; // p4
            
            objData << eleToVecMap[el][t][3] << "," << eleToVecMap[el][t][4] << "," << eleToVecMap[el][t][5] << ","; // v1
            objData << eleToVecMap[el][t][12] << "," << eleToVecMap[el][t][13] << "," << eleToVecMap[el][t][14] << ","; // v2
            objData << eleToVecMap[el][t][21] << "," << eleToVecMap[el][t][22] << "," << eleToVecMap[el][t][23] << ","; // v3
            objData << eleToVecMap[el][t][30] << "," << eleToVecMap[el][t][31] << "," << eleToVecMap[el][t][32] << ","; // v4

            objData << eleToVecMap[el][t][6] << "," << eleToVecMap[el][t][7] << "," << eleToVecMap[el][t][8] << ","; // f1
            objData << eleToVecMap[el][t][15] << "," << eleToVecMap[el][t][16] << "," << eleToVecMap[el][t][17] << ","; // f2
            objData << eleToVecMap[el][t][24] << "," << eleToVecMap[el][t][25] << "," << eleToVecMap[el][t][26] << ","; // f3
            objData << eleToVecMap[el][t][33] << "," << eleToVecMap[el][t][34] << "," << eleToVecMap[el][t][35]; // f4
            objData << endl;
        }
        objData.close();
    }

    cout << "...completed" << endl;

    delete q;
    delete q_vel;
    delete q_acc;
    delete f_ext;
}
