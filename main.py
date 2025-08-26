from boundaries_capturer import BoundariesCapturer as BC
from tiles_creator import TilesCreator as TC
from screenshot_maker import ScreenshotMaker as SM
from settings import Settings as S
from screenshot_stitcher import ScreenshotStitcher as SS

import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="MapExtractorTool",
        description="Run tool in different modes."
    )

    subparsers = parser.add_subparsers(dest='mode', required=True)

    get_coords = subparsers.add_parser("saveCoordinates", help="Collect and save map coordinates")
    get_coords.add_argument("--name", type=str, help="Map title")
    get_coords.add_argument("--w", type=int, required=True, help="Width of viewport")
    get_coords.add_argument("--h", type=int, required=True, help="Height of viewport")
    get_coords.add_argument("--z", type=int, required=True, help="Zoom of the map view")

    make_screenshots = subparsers.add_parser("takeScreenshots", help="Make screenshots from a given .json file with coordinates")
    make_screenshots.add_argument("--name", type=str, required=True, help=".json file where coordinates are stored")

    stitch_map = subparsers.add_parser("stitchMap", help="Combine screenshots into one map")
    stitch_map.add_argument("--name", type=str, required=True, help="subfolder under /tiles folder where screenshots are stored")

    run_all = subparsers.add_parser("runAll", help="Full process: collect map coordinates, take screenshots and combine them into a single map")
    run_all.add_argument("--name", type=str, help="Map title")
    run_all.add_argument("--w", type=int, required=True, help="Width of viewport")
    run_all.add_argument("--h", type=int, required=True, help="Height of viewport")
    run_all.add_argument("--z", type=int, required=True, help="Zoom of the map view")

    args = parser.parse_args()

    if args.mode == "saveCoordinates":
        # >>>>>>>>> creates folders for outputs and sets global variables <<<<<<<<<
        settings = S(args.name if args.name else '', args.w, args.h, args.z)
        settings.set_window_size_zoom()
        settings.set_map_size()
        settings.set_map_title()
        settings.set_boundaries_output_folder()

        # >>>>>>>>> collects and stores coordinates to be included in the map <<<<<<<<<
        new_boundaries = BC()
        new_boundaries.get_points()
        new_boundaries.store_points()


    elif args.mode == "takeScreenshots":
        # >>>>>>>>> creates folders for outputs and sets global variables <<<<<<<<<
        settings = S(args.name)
        settings.get_params_from_json()
        settings.set_window_size_zoom()
        settings.set_map_size()
        settings.set_map_title()
        settings.set_tiles_output_folder()

        # >>>>>>>>> computes boundaries of the map and divides it into tiles <<<<<<<<<
        # sonarignore: python:S125
        tiles_creator = TC()
        tiles_creator.read_map_coords()
        tiles_creator.convert_to_decimal()
        tiles_creator.get_container_rectangle()
        tiles_creator.compute_bands_shifts_number()

        # >>>>>>>>> makes screenshots according to computed tiles <<<<<<<<<
        screenshot_maker = SM(tiles_creator.area)
        screenshot_maker.move_across_bands()


    elif args.mode == "stitchMap":
        # >>>>>>>>> creates folders for outputs and sets global variables <<<<<<<<<
        settings = S(args.name)
        settings.check_tiles_exist()
        settings.set_map_title()
        settings.set_maps_output_folder()

        # >>>>>>>>> stitches individual screenshots into a full map <<<<<<<<<
        stitcher = SS()
        stitcher.stitch_screenshots()


    elif args.mode == "runAll":
        # >>>>>>>>> creates folders for outputs and sets global variables <<<<<<<<<
        settings = S(args.name if args.name else '', args.w, args.h, args.z)
        settings.set_window_size_zoom()
        settings.set_map_size()
        settings.set_map_title()
        settings.set_boundaries_output_folder()
        settings.set_tiles_output_folder()
        settings.set_maps_output_folder()

        # >>>>>>>>> collects and stores coordinates to be included in the map <<<<<<<<<
        new_boundaries = BC()
        new_boundaries.get_points()
        new_boundaries.store_points()

        # >>>>>>>>> computes boundaries of the map and divides it into tiles <<<<<<<<<
        # sonarignore: python:S125
        tiles_creator = TC()
        tiles_creator.read_map_coords()
        tiles_creator.convert_to_decimal()
        tiles_creator.get_container_rectangle()
        tiles_creator.compute_bands_shifts_number()

        # >>>>>>>>> makes screenshots according to computed tiles <<<<<<<<<
        screenshot_maker = SM(tiles_creator.area)
        screenshot_maker.move_across_bands()

        # >>>>>>>>> stitches individual screenshots into a full map <<<<<<<<<
        stitcher = SS()
        stitcher.stitch_screenshots()


if __name__ == "__main__":
    main()
