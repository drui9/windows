# Reading PNG Files
```python3
import png

# Read a PNG file
reader = png.Reader(filename='image.png')
width, height, pixels, metadata = reader.read()

# Access basic information
print(f"Image size: {width}x{height}")
print(f"Metadata: {metadata}")

# Convert pixels to list
pixel_list = list(pixels)
```

# Writing PNG Files
```python
import png

# Create from array
image_2d = [[255, 0, 0],    # Red pixel
            [0, 255, 0],    # Green pixel
            [0, 0, 255]]    # Blue pixel

# Save as PNG
png.from_array(image_2d, 'RGB').save("output.png")

# Write with more control
writer = png.Writer(width=3, height=3, bitdepth=8, greyscale=False)
with open('output.png', 'wb') as f:
    writer.write(f, image_2d)
```

