"""
Performans analizi için profiling script'i.
"""

import cProfile
import pstats
import tkinter as tk
from pstats import SortKey

from src.main_app import SignLanguageApp
from ui_design import AppUI


def main():
    """Ana uygulama döngüsü."""
    root = tk.Tk()
    app = SignLanguageApp(root, AppUI)

    # Kamerayı başlat
    app.toggle_camera()

    # 100 frame işle
    for _ in range(100):
        root.update()

    # Kamerayı kapat
    app.toggle_camera()
    root.destroy()


if __name__ == "__main__":
    # Profiling başlat
    profiler = cProfile.Profile()
    profiler.enable()

    # Uygulamayı çalıştır
    main()

    # Profiling sonlandır
    profiler.disable()

    # Sonuçları analiz et
    stats = pstats.Stats(profiler).sort_stats(SortKey.TIME)
    stats.dump_stats("profile_results.prof")

    # Özet göster
    stats.print_stats(20)  # En yavaş 20 fonksiyonu göster
