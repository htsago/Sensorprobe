import csv

def swap_columns(input_file, output_file, column_order, columns_to_delete):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        header_indices = {column: index for index, column in enumerate(header) if column not in columns_to_delete}
        output_header = [column for column in column_order if column in header_indices]

        with open(output_file, 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(output_header)

            for row in reader:
                output_row = [row[header_indices[column]] for column in output_header]
                writer.writerow(output_row)

    print("Done!")


# Aufruf der Funktion
input_file ="D:/Sensorprobe/new_data/screw_01.csv"

output_file = 'screw_new.csv'

column_order = ['timestamp','R1_1','R1_2','R1_3','R1_4','R1_5','R1_6','R2_1','R2_2','R2_3','R2_4','R2_5','R2_6','R3_1','R3_2','R3_3','R3_4','R3_5','R3_6','R4_1','R4_2','R4_3','R4_4','R4_5','R4_6','Label','Class']

columns_to_delete = ["timestamp","Port1","Port2","Port3","Port4","R2_1","R2_2","R2_3","R2_4","R2_5","R2_6"]

swap_columns(input_file, output_file, column_order, columns_to_delete)


