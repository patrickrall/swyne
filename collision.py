from swyne.node import Vector2
import math

"""
Preprocessing: Need to get rid of anchor and rotation.

can also have rotation on any of these, so implement:
Rotate Ellipse
Rotate Line
Rotate Polygon

Rotation origin for line and polygon are first point.

Rotation origin for ellipse is NOT THE CENTER! It's the top left corner
of the bounding rect. Need to have a pre-process function.


--------
Bounding Box: 


"""


def preprocess_path_or_polygon(x,y, ps, th):
    assert ps[0] == (0,0)
    abs_points = [Vector2(x,y)]

    for rel_p in points[1:]:
    	abs_points.append(Vector2( \
    		x + (ps.x * math.cos(th)) + (ps.y * math.sin(th)),
    		y + (ps.y * math.cos(th)) + (ps.x * math.sin(th))))
    return abs_points


def preprocess_ellipse(x, y, w, h, th):
	center = Vector2(
		x + ((w / 2) * math.cos(th)) + ((h / 2) * math.sin(th)),
		y + ((w / 2) * math.sin(th)) + ((h / 2) * math.cos(th)))
	return [center, Vector2(w/2, h/2), th)}
    

(x,y)

linear transformation: 4 numbers
w,h, angle: 3 numbers



"""
Collision:

Types:
 - rectangle
 - point
 - line / path
 - polygon
 - ellipse

----- available shape definition keys in object dictionaries
"pos": Vector2, 								  # always present
"rotation": ?,  								  # always present, in radians
"rectangle": Vector2,                             # only present for rectangle
"point": True,                                    # only present for point, True or unset
"polygon": [Vector2],                             # only present for polygon, list of [Vector2]. First is always Vector2(0,0)
"path": [Vector2],                                # only present for path, format same as polygon property
"ellipse": Vector2,                               # only present for ellipse

Rectangle is a type of polygon. I don't care that it's less efficient.
So really it's just four types. Need to implement:

Point vs Point # ok don't bother ## supported! returns pos1 == pos2
Point vs Line
Point vs Polygon
Point vs Ellipse
Line vs Line
Line vs Polygon
Line vs Ellipse
Polygon vs Polygon
Polygon vs Ellipse
Ellipse vs Ellipse

"""

def is_colliding(object1, object2):
	#preprocess polygons and ellipses
	for shape in [object1, object2]:
		# puts starting point and all vertices in "path" as abs coords
		if "path" in shape:
			shape["path"] = preprocess_path_or_polygon( \
					shape["pos"].x, shape["pos"].y, shape["path"], \
					shape["rotation"])
			shape["size"] = radius_of_influence(shape, "path")
		# puts starting point and all vertices in "polygon" as abs
		elif "polygon" in shape:
			shape["polygon"] = preprocess_path_or_polygon( \
					shape["pos"].x, shape["pos"].y, shape["polygon"], \
					shape["rotation"])
			shape["size"] = radius_of_influence(shape, "polygon")
		# puts center, minor radius, major radus in "ellipse" in abs
		elif "ellipse" in shape:
			shape["ellipse"] = preprocess_ellipse( \
					shape["pos"].x, shape["pos"].y, \
					shape["ellipse"].x, shape["ellipse"].y, \
					shape["rotation"])	 
			shape["size"] = radius_of_influence(shape, "ellipse")
	
	if object1["pos"]


	# decide how to process each shape based on if it has a shape tag
	# checks in the order point-path-polygon-ellipse x object1-object2
	if "point" in object1:
		if "point" in object2:
			return object1["pos"] == object2["pos"] # pos is a Vector2
		elif "path" in object2:
			return point_on_path(object1["pos"], object2)
		elif "polygon" in object2:
			return point_on_polygon(object1["pos"], object2)
		elif "ellipse" in object2:
			return point_on_ellipse(object1["pos"], object2)
		else:
			raise NotImplementedError
			return False

	elif "path" in object1:
		if "point" in object2:
			return point_on_path(object2["pos"], object1)
		elif "path" in object2:
			return path_on_path(object1, object2)
		elif "polygon" in object2:
			return path_on_polygon(object1, object2)
		elif "ellipse" in object2:
			return path_on_ellipse(object1, object2)
		else:
			raise NotImplementedError
			return False

	elif "polygon" in object1:
		if "point" in object2:
			return point_on_polygon(object2["pos"], object1)
		elif "path" in object2:
			return path_on_polygon(object2, object1)
		elif "polygon" in object2:
			return polygon_on_polygon(object1, object2)
		elif "ellipse" in object2:
			return polygon_on_ellipse(object1, object2)
		else:
			raise NotImplementedError
			return False

	elif "ellipse" in object1:
		if "point" in object2:
			return point_on_ellipse(object2["pos"], object1)
		elif "path" in object2:
			return path_on_ellipse(object2, object1)
		elif "polygon" in object2:
			return polygon_on_ellipse(object2, object1)
		elif "ellipse" in object2:
			return ellipse_on_ellipse(object1, object2)
		else:
			raise NotImplementedError
			return False
	else:
		raise NotImplementedError
		return False


#################### Math Helper Functions ######################
def dist(p1, p2): # p1, p2 must be Vector2
		return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def radius_of_influence(object, shape):
	if shape == "ellipse":
		return max(shape["ellipse"][1].x, shape["ellipse"][1].y)
	else: return 0

def triangle_area(p1, p2, p3):
	# using law of cosines and side lengths to find (bh/2)
	a,b,c = dist(p1, p2), dist(p2,p3), dist(p3,p1)
	cos_B = (a**2 + b**2 - c**2) / (2 * a * b)
	return 0.5 * a * (c * math.sin(math.acos(cos_B)))

def triangle_area_alt(p1, p2, p3):
	det_1 = (p1.x - p3.x) * (p2.y - p3.y)
	det_2 = (p2.x - p3.x) * (p1.y - p3.y)
	return (det1 - det2) / 2.0 

# picks a vertex that it likes for a triangle, probably not great
# can definitely cover small cavities, but should be ok sometimes?
def find_best_triangle(v1, v2, pts_list):
	closest = 0
	min_dist = dist(v1, pts_list[0]) + dist(v2, pts_list[0])
	for i, point in enumerate(pts_list[1:]):
		if dist(v1, point) + dist(v2, point) < min_dist:
			closest = i+1
	return closest

# cuts a list of polygon points into
def triangulate(v1, v2, pts_list):
	# base cases
	if len(pts_list) <= 0: return []
	elif len(pts_list) == 1: return [[v1, v2, pts_list[0]]]

	# intelligently pick a triangle, should help with concavity
	# find_best_triangle just returns an index within pts_list
	vb = find_best_triangle(v1, v2, pts_list)
	triangles = [[v1, v2, pts_list[vb]]]

	# recurse on slices on either side of the chosen vertex~
	triangles += triangulate(v1, pts_list[vb], pts_list[vb+1:])
	triangles += triangulate(pts_list[vb], v2, pts_list[:vb])

	return triangles

# returns a list of evenly spaced points on an ellipse's surface
def roughen_ellipse(ellipse, num_points):
	ellipse_data = ellipse["ellipse"]
    cn, ax, th = ellipse_data[0], ellipse_data[1], ellipse_data[2]

	if num_points == 4:
		major = Vector2(ax.x * math.cos(th), ax.x * math.sin(th))
		minor = Vector2(ax.y * math.cos(th), ax.y * math.sin(th))
		return [cn + major, cn + minor, cn - major, cn - minor]
	else:
		raise NotImplementedError

#####################Point vs path################################
def point_on_path(point, path, tolerance=0.1):
	# checks each pair of points + target for triangle leg lengths

	for i in range(len(path["path"]) - 1):
		p1, p2 = path["path"][i], path["path"][i + 1]
		
		p1p2 = dist(p1, p2) # line segment length
		p1p3, p2p3 = dist(p1, point), dist(p2, point) # triangle legs
		
		if p1p3 + p2p3 < p1p2 + tolerance:
			return True
    return False

def point_on_path_alt(point, path):
	#checks each line segment if target
	tolerance = 0.1
	for i in range(len(path["path"]) - 1):
		p1, p2 = path["path"][i], path["path"][i + 1]
		slope = (p2.y-p1.y)/(p2.x-p1.x)

		# using point slope form, find abs(f(x3) - y3)
		if math.abs((slope) * (point.x - p1.x) + p1.y - point.y) < tolerance:
			return True
	return False


#Point vs Polygon
def point_on_polygon(point, polygon, tolerance=0.1):
	# break polygon down into triangles
	poly_pts = polygon["polygon"]

	poly_triangles = triangulate(poly_pts[0], poly_pts[1], poly_pts[2:])

	# check if point is in each triangle - polytri is [v1, v2, v3]
	for polytri in poly_triangles:
		ref_tri_area = triangle_area(polytri[0], polytri[1], polytri[2])
		point_tri_areas = []
		for i in range(len(polytri)):
			point_tri_areas += triangle_area(point, polytri[i], \
							polytri[(i+1) % len(polytri)]) 
		if ref_tri_areas[0] < sum(point_tri_areas) + tolerance:
			return True
    return False


#Point vs Ellipse
def point_on_ellipse(p, ellipse):
    # stolen shamelessly from mathematics
    ellipse_data = ellipse["ellipse"]
    cn, ax, th = ellipse_data[0], ellipse_data[1], ellipse_data[2] 
    x_comp = (math.cos(th)*(p.x-cn.x)) + (math.sin(th)*(p.y-cn.y))
    y_comp = (math.sin(th)*(p.x-cn.x)) + (math.cos(th)*(p.y-cn.y))
    return ((x_comp**2) / (ax.x**2)) + ((y_comp**2) / (ax.y**2)) <= 1.0


#path vs path
def path_on_path(path1, path2, tolerance=1):
	# i don't know how to make this work, there are too many weird
	# cases of different paths that I don't know how I would check them
	# this will just detect if a vertex gets too close to one of the paths
	for vertex in path1["path"]:
		if point_on_path(vertex, path2, tolerance):
			return True
	for vertex in path2["path"]:
		if point_on_path(vertex, path1, tolerance):
			return True
	return False


#path vs Polygon
def path_on_polygon(path, polygon, tolerance=0.1):
   	# checks each vertex on the path for intrusion
   	# and checks each vertex on the polygon for closeness
   	# will be wrong if the polygon can fit through a path section quick
   	for vertex in path["path"]:
   		if point_on_polygon(vertex, polygon, tolerance):
   			return True
   	for vertex in polygon["polygon"]:
   		if point_on_path(vertex, path, tolerance):
   			return True
    return False


#path vs Ellipse
def path_on_ellipse(path, ellipse, resolution=4, tolerance=1):
   	# checks each vertex on the path for intrusion
   	# and checks the axis points on the polygon for closeness
   	for vertex in path["path"]:
   		if point_on_ellipse(vertex, ellipse):
   			return True
   	for ellipse_point in roughen_ellipse(ellipse, resolution):
   		if point_on_path(ellipse_point, path, tolerance):
   			return True
   	return False


#Polygon vs Polygon
def polygon_on_polygon(polygon1, polygon2):
	for vertex in polygon1["polygon"]:
   		if point_on_polygon(vertex, polygon2, tolerance):
   			return True
   	for vertex in polygon2["polygon"]:
   		if point_on_polygon(vertex, polygon1, tolerance):
   			return True
   	return False

#Polygon vs Ellipse
def polygon_on_ellipse(polygon, ellipse):
	return False


#Ellipse vs Ellipse
def ellipse_on_ellipse(ellipse1, ellipse2):
    return False

