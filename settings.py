# Map generation
chunk = 1
in_time_chunks = 4
draw_vertexes = False

# Chunk generation

chunk_size_x = 450
chunk_size_y = 250
chunk_rect_n = 26
z_scale = 80
chunk_size = (chunk_rect_n - 1) * chunk_size_x  # is automatically generated
# Plane
flip_speed = 200
flip_return_ratio = 2
plane_start_position = [2875, 450, 350]
plane_moving_speed = 100

# Coins
coin_rotation_speed = 400

# Camera
camera_start_position = [2875, 600, 0]
moving_speed = 10
follow_moving_speed = plane_moving_speed
rotation_speed = 0.02
cam_start_angle = 0.3

# Main App

FPS = 90
height = 1080
width = 720