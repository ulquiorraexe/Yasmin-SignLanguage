import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
import cv2
from PIL import Image

# Modern görünüm için customtkinter ayarları
ctk.set_appearance_mode("dark")  # "dark" veya "light"
ctk.set_default_color_theme(
    "blue"
)  # "blue" (mavi), "green" (yeşil), "dark-blue" (koyu mavi)


class AppUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance  # Ana uygulama referansı

        # UI temasını ayarla
        self.configure_theme()

        # UI bileşenlerini oluştur
        self.create_ui()

        # Tuş kontrolleri
        self.setup_key_bindings()

        # Pencere yeniden boyutlandırma olayını yakala
        self.root.bind("<Configure>", self.on_window_resize)

    def configure_theme(self):
        # Ana pencere ayarları
        self.root.configure(bg="#1A1A1A")
        # Renk paleti
        self.bg_color = "#1A1A1A"  # Arkaplan rengi (koyu gri)
        self.card_color = "#2D2D2D"  # Panel rengi (orta gri)
        self.accent_color = "#3498db"  # Vurgu rengi (mavi)
        self.text_color = "#FFFFFF"  # Metin rengi (beyaz)
        self.secondary_text_color = "#AAAAAA"  # İkincil metin rengi (açık gri)

    def setup_key_bindings(self):
        # Tuş kontrolleri
        self.root.bind("<space>", self.app.add_space)  # Space tuşu
        self.root.bind(
            "<KeyPress-space>", self.app.add_space
        )  # Space tuşu için alternatif bağlama
        self.root.bind("<BackSpace>", self.app.delete_last_letter)
        self.root.bind("<Return>", self.app.translate_text)
        self.root.bind("q", self.app.quit_app)

    def on_window_resize(self, event):
        # Pencere boyutlandırıldığında responsive yeniden düzenlemeler
        if hasattr(self, "stability_progress") and event.widget == self.root:
            window_width = event.width
            # Stabilite çubuğu genişliğini pencere genişliğine göre ayarla
            if hasattr(self, "stability_progress"):
                self.stability_progress.configure(
                    width=max(100, int(window_width * 0.25))
                )
            # Harf işleme çubuğunu da aynı genişlikte ayarla
            if hasattr(self, "letter_progress"):
                self.letter_progress.configure(width=max(100, int(window_width * 0.25)))

    def create_ui(self):
        # Ana frame
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Sol panel - Kamera ve kontroller
        left_panel = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=5)

        # Kamera gösterimi için çerçeve (placeholder)
        camera_frame = ctk.CTkFrame(left_panel, corner_radius=10)
        camera_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Kamera gösterimi (placeholder label olarak kullanıyoruz, video frame için)
        self.camera_label = ctk.CTkLabel(
            camera_frame,
            text="Kamera Görüntüsü",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            fg_color=("#343434", "#343434"),
        )
        self.camera_label.pack(fill="both", expand=True, padx=5, pady=5)

        # Kamera kontrolleri
        camera_control_frame = ctk.CTkFrame(left_panel, corner_radius=10)
        camera_control_frame.pack(fill="x", padx=10, pady=5)

        self.start_button = ctk.CTkButton(
            camera_control_frame,
            text="Kamerayı Başlat",
            command=self.app.toggle_camera,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            fg_color=self.accent_color,
            height=35,
        )  # Daha küçük buton
        self.start_button.pack(side="left", padx=10, pady=5, fill="x", expand=True)

        # Durum metni
        self.status_label = ctk.CTkLabel(
            camera_control_frame,
            text="Hazır",
            font=ctk.CTkFont(size=14),
            corner_radius=8,
        )
        self.status_label.pack(side="left", padx=10, pady=5)

        # Sağ panel - Kontrol paneli (Scroll View ile sarmalanmış)
        right_outer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_outer_frame.pack(side="right", fill="both", expand=True, padx=5)

        # ScrollView oluştur
        right_scroll = ctk.CTkScrollableFrame(
            right_outer_frame, fg_color="transparent", corner_radius=10
        )
        right_scroll.pack(fill="both", expand=True)

        # A. Çeviri Yönü
        translation_direction_frame = ctk.CTkFrame(right_scroll, corner_radius=10)
        translation_direction_frame.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(
            translation_direction_frame,
            text="Çeviri Yönü",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w", padx=10, pady=(10, 5))

        radio_frame = ctk.CTkFrame(translation_direction_frame, fg_color="transparent")
        radio_frame.pack(fill="x", padx=10, pady=5)

        self.tr_en_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Türkçe -> İngilizce",
            variable=self.app.translation_direction,
            value="tr-en",
            font=ctk.CTkFont(size=14),
        )
        self.tr_en_radio.pack(side="left", padx=20, pady=5)

        self.en_tr_radio = ctk.CTkRadioButton(
            radio_frame,
            text="İngilizce -> Türkçe",
            variable=self.app.translation_direction,
            value="en-tr",
            font=ctk.CTkFont(size=14),
        )
        self.en_tr_radio.pack(side="left", padx=20, pady=5)

        # B. Algılanan Harf
        letter_frame = ctk.CTkFrame(right_scroll, corner_radius=10)
        letter_frame.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(
            letter_frame,
            text="Algılanan Harf",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.letter_label = ctk.CTkLabel(
            letter_frame,
            text="",
            font=ctk.CTkFont(size=72, weight="bold"),
            text_color=self.accent_color,
        )
        self.letter_label.pack(pady=10)

        # C. Stabilite Göstergesi
        stability_frame = ctk.CTkFrame(right_scroll, corner_radius=10)
        stability_frame.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(
            stability_frame, text="Stabilite", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        stability_control_frame = ctk.CTkFrame(stability_frame, fg_color="transparent")
        stability_control_frame.pack(fill="x", padx=10, pady=5)

        self.progress_var = tk.DoubleVar(value=0)  # Başlangıçta 0

        # Stabilite etiketini önce yerleştir (sağda)
        self.stability_label = ctk.CTkLabel(
            stability_control_frame,
            text="0%",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=50,
        )
        self.stability_label.pack(side="right", padx=5, pady=5)

        # Progress bar'ı genişleyecek şekilde yerleştir
        self.stability_progress = ctk.CTkProgressBar(
            stability_control_frame,
            variable=self.progress_var,
            height=15,
            corner_radius=5,
            progress_color=self.accent_color,
        )
        self.stability_progress.pack(
            side="left", padx=(5, 10), pady=5, fill="x", expand=True
        )

        # D. Harf İşleme Çubuğu
        letter_processing_frame = ctk.CTkFrame(stability_frame, fg_color="transparent")
        letter_processing_frame.pack(fill="x", padx=10, pady=5)

        # Yeni ilerleme çubuğu (stabilite altında)
        self.letter_progress_var = tk.DoubleVar(value=0)

        # İşlem etiketini sağa yerleştir
        self.letter_progress_label = ctk.CTkLabel(
            letter_processing_frame,
            text="0/" + str(self.app.required_stable_frames),
            font=ctk.CTkFont(size=14, weight="bold"),
            width=60,
        )
        self.letter_progress_label.pack(side="right", padx=5, pady=5)

        # Harf işleme ilerleme çubuğu
        self.letter_progress = ctk.CTkProgressBar(
            letter_processing_frame,
            variable=self.letter_progress_var,
            height=15,
            corner_radius=5,
            progress_color="#27ae60",
        )  # Yeşil renk (farklı olması için)
        self.letter_progress.pack(
            side="left", padx=(5, 10), pady=5, fill="x", expand=True
        )

        # Açıklama etiketi
        ctk.CTkLabel(
            stability_frame, text="Harf İşleme İlerlemesi", font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=10, pady=(0, 10))

        # E. Oluşan Metin
        text_frame = ctk.CTkFrame(right_scroll, corner_radius=10)
        text_frame.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(
            text_frame, text="Oluşan Metin", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.text_textbox = ctk.CTkTextbox(
            text_frame, height=80, corner_radius=5, font=ctk.CTkFont(size=14)
        )
        self.text_textbox.pack(fill="x", padx=10, pady=10, expand=True)
        self.text_textbox.insert("1.0", "")  # Boş başlat
        self.text_textbox.configure(state="disabled")

        # CTkTextbox için wrapper metodu
        self.text_label = type("", (), {})()  # Boş bir nesne oluştur
        self.text_label.configure = lambda **kwargs: self.update_textbox(
            self.text_textbox, kwargs.get("text", "")
        )
        self.text_label.cget = lambda key: (
            self.text_textbox.get("1.0", "end-1c") if key == "text" else None
        )

        # F. Çeviri
        translation_frame = ctk.CTkFrame(right_scroll, corner_radius=10)
        translation_frame.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(
            translation_frame, text="Çeviri", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.translation_textbox = ctk.CTkTextbox(
            translation_frame, height=80, corner_radius=5, font=ctk.CTkFont(size=14)
        )
        self.translation_textbox.pack(fill="x", padx=10, pady=10, expand=True)
        self.translation_textbox.insert("1.0", "")  # Boş başlat
        self.translation_textbox.configure(state="disabled")

        # CTkTextbox için wrapper metodu
        self.translation_label = type("", (), {})()  # Boş bir nesne oluştur
        self.translation_label.configure = lambda **kwargs: self.update_textbox(
            self.translation_textbox, kwargs.get("text", "")
        )
        self.translation_label.cget = lambda key: (
            self.translation_textbox.get("1.0", "end-1c") if key == "text" else None
        )

        # G. Mors Kodu
        morse_frame = ctk.CTkFrame(right_scroll, corner_radius=10)
        morse_frame.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(
            morse_frame, text="Mors Kodu", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.morse_textbox = ctk.CTkTextbox(
            morse_frame,
            height=50,
            corner_radius=5,
            font=ctk.CTkFont(family="Courier", size=14),
        )
        self.morse_textbox.pack(fill="x", padx=10, pady=5, expand=True)
        self.morse_textbox.insert("1.0", "")  # Boş başlat
        self.morse_textbox.configure(state="disabled")

        # CTkTextbox için wrapper metodu
        self.morse_label = type("", (), {})()  # Boş bir nesne oluştur
        self.morse_label.configure = lambda **kwargs: self.update_textbox(
            self.morse_textbox, kwargs.get("text", "")
        )
        self.morse_label.cget = lambda key: (
            self.morse_textbox.get("1.0", "end-1c") if key == "text" else None
        )

        morse_button_frame = ctk.CTkFrame(morse_frame, fg_color="transparent")
        morse_button_frame.pack(fill="x", padx=10, pady=5)

        # Daha kompakt butonlar
        ctk.CTkButton(
            morse_button_frame,
            text="Metni Çevir",
            command=self.app.convert_to_morse,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            height=30,
            fg_color=self.accent_color,
        ).pack(side="left", padx=2, pady=3, fill="x", expand=True)

        ctk.CTkButton(
            morse_button_frame,
            text="Çeviriyi Çevir",
            command=self.app.convert_translation_to_morse,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            height=30,
            fg_color=self.accent_color,
        ).pack(side="left", padx=2, pady=3, fill="x", expand=True)

        ctk.CTkButton(
            morse_button_frame,
            text="Mors Kodunu Çal",
            command=self.app.play_morse,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            height=30,
            fg_color=self.accent_color,
        ).pack(side="left", padx=2, pady=3, fill="x", expand=True)

        # H. Aksiyon Butonları
        button_frame = ctk.CTkFrame(right_scroll, corner_radius=10)
        button_frame.pack(fill="x", pady=5, padx=5)

        # Tüm butonlar için standart grid layout (daha eşit dağıtım için)
        action_button_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        action_button_frame.pack(fill="x", padx=10, pady=5)

        # İlk sıra: Çevir ve Boşluk Ekle (2 kolon)
        row1_frame = ctk.CTkFrame(action_button_frame, fg_color="transparent")
        row1_frame.pack(fill="x", pady=2)

        ctk.CTkButton(
            row1_frame,
            text="Çevir",
            command=self.app.translate_text,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            height=35,
            fg_color=self.accent_color,
        ).pack(side="left", padx=2, pady=2, fill="x", expand=True)

        space_button = ctk.CTkButton(
            row1_frame,
            text="Boşluk Ekle",
            command=self.app.add_space,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            height=35,
            fg_color=self.accent_color,
        )
        space_button.pack(side="left", padx=2, pady=2, fill="x", expand=True)

        # İkinci sıra: Harf Sil ve Temizle (2 kolon)
        row2_frame = ctk.CTkFrame(action_button_frame, fg_color="transparent")
        row2_frame.pack(fill="x", pady=2)

        ctk.CTkButton(
            row2_frame,
            text="Harf Sil",
            command=self.app.delete_last_letter,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            height=35,
            fg_color=self.accent_color,
        ).pack(side="left", padx=2, pady=2, fill="x", expand=True)

        ctk.CTkButton(
            row2_frame,
            text="Temizle",
            command=self.app.clear_text,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            height=35,
            fg_color=self.accent_color,
        ).pack(side="left", padx=2, pady=2, fill="x", expand=True)

        # I. Alt Bilgi Paneli
        info_frame = ctk.CTkFrame(right_scroll, corner_radius=10)
        info_frame.pack(fill="x", pady=5, padx=5)

        # Daha okunaklı metin düzeni
        controls_title = ctk.CTkLabel(
            info_frame, text="Kontroller:", font=ctk.CTkFont(size=14, weight="bold")
        )
        controls_title.pack(anchor="w", padx=10, pady=(10, 5))

        # Kontrol tuşları ayrı ayrı
        control_keys_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        control_keys_frame.pack(fill="x", padx=10, pady=0)

        # 2 sütunlu düzen
        ctk.CTkLabel(
            control_keys_frame,
            text="SPACE: Manuel boşluk",
            font=ctk.CTkFont(size=13),
            justify="left",
        ).pack(anchor="w", pady=1)
        ctk.CTkLabel(
            control_keys_frame,
            text="BACKSPACE: Harf sil",
            font=ctk.CTkFont(size=13),
            justify="left",
        ).pack(anchor="w", pady=1)
        ctk.CTkLabel(
            control_keys_frame,
            text="ENTER: Çevir",
            font=ctk.CTkFont(size=13),
            justify="left",
        ).pack(anchor="w", pady=1)
        ctk.CTkLabel(
            control_keys_frame,
            text="Q: Çıkış",
            font=ctk.CTkFont(size=13),
            justify="left",
        ).pack(anchor="w", pady=1)

        # İpuçları
        tips_title = ctk.CTkLabel(
            info_frame, text="İpuçları:", font=ctk.CTkFont(size=14, weight="bold")
        )
        tips_title.pack(anchor="w", padx=10, pady=(10, 5))

        tips_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        tips_frame.pack(fill="x", padx=10, pady=(0, 10))

        tip1 = "- Her kelimeden sonra 'Boşluk Ekle' düğmesine basmanız gerekir"
        tip2 = "- Harf silme düğmesi ile son harfi silebilirsiniz"
        tip3 = f"- Bir harfin yazılması için {self.app.required_stable_frames} frame boyunca aynı harf algılanmalıdır"

        ctk.CTkLabel(
            tips_frame, text=tip1, font=ctk.CTkFont(size=13), justify="left"
        ).pack(anchor="w", pady=1)
        ctk.CTkLabel(
            tips_frame, text=tip2, font=ctk.CTkFont(size=13), justify="left"
        ).pack(anchor="w", pady=1)
        ctk.CTkLabel(
            tips_frame, text=tip3, font=ctk.CTkFont(size=13), justify="left"
        ).pack(anchor="w", pady=1)

    # CTkTextbox için text içeriğini güncelleyen yardımcı metot
    def update_textbox(self, textbox, text):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")

    # Harf işleme ilerlemesini güncelleme metodu
    def update_letter_progress(self, current_count):
        # İlerleme çubuğunu güncelle
        progress = current_count / self.app.required_stable_frames
        self.letter_progress_var.set(progress)
        # Etiketi güncelle
        self.letter_progress_label.configure(
            text=f"{current_count}/{self.app.required_stable_frames}"
        )

    # CustomTkinter ile uyumlu olması için kamera görüntüsünü güncelleme metodu
    def set_camera_image(self, img):
        """Kamera görüntüsünü günceller."""
        if img is not None:
            # OpenCV BGR'dan RGB'ye dönüştür
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # RGB'yi PIL Image'a çevir
            img_pil = Image.fromarray(img)
            # PIL Image'ı CTkImage'a çevir
            ctk_img = ctk.CTkImage(
                light_image=img_pil, dark_image=img_pil, size=(640, 480)
            )
            # Label'ı güncelle
            self.camera_label.configure(image=ctk_img, text="")

    # Eski kodla uyumluluk için metod eklentileri
    def config(self, **kwargs):
        if "text" in kwargs and hasattr(self, "configure"):
            self.configure(text=kwargs["text"])

    def configure(self, **kwargs):
        if "text" in kwargs and isinstance(self, ctk.CTkTextbox):
            self.update_textbox(self, kwargs["text"])

    # Tkinter'dan CustomTkinter'a geçiş için uyumluluk metodları
    def cget(self, key):
        if key == "text" and isinstance(self, ctk.CTkTextbox):
            return self.get("1.0", "end-1c")
        return getattr(self, key)
