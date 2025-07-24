import pickle
import threading
import time
import tkinter as tk
from collections import deque
from tkinter import messagebox, ttk

import cv2
import googletrans
import mediapipe as mp
import numpy as np
from googletrans import Translator


class SignLanguageTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Translator")
        self.root.geometry("1280x720")

        # Load model and necessary tools
        try:
            # MediaPipe hands
            self.mp_hands = mp.solutions.hands
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_drawing_styles = mp.solutions.drawing_styles
            self.hands = self.mp_hands.Hands(
                static_image_mode=True, min_detection_confidence=0.3
            )

            # Load trained model
            model_dict = pickle.load(open("./model.p", "rb"))
            self.model = model_dict["model"]

            # Labels for ASL letters
            self.labels_dict = {
                0: "A",
                1: "B",
                2: "C",
                3: "D",
                4: "E",
                5: "F",
                6: "G",
                7: "H",
                8: "I",
                9: "J",
                10: "K",
                11: "L",
                12: "M",
                13: "N",
                14: "O",
                15: "P",
                16: "Q",
                17: "R",
                18: "S",
                19: "T",
                20: "U",
                21: "V",
                22: "W",
                23: "X",
                24: "Y",
                25: "Z",
            }
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            messagebox.showerror("Error", f"Error loading model: {e}")
            self.root.destroy()
            return

        # Translator for translation
        self.translator = Translator()

        # Application variables
        self.is_running = False
        self.cap = None
        self.detected_letter = ""
        self.current_word = ""
        self.current_text = ""
        self.translated_text = ""
        self.selected_language = tk.StringVar(
            value="en-tr"
        )  # Default: English -> Turkish
        self.last_detection_time = time.time()
        self.word_timeout = 1.0  # 1 second gap = new word

        # Variables for stability
        self.last_predictions = deque(maxlen=30)  # Store last 30 predictions
        self.required_stable_frames = 20  # Same letter must be detected for 20 frames
        self.stable_threshold = 0.8  # 80% of frames must detect the same letter
        self.last_added_letter = None  # Last added letter

        # Create UI
        self.create_ui()

        # Key controls
        self.root.bind("<space>", self.add_space)
        self.root.bind("<BackSpace>", self.delete_last_letter)
        self.root.bind("<Return>", self.translate_text)
        self.root.bind("q", self.quit_app)

    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Camera and controls
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side="left", fill="both", expand=True)

        # Camera display
        self.camera_label = ttk.Label(left_panel, borderwidth=2, relief="solid")
        self.camera_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Camera controls
        camera_control_frame = ttk.Frame(left_panel)
        camera_control_frame.pack(fill="x", padx=10, pady=10)

        self.start_button = ttk.Button(
            camera_control_frame, text="Start Camera", command=self.toggle_camera
        )
        self.start_button.pack(side="left", padx=5, pady=5)

        # Status text
        self.status_label = ttk.Label(camera_control_frame, text="Ready")
        self.status_label.pack(side="left", padx=20, pady=5)

        # Right panel - Detected letters, text and translation
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Language selection
        language_frame = ttk.LabelFrame(right_panel, text="Language Selection")
        language_frame.pack(fill="x", padx=5, pady=5)

        ttk.Radiobutton(
            language_frame,
            text="English to Turkish",
            value="en-tr",
            variable=self.selected_language,
        ).pack(side="left", padx=10, pady=5)
        ttk.Radiobutton(
            language_frame,
            text="Turkish to English (Not Active Yet)",
            value="tr-en",
            variable=self.selected_language,
            state="disabled",
        ).pack(side="left", padx=10, pady=5)

        # Detected letter
        ttk.Label(right_panel, text="Detected Letter:").pack(anchor="w", padx=5, pady=5)
        self.letter_label = ttk.Label(right_panel, text="", font=("Arial", 48, "bold"))
        self.letter_label.pack(anchor="w", padx=5, pady=5)

        # Stability indicator
        self.stability_frame = ttk.Frame(right_panel)
        self.stability_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.stability_frame, text="Stability:").pack(
            side="left", padx=5, pady=5
        )
        self.stability_label = ttk.Label(self.stability_frame, text="0%", width=10)
        self.stability_label.pack(side="left", padx=5, pady=5)

        self.progress_var = tk.DoubleVar()
        self.stability_progress = ttk.Progressbar(
            self.stability_frame,
            variable=self.progress_var,
            length=200,
            mode="determinate",
        )
        self.stability_progress.pack(side="left", padx=5, pady=5)

        # Generated text
        ttk.Label(right_panel, text="Generated Text:").pack(anchor="w", padx=5, pady=5)
        self.text_frame = ttk.Frame(right_panel, borderwidth=1, relief="solid")
        self.text_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.text_label = ttk.Label(
            self.text_frame, text="", font=("Arial", 14), wraplength=500, justify="left"
        )
        self.text_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Translation
        ttk.Label(right_panel, text="Translation:").pack(anchor="w", padx=5, pady=5)
        self.translation_frame = ttk.Frame(right_panel, borderwidth=1, relief="solid")
        self.translation_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.translation_label = ttk.Label(
            self.translation_frame,
            text="",
            font=("Arial", 14),
            wraplength=500,
            justify="left",
        )
        self.translation_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="Translate", command=self.translate_text).pack(
            side="left", padx=5, pady=5
        )
        ttk.Button(button_frame, text="Clear", command=self.clear_text).pack(
            side="left", padx=5, pady=5
        )

        # Control information
        controls_text = """Controls:
        - Space: Add space
        - Backspace: Delete last letter
        - Enter: Translate
        - Q: Quit
        
        Note: A letter must be detected for {} frames to be written.""".format(
            self.required_stable_frames
        )
        ttk.Label(right_panel, text=controls_text, justify="left").pack(
            anchor="w", padx=5, pady=10
        )

    def toggle_camera(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="Start Camera")
            self.status_label.config(text="Stopped")
            if self.cap is not None:
                self.cap.release()
        else:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera!")
                return

            self.is_running = True
            self.start_button.config(text="Stop Camera")
            self.status_label.config(text="Running...")

            # Start camera stream in a separate thread
            threading.Thread(target=self.process_camera, daemon=True).start()

    def process_camera(self):
        while self.is_running and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret:
                print("Could not get camera feed!")
                break

            try:
                # Frame'i işle
                processed_frame, letter = self.process_frame(frame)

                # Algılanan harfi stabilizasyon listesine ekle
                if letter:
                    self.last_predictions.append(letter)

                    # Stabilizasyon oranını hesapla
                    if self.last_predictions:
                        # Hangi harf en çok algılandı
                        from collections import Counter

                        letter_counts = Counter(self.last_predictions)
                        most_common_letter, count = letter_counts.most_common(1)[0]

                        # Stabilite oranı
                        stability = count / len(self.last_predictions)
                        stability_percent = int(stability * 100)

                        # UI'ı güncelle
                        self.stability_label.config(text=f"{stability_percent}%")
                        self.progress_var.set(stability * 100)

                        # Kararlı bir tahmin mi?
                        if (
                            stability >= self.stable_threshold
                            and count >= self.required_stable_frames
                            and most_common_letter != self.last_added_letter
                        ):

                            # Tahmin edilen harfi ekle
                            self.detected_letter = most_common_letter
                            self.letter_label.config(text=most_common_letter)

                            # Yeni kelime kontrolü
                            current_time = time.time()
                            if (
                                current_time - self.last_detection_time
                                > self.word_timeout
                                and self.current_word
                            ):
                                self.current_text += self.current_word + " "
                                self.current_word = ""

                            self.current_word += most_common_letter
                            self.last_detection_time = current_time
                            self.last_added_letter = most_common_letter

                            # Metni güncelle
                            self.update_text()

                            # Tahmin listesini temizle
                            self.last_predictions.clear()

                # Frame'i görüntüle
                cv2_img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                img = self.convert_to_tk_image(cv2_img)

                if self.is_running:  # Eğer hala çalışıyorsa güncelle
                    self.camera_label.config(image=img)
                    self.camera_label.image = (
                        img  # Referansı tut (garbage collection engellemek için)
                    )

            except Exception as e:
                print(f"Hata: {e}")

            # UI'ı güncel tut
            self.root.update_idletasks()
            self.root.update()

            # Performans için kısa bekleme
            time.sleep(0.01)

        # Döngü bitince kamerayı serbest bırak
        if self.cap is not None:
            self.cap.release()

    def process_frame(self, frame):
        try:
            H, W, _ = frame.shape

            # BGR -> RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # MediaPipe Hands ile elleri algıla
            results = self.hands.process(frame_rgb)
            letter = ""

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Eli görselleştir
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style(),
                    )

                    # Landmark koordinatlarını topla
                    data_aux = []
                    x_ = []
                    y_ = []

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        x_.append(x)
                        y_.append(y)

                    # Normalize edilmiş koordinatlar hesapla
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                    # El etrafına dikdörtgen çiz
                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10
                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10

                    # Koordinatlar ekran dışında kalmasın
                    x1 = max(0, x1)
                    y1 = max(0, y1)
                    x2 = min(W, x2)
                    y2 = min(H, y2)

                    # Stabilite durumuna göre renk belirle
                    if len(self.last_predictions) > 0:
                        from collections import Counter

                        letter_counts = Counter(self.last_predictions)
                        most_common_letter, count = letter_counts.most_common(1)[0]
                        stability = count / len(self.last_predictions)

                        # Stabilite değerine göre renk değişimi (kırmızıdan yeşile)
                        # 0.0-0.3: Kırmızı, 0.3-0.6: Sarı, 0.6-1.0: Yeşil
                        if stability < 0.3:
                            color = (0, 0, 255)  # Kırmızı
                        elif stability < 0.6:
                            color = (0, 255, 255)  # Sarı
                        else:
                            color = (0, 255, 0)  # Yeşil
                    else:
                        color = (0, 0, 255)  # Başlangıçta kırmızı

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                    # Harf tahmini yap (doğru sayıda özellik varsa)
                    if len(data_aux) == 42:
                        prediction = self.model.predict([np.asarray(data_aux)])
                        letter = self.labels_dict[int(prediction[0])]

                        # Harfi ekrana yaz
                        cv2.putText(
                            frame,
                            letter,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.3,
                            color,
                            2,
                            cv2.LINE_AA,
                        )

                        # Stabilite bilgisini de ekle
                        if len(self.last_predictions) > 0:
                            stability_info = f"Stability: {int(stability * 100)}%"
                            cv2.putText(
                                frame,
                                stability_info,
                                (x1, y2 + 30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                color,
                                2,
                                cv2.LINE_AA,
                            )

            return frame, letter

        except Exception as e:
            print(f"Frame işleme hatası: {e}")
            return frame, ""

    def convert_to_tk_image(self, img):
        # OpenCV görüntüsünü tkinter için hazırla
        img = cv2.resize(img, (640, 480))
        _, img_encoded = cv2.imencode(".png", img)
        return tk.PhotoImage(data=img_encoded.tobytes())

    def update_text(self):
        display_text = self.current_text + self.current_word
        self.text_label.config(text=display_text)

    def add_space(self, event=None):
        if self.current_word:
            self.current_text += self.current_word + " "
            self.current_word = ""
            self.update_text()

    def delete_last_letter(self, event=None):
        if self.current_word:
            self.current_word = self.current_word[:-1]
        elif self.current_text:
            # Boş olmayan son kelimeyi bul
            self.current_text = self.current_text.rstrip()
            if self.current_text:
                parts = self.current_text.rsplit(" ", 1)
                if len(parts) > 1:
                    self.current_text = parts[0] + " "
                    self.current_word = parts[1]
                else:
                    self.current_word = parts[0]
                    self.current_text = ""

        # Son eklenen harfi güncelle
        self.last_added_letter = (
            None if not self.current_word else self.current_word[-1]
        )

        self.update_text()

    def translate_text(self, event=None):
        # Önce mevcut kelimeyi ekle
        if self.current_word:
            self.current_text += self.current_word + " "
            self.current_word = ""
            self.update_text()

        # Çeviri için metin boş değilse
        text_to_translate = self.current_text.strip()
        if text_to_translate:
            try:
                lang_pair = self.selected_language.get().split("-")
                src_lang = lang_pair[0]
                dest_lang = lang_pair[1]

                translated = self.translator.translate(
                    text_to_translate, src=src_lang, dest=dest_lang
                )

                self.translated_text = translated.text
                self.translation_label.config(text=self.translated_text)

            except Exception as e:
                print(f"Çeviri hatası: {e}")
                self.translation_label.config(text=f"Çeviri hatası: {e}")

    def clear_text(self):
        self.last_predictions.clear()
        self.detected_letter = ""
        self.current_word = ""
        self.current_text = ""
        self.translated_text = ""
        self.last_added_letter = None

        self.letter_label.config(text="")
        self.text_label.config(text="")
        self.translation_label.config(text="")
        self.stability_label.config(text="0%")
        self.progress_var.set(0)

    def quit_app(self, event=None):
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageTranslatorApp(root)
    root.mainloop()
