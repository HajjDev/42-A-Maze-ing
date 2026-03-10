import sys
sys.path.append('../')
from mlx import Mlx
import struct

def gere_close(param):
    m.mlx_loop_exit(mlx_ptr)
    return 0

m = Mlx()
mlx_ptr = m.mlx_init()
mlx_win = m.mlx_new_window(mlx_ptr, 1920, 1080, "Hello World")
img = m.mlx_new_image(mlx_ptr, 1920, 1080)
img_buffer, bpp, line_len, endian = m.mlx_get_data_addr(img)
color = 0xFFFF0000
pixel_size = bpp // 8
byteorder = 'little' if endian == 0 else 'big'
for y in range(10):
    for x in range(100):
        index = y * line_len + x * pixel_size
        img_buffer[index:index+pixel_size] = color.to_bytes(pixel_size, byteorder)
m.mlx_hook(mlx_win, 33, 0, gere_close, None)
m.mlx_put_image_to_window(mlx_ptr, mlx_win, img, 100, 100)
m.mlx_put_image_to_window(mlx_ptr, mlx_win, img, 150, 200)
m.mlx_loop(mlx_ptr)