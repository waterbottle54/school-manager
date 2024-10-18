import os

from data.ProblemHeader import *


class ImageRepository:

    _instance: "ImageRepository | None" = None

    @staticmethod
    def get_instance() -> "ImageRepository":
        if ImageRepository._instance is None:
            ImageRepository._instance = ImageRepository()
        return ImageRepository._instance

    def get_problem_image_path(self, header: ProblemHeader, is_main: bool) -> str:
        return f"images_problem/grade{header.grade}/{header.chapter}/{header.book}-{header.title}({'main' if is_main else 'sub'}).png"

    def save_problem_image(self, header: ProblemHeader, data: bytes, is_main: bool):
        path = self.get_problem_image_path(header, is_main)
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, "wb") as file:
            file.write(data)

    def load_problem_image(self, header: ProblemHeader, is_main: bool) -> bytes | None:
        path = self.get_problem_image_path(header, is_main)
        try:
            with open(path, "rb") as file:
                return file.read()
        except FileNotFoundError:
            return None

    def delete_problem_image(self, header: ProblemHeader, is_main: bool) -> bool:
        path = self.get_problem_image_path(header, is_main)
        try:
            if os.path.isfile(path):
                os.remove(path)
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
