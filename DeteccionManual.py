#Deteccion de manos Codigo por mejorar a futuro 
#@author Salvador Sanchez Luengas
import cv2
import mediapipe as mp

# Inicializar Mediapipe Hands pra una sola mano
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)
#vector definido para la utilizacion de deteccion de dedos 
def count_fingers(landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Incluyendo pulgar detectado por enfrente  
    finger_count = 0

    # Comprobar el pulgar en posicion diagonal
    if landmarks[4].x < landmarks[3].x and landmarks[4].y < landmarks[3].y:  # Pulgar extendido
        finger_count += 1
    
    # Comprobar los otros dedos
    for tip in finger_tips[1:]:  # Excluye el pulgar
        if landmarks[tip].y < landmarks[tip - 2].y:
            finger_count += 1

    return finger_count

while True:
    ret, frame = cap.read()
    if not ret:
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(hand_landmarks.landmark)
            cv2.putText(frame, f'Dedos : {finger_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Hand Detection', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Salir al presionar Esc
        break

cap.release()
cv2.destroyAllWindows()