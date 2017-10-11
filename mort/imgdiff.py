import cv2
import numpy
from skimage.measure import compare_ssim
from skimage.measure import structural_similarity as ssim

from .local_conf import IMAGE_DIFF_BOX_COLOR, IMAGE_DIFF_BOX_STROKE_WIDTH


def load_image(img_file: str) -> numpy.ndarray:
    """
    Load the specified image file into a `numpy.ndarray` and convert
    the image into gray scale if it's specified.

    :param img_file: path to the image file to load
    :return: `ndarray` for us to do further operations on
    """
    img = cv2.imread(img_file, 0)  # Load in Gray Scale
    return img


def get_similarity_index(image_file: str, reference_file: str) -> float:
    """
    Return the Structural Similarity Index for the two images.

    :param reference_file: the baseline image that acts as the reference image.
    :param image_file: the image we are comparing to the baseline.

    :return: a float value between `[1, -1]` where 1 means perfect match.
    """
    reference = load_image(reference_file)
    image = load_image(image_file)
    return ssim(image, reference)


def generate_annotated_diff_image(image_file: str, reference_file: str, as_file: str) -> int:
    """
    Compare the two image files and generate a new image with the differences highlighted on the `image_file`.

    :param reference_file: the baseline image that acts as the reference image.
    :param image_file: the image we are comparing to the baseline.
    :param as_file: the full path where the diff image will be saved.
    :return: the number of differences found
    """
    reference = load_image(reference_file)
    image = load_image(image_file)
    (_, diff_image) = compare_ssim(image, reference, full=True)  # full will return the `diff_image`

    # First, let's convert the `diff_image` from float data between [0, 1] into unsigned int 8
    diff_image = (diff_image * 255).astype('uint8')

    # Threshold the difference using and find the regions where the two images differ.
    threshold_image = cv2.threshold(diff_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    region_contours = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    # Now that we have the contour of each shape. Find out the bounding box for each region.
    region_boxes = [cv2.boundingRect(contour) for contour in region_contours]

    # Annotate each regions by drawing a rectangle on the image
    color_image = cv2.imread(image_file)
    for (x, y, w, h) in region_boxes:
        cv2.rectangle(color_image, (x, y), (x + w, y + h), IMAGE_DIFF_BOX_COLOR, IMAGE_DIFF_BOX_STROKE_WIDTH)
    cv2.imwrite(as_file, color_image)
    return len(region_boxes)

# if __name__ == "__main__":
# print(get_similarity_index('/tmp/edited.jpg', '/tmp/origin.jpg'))
# print(generate_annotated_diff_image('/tmp/edited.jpg', '/tmp/origin.jpg', '/tmp/output.jpg'))
