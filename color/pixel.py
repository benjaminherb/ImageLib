from color import COLOR_SPACE_PRIMARIES, TRANSFER_CURVES, WHITE_POINTS
import numpy as np
import pyopencl as cl

class Pixel:
    def __init__(self, X, Y, Z):
        self.XYZ = np.array([X, Y, Z])


def get_pixel_from_rgb(r, g, b, primaries="rec709",
                       white_point="D65", transfer_curve="linear", gamma=2.2):
    rgb = np.array([r, g, b])
    if primaries not in COLOR_SPACE_PRIMARIES:
        raise Exception(f"Unknown primaries. Possible values are: {COLOR_SPACE_PRIMARIES}")

    if white_point not in WHITE_POINTS:
        raise Exception(f"Unknown white point. Possible values are: {WHITE_POINTS}")

    if transfer_curve not in TRANSFER_CURVES:
        raise Exception(f"Unknown transfer curve. Possible values are: {TRANSFER_CURVES}")

    # linearize
    rgb = _to_lin(rgb, transfer_curve, gamma)


def _to_lin(rgb, transfer_curve, gamma=None):
    if transfer_curve == "linear":
        return rgb
    elif transfer_curve == "gamma":
        if not gamma:
            raise Exception(f"Transfer curve 'gamma' specified but no value provided")
        return np.power(rgb, 1.0 / gamma)
    elif transfer_curve == "srgb":
        pass


def _from_lin(rgb, transfer_curve, gamma=None):

    if transfer_curve == "srgb":
        pass



# testing
get_pixel_from_rgb(0.2, 0.4, 0.2, transfer_curve="gamma", gamma=2.2)


def linear_to_srgb(x):
    return ((x > 0.0031308) * (1.055 * pow(x, (1 / 2.4)) - 0.055)
            + (x <= 0.0031308) * (x * 12.92))


