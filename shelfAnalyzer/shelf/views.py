from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ShelfAnalysisView(APIView):

    def post(self,request):

        shelf_layout = request.data.get("layout")

        if not shelf_layout:
            return Response({"error:layout is required"},status=400)
        
        brand_cells_map = self.group_cells_by_brand(shelf_layout)

        final_result = {}

        for brand,cell_positions  in brand_cells_map.items():

            shape_type = self.identify_shape(cell_positions)
            location = self.indetify_location(cell_positions,shelf_layout)

            final_result[brand] = {
                "shape":shape_type,
                "location":location
            }

            return Response(final_result,status=status.HTTP_200_OK)
        
    # GROUP CELLS BY BRAND

    def group_cells_by_brand(self,shelf_layout):

        brand_cells = {}

        total_rows = len(shelf_layout)

        total_coolums = len(shelf_layout[0])





