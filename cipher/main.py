#!./.venv/bin/python3
import argparse
import struct
import png

HEADER_SIZE = 8  # bytes (unsigned long long)

def bytes_to_bits(data):
    for byte in data:
        for i in range(7, -1, -1):
            yield (byte >> i) & 1

def bits_to_bytes(bits):
    out = bytearray()
    cur = 0
    count = 0
    for bit in bits:
        cur = (cur << 1) | bit
        count += 1
        if count == 8:
            out.append(cur)
            cur = 0
            count = 0
    return bytes(out)

def encode(
        payload_path,
        cover_png_path,
        output_png_path,
        capacity_check=False
    ):
    with open(payload_path, "rb") as f:
        payload = f.read()

    payload_len = len(payload)
    header = struct.pack(">Q", payload_len)
    data = header + payload
    bits = list(bytes_to_bits(data))
    required_bits = len(bits)

    reader = png.Reader(filename=cover_png_path)
    width, height, rows, info = reader.read()

    planes = info["planes"]  # 3 = RGB, 4 = RGBA
    if planes not in (3, 4):
        raise ValueError("Unsupported PNG format")

    capacity_bits = width * height * 3
    if capacity_check:
        print("Capacity check:")
        print(f"  Usable channels  : RGB")
        print(f"  Image dimensions : {width} x {height}")
        print(f"  Capacity         : {capacity_bits} bits")
        print(f"  Required         : {required_bits} bits")
        print(f"  Margin           : {capacity_bits - required_bits} bits")
        return
    # --
    if required_bits > capacity_bits:
        raise ValueError("Payload too large for this image")
    # --
    pixels = []
    for row in rows:
        pixels.extend(row)
    # --
    bit_idx = 0
    for i in range(0, len(pixels), planes):
        for c in range(3):  # R, G, B only
            if bit_idx >= required_bits:
                break
            pixels[i + c] = (pixels[i + c] & ~1) | bits[bit_idx]
            bit_idx += 1
    # --
    stride = width * planes
    new_rows = [
        pixels[y * stride : (y + 1) * stride]
        for y in range(height)
    ]
    with open(output_png_path, "wb") as f:
        writer = png.Writer(
            width,
            height,
            greyscale=False,
            alpha=(planes == 4)
        )
        writer.write(f, new_rows)
    print(f"Encoded {payload_len} bytes into {output_png_path}")

def decode(stego_png_path, output_payload_path):
    reader = png.Reader(filename=stego_png_path)
    width, height, rows, info = reader.read()
    # --
    planes = info["planes"]
    if planes not in (3, 4):
        raise ValueError("Unsupported PNG format")
    # --
    bits = []
    for row in rows:
        for i in range(0, len(row), planes):
            for c in range(3):  # R, G, B only
                bits.append(row[i + c] & 1)
    # --
    header_bits = bits[: HEADER_SIZE * 8]
    header = bits_to_bytes(header_bits)
    payload_len = struct.unpack(">Q", header)[0]
    payload_bits = bits[
        HEADER_SIZE * 8 : HEADER_SIZE * 8 + payload_len * 8
    ]
    payload = bits_to_bytes(payload_bits)
    with open(output_payload_path, "wb") as f:
        f.write(payload)
    print(f"Decoded {payload_len} bytes to {output_payload_path}")


def main():
    parser = argparse.ArgumentParser(description="LSB steganography using PyPNG")
    sub = parser.add_subparsers(dest="cmd", required=True)

    enc = sub.add_parser("encode", help="Hide binary data in a PNG")
    enc.add_argument("payload", help="Binary file to hide")
    enc.add_argument("image", help="Cover PNG image (RGB)")
    enc.add_argument("output", help="Output stego PNG")
    enc.add_argument(
        "--capacity",
        action="store_true",
        help="Compare payload size to image storage capacity and exit"
    )
    dec = sub.add_parser("decode", help="Extract binary data from a PNG")
    dec.add_argument("image", help="Stego PNG image")
    dec.add_argument("output", help="Recovered binary file")
    args = parser.parse_args()

    if args.cmd == "encode":
        if args.cmd == "encode":
            encode(
                args.payload,
                args.image,
                args.output,
                capacity_check=args.capacity
            )
    elif args.cmd == "decode":
        decode(args.image, args.output)


if __name__ == "__main__":
    main()

