import numpy as np


def get_RGB_to_XYZ_matrix(XYZr, XYZg, XYZb, XYZw):
    Xr, Yr, Zr = XYZr
    Xg, Yg, Zg = XYZg
    Xb, Yb, Zb = XYZb
    Xw, Yw, Zw = XYZw
    XYZ_to_RGB_matrix = np.array([Xr, Xg, Xb],
                                 [Yr, Yg, Yb],
                                 [Zr, Zg, Zb])

    XwYwZw_vector = np.array([Xw, Yw, Zw])
    SrSgSb_vector = XYZ_to_RGB_matrix / XwYwZw_vector

    return XYZ_to_RGB_matrix * [SrSgSb_vector, SrSgSb_vector, SrSgSb_vector]
