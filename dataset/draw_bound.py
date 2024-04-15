import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont


def draw_bounds_on_image(image_path, json_data_path, output_image_path):
    if not os.path.exists(json_data_path):
        raise FileNotFoundError(f"{json_data_path} not found")

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    json_data = json.load(open(json_data_path))

    for i, item in enumerate(json_data):
        bounds = item["bounds"]
        bounds = bounds.strip("[]").split("][")
        x1, y1 = map(int, bounds[0].split(","))
        x2, y2 = map(int, bounds[1].split(","))

        draw.rectangle([x1, y1, x2, y2], outline="red", width=5)

        font_size = max(1, min(int(min(x2 - x1, y2 - y1) * 0.8), 150))
        font = ImageFont.truetype(font="arial.ttf", size=font_size)

        text = str(i)
        text_width, text_height = draw.textsize(text, font=font)

        text_x = x1 + (x2 - x1) / 2 - text_width / 2
        text_y = y1 + (y2 - y1) / 2 - text_height / 2

        draw.text((text_x, text_y), text, fill="red", font=font)

    image.save(output_image_path)


if __name__ == "__main__":

    if len(sys.argv) == 1:

        ALLOWED_EXTENSIONS = {"png"}
        cats = ["general", "generated", "googleapps", "install", "webshopping"]

        # False: if figure exists, skip it
        # True: regenerate all figures
        force_draw = False

        for sub_categories in cats:
            folder_path = sub_categories
            traces_path = os.listdir(folder_path)
            traces_path = [os.path.join(folder_path, trace) for trace in traces_path]
            traces_path = [trace for trace in traces_path if "trace" in trace]
            traces_path = [trace for trace in traces_path if os.path.isdir(trace)]

            image_files_path = []
            for trace_path in traces_path:
                image_files = [
                    file
                    for file in os.listdir(trace_path)
                    if file.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS
                    and "drawed" not in file
                    and "agg_plot" not in file
                ]
                for image_file in image_files:
                    image_files_path.append(os.path.join(trace_path, image_file))

            for image_file_path in image_files_path:
                if not force_draw and os.path.exists(
                    image_file_path[:-4] + "_drawed.png"
                ):
                    continue

                print(image_file_path)
                draw_bounds_on_image(
                    image_file_path,
                    image_file_path[:-3] + "json",
                    image_file_path[:-4] + "_drawed.png",
                )
    else:
        # plot for single image
        for image_path in sys.argv[1:]:
            draw_bounds_on_image(
                image_path, image_path[:-3] + "json", image_path[:-4] + "_drawed.png"
            )
