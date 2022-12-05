import numpy as np
import pyopencl as cl
import os
from PIL import Image

os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

img = Image.open("testbild_alpha.png")
img_array = np.asarray(img)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
input_buffer = cl.image_from_array(ctx, img_array, 4)

program = cl.Program(ctx, """
float linear_to_srgb(float x) {
    return ((x > 0.0031308) * (1.055 * pow(x, (1.0f / 2.4f)) - 0.055) + (x <= 0.0031308) * (x * 12.92));

}
__kernel void enhance(
    read_only image2d_t input_buffer,
    write_only image2d_t result_buffer
    )
{
  const sampler_t sampler =  CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;
  int2 pos = (int2)(get_global_id(1), get_global_id(0));
  uint4 pixel = read_imageui(input_buffer, sampler, pos);
  pixel = (uint4)((uint)(linear_to_srgb(pixel.r /255.0)*255), (uint)(linear_to_srgb(pixel.g/255.0)*255), (uint)(linear_to_srgb(pixel.b/255.0)*255), pixel.a);
  write_imageui(result_buffer, pos, pixel);
}
""").build()
fmt = cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNSIGNED_INT8)
result_buffer = cl.Image(ctx, mf.WRITE_ONLY, fmt, shape=(img.width, img.height))
kernel = program.enhance  # Use this Kernel object for repeated calls
kernel(queue, img_array.shape, None, input_buffer, result_buffer)

result_array = np.empty_like(img_array)
cl.enqueue_copy(queue, result_array, result_buffer, origin=(0, 0), region=(img.width, img.height))
Image.fromarray(result_array).show()
