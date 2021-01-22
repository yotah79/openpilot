/******************************************************************************
 *                       Code generated with sympy 1.4                        *
 *                                                                            *
 *              See http://www.sympy.org/ for more information.               *
 *                                                                            *
 *                         This file is part of 'ekf'                         *
 ******************************************************************************/
void err_fun(double *nom_x, double *delta_x, double *out_3906977837352698463);
void inv_err_fun(double *nom_x, double *true_x, double *out_367371526983327903);
void H_mod_fun(double *state, double *out_1282326894958700794);
void f_fun(double *state, double dt, double *out_2218022952283072833);
void F_fun(double *state, double dt, double *out_4168449100878208170);
void h_3(double *state, double *unused, double *out_606097172959107911);
void H_3(double *state, double *unused, double *out_6303830411083569863);
void h_4(double *state, double *unused, double *out_2028880912738113046);
void H_4(double *state, double *unused, double *out_2089251393154212868);
void h_9(double *state, double *unused, double *out_3063276975560243411);
void H_9(double *state, double *unused, double *out_5877405207874280140);
void h_10(double *state, double *unused, double *out_7482719075154554828);
void H_10(double *state, double *unused, double *out_7482087534076486602);
void h_12(double *state, double *unused, double *out_5231810314174083135);
void H_12(double *state, double *unused, double *out_3243579174481992836);
void h_13(double *state, double *unused, double *out_988565506603265442);
void H_13(double *state, double *unused, double *out_6000281052544456206);
void h_14(double *state, double *unused, double *out_3063276975560243411);
void H_14(double *state, double *unused, double *out_5877405207874280140);
void h_19(double *state, double *unused, double *out_4576836792907702387);
void H_19(double *state, double *unused, double *out_5201517699649548016);
#define DIM 23
#define EDIM 22
#define MEDIM 22
typedef void (*Hfun)(double *, double *, double *);

void predict(double *x, double *P, double *Q, double dt);
const static double MAHA_THRESH_3 = 3.841459;
void update_3(double *, double *, double *, double *, double *);
const static double MAHA_THRESH_4 = 7.814728;
void update_4(double *, double *, double *, double *, double *);
const static double MAHA_THRESH_9 = 7.814728;
void update_9(double *, double *, double *, double *, double *);
const static double MAHA_THRESH_10 = 7.814728;
void update_10(double *, double *, double *, double *, double *);
const static double MAHA_THRESH_12 = 7.814728;
void update_12(double *, double *, double *, double *, double *);
const static double MAHA_THRESH_13 = 7.814728;
void update_13(double *, double *, double *, double *, double *);
const static double MAHA_THRESH_14 = 7.814728;
void update_14(double *, double *, double *, double *, double *);
const static double MAHA_THRESH_19 = 7.814728;
void update_19(double *, double *, double *, double *, double *);