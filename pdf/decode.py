"""Simple decoder for CCITT-encoded data.

To decode (decompress) data (at least, image data) that has been encoded with
CCITT compression, without writing/using a CCITT decoder, we can use a trick:
wrap it inside a TIFF header, and treat the result as a TIFF file. So now, we
can use tools that work with TIFF files (as there are many, and they probably
already contain a CCITT decoder internally).

This is especially useful for any region in a PDF file that is intended to be
decoded with the /CCITTFaxDecode ("CCITT facsimile (fax) encoding") filter."""

import re
import struct


def tiff_header_for_CCITT(width, height, img_size, CCITT_group=4, blackIsZero=False):
    """Returns the appropriate header that will make it a valid TIFF file."""
    tiff_header_struct = '<' + '2s' + 'h' + 'l' + 'h' + 'hhll' * 8 + 'h'
    return struct.pack(tiff_header_struct,
                       b'II',  # Byte order indication: Little-endian
                       42,  # Version number (always 42)
                       8,  # Offset to first IFD
                       8,  # Number of tags in IFD
                       256, 4, 1, width,  # ImageWidth, LONG, 1, width
                       257, 4, 1, height,  # ImageLength, LONG, 1, length
                       258, 3, 1, 1,  # BitsPerSample, SHORT, 1, 1
                       259, 3, 1, CCITT_group,  # Compression, SHORT, 1, 4 = CCITT Group 4 fax encoding
                       262, 3, 1, int(blackIsZero),  # Threshholding, SHORT, 1, 0 = WhiteIsZero
                       273, 4, 1, struct.calcsize(tiff_header_struct),  # StripOffsets, LONG, 1, len of header
                       278, 4, 1, height,  # RowsPerStrip, LONG, 1, length
                       279, 4, 1, img_size,  # StripByteCounts, LONG, 1, size of image
                       0  # last IFD
                       )


def decode_ccitt_data(data, width, height, CCITT_group=4, blackIsZero=False):
    """Decodes CCITT-encoded data, if its intended width, height, etc are known."""
    img_size = len(data)
    tiff_header = tiff_header_for_CCITT(width, height, img_size, CCITT_group)
    return tiff_header + data


def decode_cccitt_data_to_file(data, width, height, out_filename, CCITT_group=4, blackIsZero=False):
    with open(out_filename, 'wb') as img_file:
        img_file.write(decode_ccitt_data(data, width, height, CCITT_group, blackIsZero))


def extract_imagedata_from_pdf(filename):
  """A VERY hacky function to look for stuff inside BI ... ID ... EI tags, and try to extract it.
  Won't work with most PDFs; designed for a very specific PDF file processed with mutool."""
  lines open(filename, 'rb').readlines()
  i = -1
  found_objs = set()
  while i + 1 < len(lines):
    i += 1
    if not lines[i].startswith('ID'): continue

    width = None
    height = None
    # Go back, till we find the 'BI'
    h = i - 1
    while not lines[h].startswith('BI'):
      if '/W ' in lines[h]: width = int(re.search('/W ([^/]*)', lines[h]).group(1))
      if '/H ' in lines[h]: height = int(re.search('/H ([^/]*)', lines[h]).group(1))
      h -= 1
    assert width is not None
    assert height is not None

    # Go further back, till we find the "n 0 obj"
    while not (m = re.search('([0-9]*) 0 obj', lines[h])):
      h -= 1
    obj_num = int(m.group(1))
    assert obj_num not in found_objs
    found_objs.add(obj_num)

    # Go forward, till we find the 'EI'
    data = lines[i][3:]
    j = i + 1
    while not lines[j].startswith('EI'): 
      data += lines[j]
      j += 1
    i = j
    print('Decoding')
    filename = 'extr-%s.tiff' % obj_num
    decode_cccitt_data_to_file(data, width, height, filename, blackIsZero=

    decode(data, width, height, filename)
    num += 1

    from PIL import Image
    image_obj = Image.open(filename)
    rotated_image = image_obj.transpose(Image.FLIP_TOP_BOTTOM)
    rotated_image.save('flipped-' + filename)
    rotated_image.show()


    




extract_imagedata_from_pdf('P29-qpdf.pdf')

