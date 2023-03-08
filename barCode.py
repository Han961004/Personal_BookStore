import cv2
import pyzbar.pyzbar as pyzbar



def barcode():
    
    cap = cv2.VideoCapture(0)

    turn = True
    while True:
        
        success, frame = cap.read()
        
        if success:
            for code in pyzbar.decode(frame):
                my_code = code.data.decode('utf-8')
                
                # print("인식 성공 : ", my_code)
                
                # 인식했을 때 카메라 끄기
                turn = False
                
            cv2.imshow('cam', frame)

            key = cv2.waitKey(1)
            
            # 카메라 끄기 
            if turn == False:
                break



    cap.release()
    cv2.destroyAllWindows()

    return my_code