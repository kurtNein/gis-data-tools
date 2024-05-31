import arcpy
from arcpy import da

arcpy.env.workspace = r'C:\Users\kcneinstedt\Downloads\NJ_NG911_2023_12_26.gdb\NJ_NG911_2023_12_26.gdb'
print(arcpy.ListFeatureClasses())
class RetrieveExternalKeyFromMatchingAttributes:
    def __init__(self,
                 target_fc: str,
                 reference_fc: str,
                 match_fields_target: list,
                 match_fields_reference: list,
                 key_field_target: str,
                 key_field_reference: str
                 ):
        # This will be the feature class you intend to retrieve an external key for.
        self.target_fc = target_fc
        # This will be the feature class whose matched feature you will take the external key from.
        self.reference_fc = reference_fc
        # This will be the list of fields from the target_fc that will be used as match criteria to the reference_fc.
        self.match_fields_target = match_fields_target
        # This will be the list of fields it will look to match with the match_fields_target.
        self.match_fields_reference = match_fields_reference
        self.key_field_target = key_field_target
        self.key_field_reference = key_field_reference
        # Do the below so that you have an index to reference the key field by in the SearchCursor later on.
        self.match_fields_reference.insert(0, self.key_field_reference)
        # Instead of iterating through every record in target_fc, turn it into a dict.
        # Average time complexity of dict access by key is O(1), iterating through n records is O(n).
        # Iterating through n records in the reference_fc for x records in target_fc is O(n*x).
        self.reference_dictionary = {}
        print('Variables initialized')

        with da.SearchCursor(self.reference_fc, match_fields_reference) as cursor:
            for row in cursor:
                # Slice the match_fields_reference because the key field was inserted at index 0, so get 1 to the end.
                self.reference_dictionary[match_fields_reference[1:]] = row[0] # row[0] is the key field we inserted.
            print(self.reference_dictionary)


    def get_reference_point(self):
        clause = "SignPostID = '{}'".format(self.attribute)
        clause = []
        print(clause)
        with da.SearchCursor(self.reference_fc, ["OID@", "SHAPE@", "SignPostID"], where_clause=str(clause)) as cursor:
            for row in cursor:
                print(row[0])
                coord = row[1]
            return coord

if __name__ == '__main__':
    key_finder = RetrieveExternalKeyFromMatchingAttributes(
        r'C:\Users\kcneinstedt\Downloads\NJ_NG911_2023_12_26.gdb\NJ_NG911_2023_12_26.gdb\AddressPoints',
        r'C:\Users\kcneinstedt\Downloads\NJ_NG911_2023_12_26.gdb\NJ_NG911_2023_12_26.gdb\DATA\RoadCenterlines',
        ['INC_MUNI'],
        ['INCMUNI_L'],
        'RCL_NGUID',
        'RCL_NGUID')
