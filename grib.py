import cv2

def draw_grid_3x3(frame, x1, y1, x2, y2,occupied_cells=[]):

   
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Hitung ukuran
    w = x2 - x1
    h = y2 - y1

    cell_w = w // 3
    cell_h = h // 3

    # =========================
    # GARIS VERTIKAL
    # =========================
    for i in range(1, 3):

        x = x1 + i * cell_w

        cv2.line(
            frame,
            (x, y1),
            (x, y2),
            (0, 255, 0),
            2
        )

    # =========================
    # GARIS HORIZONTAL
    # =========================
    for j in range(1, 3):

        y = y1 + j * cell_h

        cv2.line(
            frame,
            (x1, y),
            (x2, y),
            (0, 255, 0),
            2
        )

   
    number = 1
    
    for row in range(3):
        for col in range(3):

            # Posisi text
            tx = x1 + col * cell_w + 20
            ty = y1 + row * cell_h + 40
            
            text = str(number)
            if number in occupied_cells:
                text += " [X]"

            cv2.putText(
                frame,
                text,
                (tx, ty),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            number += 1


def get_grid_cell(obj_x, obj_y, x1, y1, x2, y2):

    w = x2 - x1
    h = y2 - y1

    cell_w = w / 3
    cell_h = h / 3

    col = int((obj_x - x1) / cell_w)
    row = int((obj_y - y1) / cell_h)

    col = min(max(col, 0), 2)
    row = min(max(row, 0), 2)

    return row * 3 + col + 1

def count_objects_in_grid(bounding_box, kotak_list):

    bx1, by1, bx2, by2 = bounding_box

    
    grid_count = {i: 0 for i in range(1, 10)}

    w = bx2 - bx1
    h = by2 - by1

    cell_w = w / 3
    cell_h = h / 3

    for cx, cy in kotak_list:

        col = int((cx - bx1) / cell_w)
        row = int((cy - by1) / cell_h)

        col = min(max(col, 0), 2)
        row = min(max(row, 0), 2)

        cell = row * 3 + col + 1

        grid_count[cell] += 1

    return grid_count