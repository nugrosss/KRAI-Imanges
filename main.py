import cv2
from ultralytics import YOLO
from grib import draw_grid_3x3,get_grid_cell,count_objects_in_grid
import time


model = YOLO(r"rak-v2\weights\best_int8_openvino_model", task="detect")


cap = cv2.VideoCapture(r"D:\kuliah JTD\belajar aroc\KRAI\frame_2.mp4")
# cap = cv2.VideoCapture(1)
 
prev_time = 0
tinggi_box = 35
focal_length = 800



if not cap.isOpened():
    print("Video tidak bisa dibuka")
    exit()

while True:

    # Ambil frame
    ret, frame = cap.read()

    # Jika video selesai
    if not ret:
        break

    frame = cv2.resize(frame, (640, 360))

    bounding_box = None
    kotak_list = []
    occupied_cells = []

    # Deteksi objek
    results = model(frame, imgsz=640, conf=0.25)
    frame = results[0].plot()

    

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cls = int(box.cls[0])

            conf = box.conf[0]
            class_name = model.names[cls]

            if class_name == "Bounding":
                bounding_box = (x1, y1, x2, y2)

            elif class_name == "Kotak":

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                distance = (focal_length * tinggi_box) / (y2 - y1)
                print(f"Jarak: {distance:.2f} cm")

                kotak_list.append((cx, cy))
    
    current_time = time.time()
    fps = 1 / max(current_time - prev_time, 0.0001)
    prev_time = current_time
    cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if bounding_box is not None:
        bx1, by1, bx2, by2 = bounding_box
        
        
        for cx, cy in kotak_list:
            cell = get_grid_cell(cx, cy, bx1, by1, bx2, by2)
            if cell is not None: # Pastikan cell valid
                occupied_cells.append(cell)

        grid_data = count_objects_in_grid(bounding_box,kotak_list)
        print(grid_data)
        
        draw_grid_3x3(frame, bx1, by1, bx2, by2, occupied_cells)

            
   
    cv2.imshow("YOLO Detection", frame)

    # Tombol q untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()