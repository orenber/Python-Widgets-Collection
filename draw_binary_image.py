import numpy as np
from skimage import morphology


def plot_binary_image(mask: np.array, x_data: np.array =None, y_data: np.array= None):

    mat = np.vstack((np.array(x_data),np.array(y_data)))
    matrix = mat.transpose()

    start_point = matrix[0:-1]
    end_point = matrix[1:]
    lines_matrix_list = list()
    lines_matrix_list.append((list(start_point), list(end_point)))
    lines_matrix = lines_matrix_list[0]

    # for every row get the appropriate linear equation
    length = len(lines_matrix_list[0][1])
    point_x = []
    point_y = []

    for n in range(length):

        x1 = lines_matrix[0][n][0]
        y1 = lines_matrix[0][n][1]

        x2 = lines_matrix[1][n][0]
        y2 = lines_matrix[1][n][1]

        fun = create_line(x1, y1, x2, y2)
        x_sort = sorted([x1, x2])
        initial = x_sort[0]
        final = x_sort[1]
        if initial == final:
            continue

        interval = np.arange(initial, final, 0.01)
        point_x.append(np.round(interval))
        point_y.append(np.round(fun(interval)))

        if initial == final:
            x_array = np.kron((point_y[n]), interval)
            point_x.append(list(x_array))

    # for every linear equation get the pixel
    pixel_x = np.array(np.concatenate(point_x))
    pixel_y = np.array(np.concatenate(point_y))

    # fix the index to the image size
    index_x = (pixel_x > 0) & (pixel_x < mask.shape[0])
    index_y = (pixel_y > 0) & (pixel_y < mask.shape[1])
    index = index_x & index_y

    pixel_image_size_fix_x = pixel_x[index]
    pixel_image_size_fix_y = pixel_y[index]
    row_index = list(pixel_image_size_fix_y.astype(int))
    col_index = list(pixel_image_size_fix_x.astype(int))

    # plot the pixels
    mask[row_index, col_index] = True


    # binary dilation
    disk = morphology.selem.disk(1, dtype=np.bool)
    mask_image = morphology.binary_dilation(mask, selem=disk)

    return mask_image


def create_line(x1: float, y1: float, x2: float,y2: float):

    if x1 == x2:

        y_sorted = sorted([y1, y2])
        a = y_sorted[0]
        b = y_sorted[1]

        anonymous_function = lambda x: range(a, b, 0.01)

    else:

        coefficients = np.polyfit([x1, x2], [y1, y2], 1)
        a = coefficients[0]
        b = coefficients[1]
        anonymous_function = lambda x: a*x+b

    return anonymous_function