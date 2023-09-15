import numpy as np
from scipy.linalg import solve

# Define the corresponding points
src_points = np.array([
    [1003.9286756661193, 6219.173261322787, -0.9506062064929727],
    [1004.4084047331409, 6219.4633171383175, -0.9481987150762584],
    [
			1006.4776614382538,
			6219.463398240616,
			-0.9460014561146647
		],
		[
			1004.102411805066,
			6220.203203729848,
			-0.9436585457230725
		],
		[
			1002.8010281939364,
			6220.609051781263,
			-0.9423662359986147
		],
		[
			1004.8200831880487,
			6220.564266544223,
			-0.9405093334013753
		],
		[
			1006.966073519169,
			6220.453616854667,
			-0.9389446881159013
		]
])

dst_points = np.array([
    [24.07954, -184.04687, 19.9905],
    [13.68084, -140.9956, 19.10391],
    [-9.68999, -102.80228, 17.92118],
    [22.72815, -58.14626, 16.52381],
    [42.29524, -34.47619, 15.78236],
    [16.0181, -8.72164, 15.6544],
    [-20.00318, 26.15043, 15.53423]
    
])

# Adding a column of ones to the source points to work with homogenous coordinates
src_points_homogeneous = np.hstack((src_points, np.ones((src_points.shape[0], 1))))

# Finding the transformation matrix by solving the linear system
A, res, rank, s = np.linalg.lstsq(src_points_homogeneous, dst_points, rcond=None)

# To transform new points using the found transformation matrix, 
# create an array of points you want to transform (with a column of ones for homogeneous coordinates)
# new_points = np.array([[x1, y1, z1, 1], [x2, y2, z2, 1], ...])

# Then use np.dot to apply the transformation matrix to the new points
# transformed_points = np.dot(new_points, A)

# Note: For finding an accurate transformation matrix, it's recommended to have at least 4 corresponding point pairs.


np.save('transformation_matrix.npy', A)

A_loaded = np.load('transformation_matrix.npy')

new_points = np.array([[			1012.9526086217902,
			6220.57126117379,
			-0.931698018321944,1]])

# Use np.dot to apply the transformation matrix to the new points
transformed_points = np.dot(new_points, A_loaded)

print("Transformed points:")
print(transformed_points)