from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ShelfAnalysisView(APIView):

    def post(self, request):

        shelf_layout = request.data.get("layout")

        if not shelf_layout:
            return Response({"error": "layout is required"}, status=400)

        brand_cells_map = self.group_cells_by_brand(shelf_layout)

        final_result = {}

        for brand, cell_positions in brand_cells_map.items():

            shape_type = self.identify_shape(cell_positions)
            location = self.identify_location(cell_positions, shelf_layout)

            final_result[brand] = {
                "shape": shape_type,
                "location": location
            }

        return Response(final_result, status=status.HTTP_200_OK)

    # GROUP CELLS BY BRAND

    def group_cells_by_brand(self, shelf_layout):

        brand_cells = {}

        total_rows = len(shelf_layout)

        total_colums = len(shelf_layout[0])

        for row_index in range(total_rows):

            for column_index in range(total_colums):

                brand = shelf_layout[row_index][column_index]

                if brand not in brand_cells:
                    brand_cells[brand] = []

                brand_cells[brand].append((row_index, column_index))

        return brand_cells

    # GET BOUNDING BOX

    def get_bounding_box(self, cell_positions):

        min_row = min(position[0] for position in cell_positions)
        max_row = max(position[0] for position in cell_positions)
        min_column = min(position[1] for position in cell_positions)
        max_column = max(position[1] for position in cell_positions)

        return min_row, max_row, min_column, max_column

    # SHAPE DETECTION

    def identify_shape(self, cell_positions):

        min_row, max_row, min_column, max_column = self.get_bounding_box(
            cell_positions)

        height = max_row - min_row + 1

        width = max_column - min_column + 1

        excepted_total_cells = height * width
        actual_total_cells = len(cell_positions)

        if actual_total_cells == excepted_total_cells:

            if height == width:
                return "square"

            elif height > width:
                return "vertical rectangle"

            else:
                return "horizontal rectangle"

        return "polygon"

    # LOCATION DETECTION

    def identify_location(self, cell_positions, shelf_layout):
        total_rows = len(shelf_layout)
        total_columns = len(shelf_layout[0])

        min_row, max_row, min_column, max_column = self.get_bounding_box(
            cell_positions)

        # Vertical position
        if max_row < total_rows // 2:
            vertical_position = "top"
        elif min_row >= total_rows // 2:
            vertical_position = "bottom"
        else:
            vertical_position = "middle"

        # Horizontal position
        if max_column < total_columns // 2:
            horizontal_position = "left"
        elif min_column >= total_columns // 2:
            horizontal_position = "right"
        else:
            horizontal_position = "middle"

        if vertical_position == "middle" and horizontal_position == "middle":
            return ["middle"]

        return [f"{vertical_position} {horizontal_position}".strip()]
